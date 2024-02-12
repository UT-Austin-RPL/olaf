import lflf.prompts.prompts as system_prompts
import lflf.prompts.summary as summary_prompts
import lflf.prompts.human_feedback_shorten as human_feedback_prompts
from lflf.utils.llm_utils import *
from lflf.utils.openai_utils import call_model
from lflf.utils.data_utils import select_obs_idx
from lflf.utils.llm_utils import *
import lflf.utils.robosuite_utils.transform_utils as T
import re
import json
from lflf.utils.random_utils import *
import os

class LLMCritic():
    """
    LLM as the critic to select one action from action candidates
    """
    def __init__(self, args, time, per_ep=None):

        self._temperature = args.temperature
        self._candidate_strategy = args.candidate_strategy
        self._have_low_level_info = args.have_low_level_info
        self._llm_model = args.gpt_model
        self._llm_model_summary = "gpt-4" #"gpt-35-turbo"
        self._task_name = args.task_name
        try:
            self._timeout = args.timeout
        except:
            self._timeout = 60
        
        # create log dir
        self._time = time
        os.makedirs(self._time, exist_ok=True)
        
        # create log file
        if per_ep is not None:
            self._log_file = open("{}/{}_llm_{}_{}_temp_{}.txt".format(self._time,
                                                                    per_ep,
                                                                    self._candidate_strategy, 
                                                                    self._llm_model, 
                                                                    self._temperature), "w")
        else:
            self._log_file = open("{}/llm_{}_{}_temp_{}.txt".format(self._time,
                                                                    self._candidate_strategy, 
                                                                    self._llm_model, 
                                                                    self._temperature), "w")
        
            
    def eval(self, action_candidates, obs, language_correction=None):
        
        self._num_actions = len(action_candidates)

        try:
            system_prompt, user_prompt = self._create_prompt(action_candidates, obs, language_correction)
            print_color(system_prompt, "yellow")
            print_color(user_prompt, "yellow")

            self._log_file.write("\n\n\n")
            self._log_file.write("system prompt: {}\n".format(system_prompt))
            self._log_file.write("user prompt: {}\n".format(user_prompt))
            self._log_file.write("\n")

            action_idx = self.llm_call(system_prompt, user_prompt)
            action_idx = int(action_idx)
            print()
            print_color("final action idx: ", "green")
            print_color(action_idx, "green")

            self._log_file.write("final action idx: {}\n".format(action_idx))
            self._log_file.write("\n")

            # randomly select an action if the action idx is invalid
            if action_idx not in list(range(len(action_candidates))):
                print_color("LLM failed. Randomly select an action.", "red")
                return np.random.randint(0, len(action_candidates))

            return action_idx
        
        except:
            # randomly select an action
            print_color("LLM failed. Randomly select an action.", "red")
            return np.random.randint(0, self._num_actions)
    
    def llm_call(self, system_prompt, user_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        _, response = call_model(messages, 
                          model=self._llm_model, 
                          temperature=self._temperature, 
                          request_timeout=self._timeout + np.random.randint(-10, 10)
                          )
        
        print_color(response, "blue")
        self._log_file.write("first response: {}\n".format(response))
        self._log_file.write("\n")

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": response},
            {"role": "user", "content": summary_prompts.summary_prompt},
        ]       

        idx = None

        # Summarize LLM output
        num_attempts = 3
        for i in range(num_attempts):

            _, action_choice_response = call_model(messages, 
                            model=self._llm_model_summary, 
                            temperature=0.1, 
                            request_timeout=10)

            try:
                json_str = re.search(r'\{.*?\}', action_choice_response, re.DOTALL).group()
                json_str = json_str.replace("'", '"')
                action_choice_json = json.loads(json_str)
                idx = list(action_choice_json.values())[0]
                break
            except:
                print("LLM failed to return a valid json object. Output text: {}".format(action_choice_response))
                print("Retrying...")
                messages.append({"role": "assistant", "content": action_choice_response})
                messages.append({"role": "user", "content": summary_prompts.summary_correction})
                continue
        
        if idx is None:
            print("LLM failed to return a valid json object after {} attempts. Output text: \n{}".format(num_attempts, action_choice_response))
            print("Returning a random action idx...")
            idx = np.random.randint(0, self._num_actions)

        return idx
    
    def _create_prompt(self, action_candidates, obs, language_correction=None):
        system_prompt = system_prompts.system_prompt_behavior

        if language_correction is not None:
            system_prompt = system_prompts.system_prompt_behavior_human
        
        user_prompt = system_prompts.prompt_robot \
                    + system_prompts.prompt_task[self._task_name] \
                    + system_prompts.prompt_instruction \
                    + system_prompts.prompt_instruction_cot
                    # TODO: + system_prompts.prompt_instruction_cot_combine_onedim

        obs_processed = self._process_obs(obs)
        obs_string = format_obs(obs_processed, system_prompts.template_obs[self._task_name], task=self._task_name)
        
        action_string = format_action(action_candidates)

        user_prompt = user_prompt + obs_string + action_string

        if language_correction is not None:
            language_prompt = self._process_language(language_correction)
            user_prompt = user_prompt + language_prompt

        return system_prompt, user_prompt 
    
    def _process_language(self, language_correction):
        return system_prompts.prompt_language_correction + language_correction
           
    def _process_obs(self, obs_i):
        robot_eef_pos = obs_i["robot0_eef_pos"]
        robot_eef_quat = obs_i["robot0_eef_quat"]

        # correct the robot pose
        inv_initial = T.quat_inverse([1,0,0,0])
        robot_eef_quat = T.quat_multiply(robot_eef_quat, inv_initial) 

        robot_angle = np.array(T.quat2axisangle(robot_eef_quat)) / np.pi * 180.

        gripper_state = np.array([1]) if obs_i["robot0_gripper_qpos"][0] - obs_i["robot0_gripper_qpos"][1] < 0.065 else np.array([-1])


        if self._task_name == "square":
            handle_pos = obs_i["handle_pos"]
            handle_quat = obs_i["handle_quat"]
            handle_angle = np.array(T.quat2axisangle(handle_quat)) / np.pi * 180.

            nut_pos = obs_i["object"][:3]
            nut_quat = obs_i["object"][3:7]
            nut_angle = np.array(T.quat2axisangle(nut_quat)) / np.pi * 180.

            peg_pos = obs_i["peg_pos"]
            peg_quat = obs_i["peg_quat"]
            peg_angle = np.array(T.quat2axisangle(peg_quat)) / np.pi * 180.
        
            print_color("handle_pos: ", "green")
            print_color(handle_pos, "green")
            print_color("handle_angle: ", "green")
            print_color(handle_angle, "green")
            
            print_color("nut_pos: ", "green")
            print_color(nut_pos, "green")
            print_color("nut_angle: ", "green")
            print_color(nut_angle, "green")
            
            print_color("peg_pos: ", "green")
            print_color(peg_pos, "green")
            print_color("peg_angle: ", "green")
            print_color(peg_angle, "green")
            
            state_info = {
            "robot_pos": robot_eef_pos,
            "robot_angle": robot_angle,
            
            "handle_pos": handle_pos,
            "handle_angle": handle_angle,
        
            "nut_pos": nut_pos,
            "nut_angle": nut_angle,
            
            "peg_pos": peg_pos,
            "peg_angle": peg_angle,
            
            "gripper_state": gripper_state,
            }

        elif self._task_name == "threading":
            all_obs = ["needle_needle", "needle_handle", "ring"]
    
        elif self._task_name == "toolhang":
            all_obs = ["base",
                        "hook_handle",
                        "hook_bottom",
                        "hook_hang",
                        "tool_handle",
                        "tool_hole"
                        ]

        elif self._task_name == "coffee":
            all_obs = ["pod", "pod_holder", "lid"]

        elif self._task_name == "can":
            all_obs = ["can", "bin"]
        
        else:
            raise ValueError("task not found")
        
        object_info = {}
        for obs in all_obs:
            obj_pos = obs_i["{}_pos".format(obs)]
            if obs != "bin":
                obj_quat = obs_i["{}_quat".format(obs)]
            else:
                obj_quat = [0,0,0,1]
            obj_angle = np.array(T.quat2axisangle(obj_quat)) / np.pi * 180.
            object_info["{}_pos".format(obs)] = obj_pos
            object_info["{}_angle".format(obs)] = obj_angle

            self._print_obs_color(obs, obj_pos, obj_angle)

        state_info = {
            "robot_pos": robot_eef_pos,
            "robot_angle": robot_angle,    
            "gripper_state": gripper_state,
        }

        state_info.update(object_info)

        return state_info

    def _print_obs_color(self, obj_name, obj_pos, obj_angle, color="green"):
        print_color("{}_pos: ".format(obj_name), color)
        print_color(obj_pos, color)
        print_color("{}_angle: ".format(obj_name), color)
        print_color(obj_angle, color)

