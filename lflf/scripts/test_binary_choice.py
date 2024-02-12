import h5py
import numpy as np
import random
import time
import openai

# Loading system prompts
from lflf.prompts.prompts import overall_prompt, system_prompt_task, examples_context, user_context, behavior_system_prompt, \
template_long, template_short, template_long_eval, template_short_eval

import lflf.utils.robosuite_utils.transform_utils as T

"""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""
""" Setting up OpenAI API """

API_MODE_AZURE = False

if API_MODE_AZURE:
    # Set up the OpenAI API.
    openai.api_type = "azure"
    openai.api_version = "2023-05-15"
    openai.api_base = "https://nexus-openai-1.openai.azure.com/"
    openai.api_key = "161889719bee40d18b1824df87131114" 
else:
    openai.api_key_path = "/home/huihanliu/.config/openai.token" 

"""""""""""""""""""""""""""""
"""""""""""""""""""""""""""""

def obtain_data(data_path):
    f = h5py.File(data_path, "r")
    # Obtain the list of trajectory keys
    demos = list(f["data"].keys())
    inds = np.argsort([int(elem[5:]) for elem in demos])
    demos = [demos[i] for i in inds]
    return f, demos



def obtain_state_action_info(data_ep):
    original_actions_full = data_ep["actions"][()]
    relabeled_actions_full = data_ep["actions_relabeled"][()]
    relabeled_actions_full[:,3:5] = 0

    robot_eef_pos = data_ep["obs"]["robot0_eef_pos"][()]
    robot0_eef_quat = data_ep["obs"]["robot0_eef_quat"][()]
    object_info = data_ep["obs"]["object"][()]
    object_pos = object_info[:,:3]
    object_quat = object_info[:,3:7]

    state_action_data_full = {
        "original_actions": original_actions_full,
        "relabeled_actions" : relabeled_actions_full,

        "robot_pos": robot_eef_pos,
        "robot_quat": robot0_eef_quat, 
        "robot_angle": np.array([T.quat2axisangle(q) for q in robot0_eef_quat]) / np.pi * 180.,
        
        "object_pos": object_pos,
        "object_quat": object_quat,
        "object_angle": np.array([T.quat2axisangle(q) for q in object_quat]) / np.pi * 180.,
    }
    return state_action_data_full


# only get relabeled region for comparison
# the code for "human relabeling" of pre-intervention region is 20
def obtain_relabeled_mask(data_ep):
    relabeled_mask = data_ep["intv_labels_relabeled"][()] == 20
    return relabeled_mask


def obtain_mask_data_only(state_action_data_full, data_ep):
    state_action_data_full = state_action_data_full.copy()

    relabeled_mask = obtain_relabeled_mask(data_ep)

    for key in state_action_data_full:
        if type(state_action_data_full[key]) == dict:
            for key1 in state_action_data_full[key]:
                state_action_data_full[key][key1] = state_action_data_full[key][key1][relabeled_mask]
        else:
            state_action_data_full[key] = state_action_data_full[key][relabeled_mask]
    return state_action_data_full


def get_one_single_tuple(state_action_data, idx):
    new_dict = dict()
    for key in state_action_data:
        new_dict[key] = state_action_data[key][idx]
    return new_dict


def add_handle_data(state_action_data_full, data_ep_handle):
    handle_pos = data_ep_handle["obs"]["handle_pos"][()]
    handle_angle = data_ep_handle["obs"]["handle_angle"][()]
    state_action_data_full["handle_pos"] = handle_pos
    state_action_data_full["handle_angle"] = handle_angle


def _call_model(messages, model, temperature, request_timeout):
    # Place one call to the model, returning the response and total number of tokens involved.
    # Minor difference between using azure service (like MSR do) or not: use `engine` or `model`
    if API_MODE_AZURE:
        response = openai.ChatCompletion.create(
            messages=messages,
            engine=model,
            temperature=temperature,
            request_timeout=request_timeout
        )
    else:
        response = openai.ChatCompletion.create(
            messages=messages,
            model=model,
            temperature=temperature,
            request_timeout=request_timeout
        )
    response_usage = response['usage']
    num_input_tokens = response_usage['prompt_tokens']
    num_output_tokens = response_usage['completion_tokens']
    return num_input_tokens + num_output_tokens, response['choices'][0]['message']['content']


def call_model(messages, model, temperature, request_timeout):
    while True:
        try:
            return _call_model(messages, model, temperature, request_timeout)
        except openai.error.Timeout as e:
            print(f"Request timed out: {e}")
            print("Retrying the call...")
            continue
        except openai.error.RateLimitError as e:
            print(f"OpenAI API request exceeded rate limit: {e}")
            # Wait the timeout period before retrying, to avoid a retry storm.
            print(f"Waiting {request_timeout} seconds before retrying...")
            time.sleep(request_timeout)
            print("Retrying the call...")
            continue
        except openai.error.APIError as e:
            print(f"OpenAI API returned an API Error: {e}")
            exit(1)
        except openai.error.AuthenticationError as e:
            print(f"OpenAI API returned an Authentication Error: {e}")
            exit(1)
        except openai.error.APIConnectionError as e:
            print(f"Failed to connect to OpenAI API: {e}")
            exit(1)
        except openai.error.InvalidRequestError as e:
            print(f"Invalid Request Error: {e}")
            exit(1)
        except openai.error.ServiceUnavailableError as e:
            print(f"Service Unavailable: {e}")
            exit(1)
        except Exception as e:
            print(f"Unexpected exception: {e}")
            exit(1)


# Now include robot position and angle, handle position and angle
def _format_example(one_step, eval_mode=False, convert_int=False, short=False):
    original_actions = one_step['original_actions']
    relabeled_actions = one_step['relabeled_actions']
    robot_pos = one_step['robot_pos']
    robot_angle = one_step['robot_angle']
    object_pos = one_step['handle_pos']
    object_angle = one_step['handle_angle']
    
    def _format_numpy(arr, angle=False):            
        if angle:
            arr = arr[-1]
            arr = np.where(np.sign(arr) == 0, 0.0, arr)
            arr = int(arr)
            return str(arr)
            
        arr = arr.round(2)
        arr = np.where(np.sign(arr) == 0, 0.0, arr)
        if convert_int:
            arr = np.int8(arr * 100)
        return str(arr)
    
    choice = np.random.randint(2)
    action_choice_0 = relabeled_actions if choice == 0 else original_actions
    action_choice_1 = original_actions if choice == 0 else relabeled_actions
    assert not (action_choice_0 == action_choice_1).all()
    
    template_base = template_short if short else template_long
    template_base_eval = template_short_eval if short else template_long_eval
    
    # 1 - choice: original_actions is right, relabeled_actions is wrong
    template = template_base.format(
        _format_numpy(robot_pos),
        _format_numpy(robot_angle, angle=True),
        _format_numpy(object_pos),
        _format_numpy(object_angle, angle=True),
        _format_numpy(action_choice_0),
        _format_numpy(action_choice_1),
        1 - choice
    )
    
    if eval_mode:
        template = template_base_eval.format(
            _format_numpy(robot_pos),
            _format_numpy(robot_angle, angle=True),
            _format_numpy(object_pos),
            _format_numpy(object_angle, angle=True),
            _format_numpy(action_choice_0),
            _format_numpy(action_choice_1),
        )

    return template, 1 - choice

# Functions to create in-context examples script, and the user prompt script (for the actual query):


def create_examples_from_dataset(context, benchmark_dataset, num_examples=50, convert_int=False, short=False):
    if short:
        short_description = """
        The following inputs are formated with each line representing
        Robot Position, Robot Orientation, Object Position, Object Orientation, Action Choice 0 and Action Choice 1.
        """
        context = context + short_description
    for i in range(num_examples):
        example, _ = _format_example(benchmark_dataset[i], convert_int=convert_int)
        context = context + example
    return context

def create_user_prompt_from_dataset(context, benchmark_dataset, num_examples=1, convert_int=False, short=False, idx=-1):
    example, true_answer = _format_example(benchmark_dataset[idx], eval_mode=True, convert_int=convert_int)
    context = context + example
    return context, true_answer


def _process_text(text_response):
    # single result without explanation
    if len(text_response) == 1 and text_response in ["0", "1"]:
        return int(text_response)
    # have explanation
    else:
        res = text_response[0] # assume result comes first for now
        if res in ["0", "1"]:
            return int(res)
        else:
            return -1 # invalid

def _accuracy(true, pred):
    difference = np.array(true) - np.array(pred)
    # Count the number of matching elements (zeros in the difference array)
    matching_elements = np.count_nonzero(difference == 0)
    # Calculate the accuracy as a percentage
    accuracy = (matching_elements / len(true))
    return accuracy


def test_binary_choice(system_prompt, user_prompt, model="gpt-35-turbo", temperature=0.1):
    system_prompt = system_prompt
    user_prompt = user_prompt
    messages = [
        {"role": "system", "content": behavior_system_prompt},
        {"role": "user", "content": system_prompt + user_prompt},
    ]
    print("Full message: ")
    print(messages[0]["content"])
    print(messages[1]["content"])
    return call_model(messages, model=model, temperature=temperature, request_timeout=100)


def test_action_critic_accuracy(num_incontext_examples, num_trials, model, temperature=0.1):
    """
    num_incontext_examples: number of examples to learn from
    num_trials: number of samples to test LLM
    model: model names (e.g. "gpt-35-turbo")
    """
    true_answer_lst = []
    response_lst = []
    for idx in range(num_trials):

        # Creating prompt (system + in-context examples)
        examples = create_examples_from_dataset(examples_context,
                                                benchmark_dataset_train,
                                                num_examples=num_incontext_examples,
                                                convert_int=True)

        system_prompt = overall_prompt + system_prompt_task

        print("Trial {}".format(idx))

        # Creating user query
        user_prompt, true_answer = create_user_prompt_from_dataset(user_context,
                                                                   benchmark_dataset_test,
                                                                   num_examples=1,
                                                                   convert_int=True,
                                                                   idx=idx)

        num_tokens, text_response = test_binary_choice(system_prompt, user_prompt, model=model, temperature=temperature)
        
        #print(user_prompt)
        true_answer_lst.append(true_answer)
        print('\033[93m Expected answer: \033[0m')
        print('\033[93m Action {} \033[0m'.format(true_answer))        
        
        print("\033[92m Model Output:  \033[0m")
        print("\033[92m {} \033[0m".format(text_response))
        print()
        print()


def get_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--data_path', type=str, default="/home/huihanliu/LoLF_data/intv_relabeled.hdf5")
    return parser

if __name__ == "__main__":

    args = get_parser().parse_args()
    #data_path = args.data_path

    data_path = "/home/huihanliu/square_grasp_only_relabel_merged.hdf5"
    handle_path = "/home/huihanliu/square_grasp_only_relabel_handle.hdf5"

    """
    Creating Dataset
    """
    benchmark_dataset = []
    f, demos = obtain_data(data_path)
    f_handle, demos_handle = obtain_data(handle_path)

    for ep in demos:
        data_ep = f["data"][ep]
        state_action_data_full = obtain_state_action_info(data_ep)

        data_ep_handle = f_handle["data"][ep]
        add_handle_data(state_action_data_full, data_ep_handle)
        
        state_action_data = obtain_mask_data_only(state_action_data_full, data_ep)
        for idx in range(len(state_action_data["original_actions"])):
            single_step_state_action = get_one_single_tuple(state_action_data, idx)
            benchmark_dataset.append(single_step_state_action)
    

    print(benchmark_dataset[0].keys())
    np.save("square_llm_benchmark_v0_grasp_only", benchmark_dataset)

    benchmark_dataset_train = benchmark_dataset[:150]
    benchmark_dataset_test = benchmark_dataset[150:]
    random.shuffle(benchmark_dataset_train)
    random.shuffle(benchmark_dataset_test)


    """
    LLM as Critic
    """
    model_name = "gpt-35-turbo" if API_MODE_AZURE else "gpt-4"
    test_action_critic_accuracy(num_incontext_examples=20,
                                num_trials=30,
                                model=model_name,
                                temperature=0.7
                                )