class LLMCriticReturnAction(LLMCritic):
    """
    LLM as the critic to select one action from action candidates
    """
    def __init__(self, args, time, per_ep=None):
        super().__init__(args, time, per_ep)

    def eval(self, action_candidates, obs, language_correction=None):
        try:
            system_prompt, user_prompt = self._create_prompt(action_candidates, obs, language_correction)
            print_color(system_prompt, "yellow")
            print_color(user_prompt, "yellow")

            self._log_file.write("\n\n\n")
            self._log_file.write("system prompt: {}\n".format(system_prompt))
            self._log_file.write("user prompt: {}\n".format(user_prompt))
            self._log_file.write("\n")

            action = self.llm_call(system_prompt, user_prompt)
            print()
            print_color("final action: ", "green")
            print_color(action, "green")

            self._log_file.write("final action: {}\n".format(action))
            self._log_file.write("\n")

            if action is None:
                return action

            action = [a / 100 for a in action]
            print("action: ", action)

            return action
        
        except:
            # randomly select an action
            print_color("LLM failed. Did not return an action.", "red")
            return None
        
    
    def llm_call(self, system_prompt, user_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        _, response = call_model(messages, 
                          model=self._llm_model, 
                          temperature=self._temperature, 
                          request_timeout=self._timeout + np.random.randint(-10, 10)
                          )
        
        print_color(response, "blue")
        self._log_file.write("first response: {}\n".format(response))
        self._log_file.write("\n")
        
        summary_prompt = summary_prompts.summary_prompt_return_action
        summary_prompt_correction = summary_prompts.summary_correction_return_action
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": response},
            {"role": "user", "content": summary_prompt},
        ]       

        action = None
        # Summarize LLM output
        num_attempts = 3
        for i in range(num_attempts):

            _, action_choice_response = call_model(messages, 
                            model=self._llm_model_summary, 
                            temperature=0.1, 
                            request_timeout=10)
            print_color(action_choice_response, "yellow")

            try:
                json_str = re.search(r'\{.*?\}', action_choice_response, re.DOTALL).group()
                json_str = json_str.replace("'", '"')
                print_color(json_str, "yellow")
                action_choice_json = json.loads(json_str)
                action = list(action_choice_json.values())[0]
                print_color(action, "yellow")
                break
            except:
                print("LLM failed to return a valid json object. Output text: {}".format(action_choice_response))
                print("Retrying...")
                messages.append({"role": "assistant", "content": action_choice_response})
                messages.append({"role": "user", "content": summary_prompt_correction})
                continue
        
        if action is None:
            print("LLM failed to return a valid json object after {} attempts. Output text: \n{}".format(num_attempts, action_choice_response))
            print("Returning a random action idx...")

        return action

    def _create_prompt(self, action_candidates, obs, language_correction=None):
        system_prompt = system_prompts.system_prompt_behavior

        if language_correction is not None:
            system_prompt = system_prompts.system_prompt_behavior_human
        
        user_prompt = system_prompts.prompt_robot \
                    + system_prompts.prompt_task \
                    + system_prompts.prompt_instruction \
                    + system_prompts.prompt_instruction_cot_return_action
                    # TODO: + system_prompts.prompt_instruction_cot_combine_onedim

        obs_processed = self._process_obs(obs)
        obs_string = format_obs(obs_processed, system_prompts.template_obs[self._task_name], task=self._task_name)

        user_prompt = user_prompt + obs_string

        if language_correction is not None:
            language_prompt = self._process_language(language_correction)
            user_prompt = user_prompt + language_prompt

        return system_prompt, user_prompt 
    


class LLMCriticEditAction(LLMCritic):
    """
    LLM as the critic to select one action from action candidates
    """
    def __init__(self, args, time, per_ep=None):
        super().__init__(args, time, per_ep)

    def eval(self, action_candidates, obs, language_correction=None):
        try:
            system_prompt, user_prompt = self._create_prompt(action_candidates, obs, language_correction)
            print_color(system_prompt, "yellow")
            print_color(user_prompt, "yellow")

            self._log_file.write("\n\n\n")
            self._log_file.write("system prompt: {}\n".format(system_prompt))
            self._log_file.write("user prompt: {}\n".format(user_prompt))
            self._log_file.write("\n")

            action = self.llm_call(system_prompt, user_prompt)
            print()
            print_color("final action: ", "green")
            print_color(action, "green")

            self._log_file.write("final action: {}\n".format(action))
            self._log_file.write("\n")

            if action is None:
                return action

            action = [a / 100 for a in action]
            print("action: ", action)

            return action
        
        except:
            # randomly select an action
            print_color("LLM failed. Did not return an action.", "red")
            return None
        
    
    def llm_call(self, system_prompt, user_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        _, response = call_model(messages, 
                          model=self._llm_model, 
                          temperature=self._temperature, 
                          request_timeout=self._timeout + np.random.randint(-10, 10)
                          )
        
        print_color(response, "blue")
        self._log_file.write("first response: {}\n".format(response))
        self._log_file.write("\n")
        
        summary_prompt = summary_prompts.summary_prompt_return_action
        summary_prompt_correction = summary_prompts.summary_correction_return_action
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": response},
            {"role": "user", "content": summary_prompt},
        ]       

        action = None
        # Summarize LLM output
        num_attempts = 3
        for i in range(num_attempts):

            _, action_choice_response = call_model(messages, 
                            model=self._llm_model_summary, 
                            temperature=0.1, 
                            request_timeout=10)
            print_color(action_choice_response, "yellow")

            try:
                json_str = re.search(r'\{.*?\}', action_choice_response, re.DOTALL).group()
                json_str = json_str.replace("'", '"')
                print_color(json_str, "yellow")
                action_choice_json = json.loads(json_str)
                action = list(action_choice_json.values())[0]
                print_color(action, "yellow")
                break
            except:
                print("LLM failed to return a valid json object. Output text: {}".format(action_choice_response))
                print("Retrying...")
                messages.append({"role": "assistant", "content": action_choice_response})
                messages.append({"role": "user", "content": summary_prompt_correction})
                continue
        
        if action is None:
            print("LLM failed to return a valid json object after {} attempts. Output text: \n{}".format(num_attempts, action_choice_response))
            print("Returning a random action idx...")

        return action

    def _create_prompt(self, action_candidates, obs, language_correction=None):
        system_prompt = system_prompts.system_prompt_behavior

        if language_correction is not None:
            system_prompt = system_prompts.system_prompt_behavior_human
        
        user_prompt = system_prompts.prompt_robot \
                    + system_prompts.prompt_task \
                    + system_prompts.prompt_instruction \
                    + system_prompts.prompt_instruction_cot_edit_action
                    # TODO: + system_prompts.prompt_instruction_cot_combine_onedim

        obs_processed = self._process_obs(obs)
        obs_string = format_obs(obs_processed, system_prompts.template_obs[self._task_name], task=self._task_name)

        assert len(action_candidates) == 1
        action_string = format_action_single(action_candidates[0])

        user_prompt = user_prompt + obs_string + action_string

        if language_correction is not None:
            language_prompt = self._process_language(language_correction)
            user_prompt = user_prompt + language_prompt

        return system_prompt, user_prompt 
    

class LLMCriticCombineOnedimAction(LLMCritic):
    """
    LLM as the critic to select one action from action candidates
    """
    def __init__(self, args, time, per_ep=None):
        super().__init__(args, time, per_ep)

    def eval(self, action_candidates, obs, language_correction=None):

        if True: #try:
            system_prompt, user_prompt = self._create_prompt(action_candidates, obs, language_correction)
            print_color(system_prompt, "yellow")
            print_color(user_prompt, "yellow")

            self._log_file.write("\n\n\n")
            self._log_file.write("system prompt: {}\n".format(system_prompt))
            self._log_file.write("user prompt: {}\n".format(user_prompt))
            self._log_file.write("\n")

            action = self.llm_call(system_prompt, user_prompt)
            print()
            print_color("final action: ", "green")
            print_color(action, "green")

            self._log_file.write("final action: {}\n".format(action))
            self._log_file.write("\n")

            if action is None:
                return action

            action = [a / 100 for a in action]
            print("action: ", action)

            return action
        
        # except:
        #     # randomly select an action
        #     print_color("LLM failed. Did not return an action.", "red")
        #     return None
        
    
    def llm_call(self, system_prompt, user_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        _, response = call_model(messages, 
                          model=self._llm_model, 
                          temperature=self._temperature, 
                          request_timeout=self._timeout + np.random.randint(-10, 10)
                          )
        
        print_color(response, "blue")
        self._log_file.write("first response: {}\n".format(response))
        self._log_file.write("\n")
        
        summary_prompt = summary_prompts.summary_prompt_return_action
        summary_prompt_correction = summary_prompts.summary_correction_return_action
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": response},
            {"role": "user", "content": summary_prompt},
        ]       

        action = None
        # Summarize LLM output
        num_attempts = 3
        for i in range(num_attempts):

            _, action_choice_response = call_model(messages, 
                            model=self._llm_model_summary, 
                            temperature=0.1, 
                            request_timeout=10)
            print_color(action_choice_response, "yellow")

            try:
                json_str = re.search(r'\{.*?\}', action_choice_response, re.DOTALL).group()
                json_str = json_str.replace("'", '"')
                print_color(json_str, "yellow")
                action_choice_json = json.loads(json_str)
                action = list(action_choice_json.values())[0]
                print_color(action, "yellow")
                break
            except:
                print("LLM failed to return a valid json object. Output text: {}".format(action_choice_response))
                print("Retrying...")
                messages.append({"role": "assistant", "content": action_choice_response})
                messages.append({"role": "user", "content": summary_prompt_correction})
                continue
        
        if action is None:
            print("LLM failed to return a valid json object after {} attempts. Output text: \n{}".format(num_attempts, action_choice_response))
            print("Returning a random action idx...")

        return action

    def _create_prompt(self, action_candidates, obs, language_correction=None):
        system_prompt = system_prompts.system_prompt_behavior

        if language_correction is not None:
            system_prompt = system_prompts.system_prompt_behavior_human
        
        user_prompt = system_prompts.prompt_robot \
                    + system_prompts.prompt_task[self._task_name] \
                    + system_prompts.prompt_instruction \
                    + system_prompts.prompt_instruction_cot_combine_onedim

        obs_processed = self._process_obs(obs)
        obs_string = format_obs(obs_processed, system_prompts.template_obs[self._task_name], task=self._task_name)

        action_string = format_action(action_candidates)

        user_prompt = user_prompt + obs_string + action_string

        if language_correction is not None:
            language_prompt = self._process_language(language_correction)
            user_prompt = user_prompt + language_prompt

        return system_prompt, user_prompt 

class LLMAgent():
    """
    Basic universal LLM agent that do the conversation.
    """
    def __init__(self, llm_model="gpt-35-turbo", temperature=0.1, timeout=20):
        self._llm_model = llm_model
        self._temperature = temperature
        self._log_file = open("test.txt", "w")
        self._timeout = timeout
        
    def eval(self, text):

        system_prompt, user_prompt = self.create_prompt(text)
        print_color(system_prompt, "yellow")
        print_color(user_prompt, "yellow")

        self._log_file.write("\n\n\n")
        self._log_file.write("system prompt: {}\n".format(system_prompt))
        self._log_file.write("user prompt: {}\n".format(user_prompt))
        self._log_file.write("\n")

        llm_output = self.llm_call(system_prompt, user_prompt)

        self._log_file.write("Output: \n{}\n\n".format(llm_output))

        return llm_output

    
    def llm_call(self, system_prompt, user_prompt):
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        _, response = call_model(messages, 
                          model=self._llm_model, 
                          temperature=self._temperature, 
                          request_timeout=self._timeout + np.random.randint(-10, 10)
                          )
        
        print_color(response, "blue")
        
        return response
   
    def create_prompt(self):
        pass
    
class FeedbackSummaryAgent(LLMAgent):
    
    def create_prompt(self, text):
        system_prompt = human_feedback_prompts.system_prompt
        user_prompt = human_feedback_prompts.context + text
        return system_prompt, user_prompt
    
