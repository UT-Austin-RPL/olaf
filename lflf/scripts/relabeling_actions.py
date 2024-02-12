import h5py
from shutil import copyfile
import os
import numpy as np
import time

from lflf.utils.data_utils import *
from lflf.utils.llm_utils import *
from lflf.utils.random_utils import *
from lflf.models.critic import LLMCritic, LLMCriticReturnAction, LLMCriticEditAction, LLMCriticCombineOnedimAction

class RelabelTool():

    def __init__(self, args):

        self._mode = args.mode
        
        self._setup_time()
        self._setup_dataset(args)
        self._setup_llm(args)

        self._num_actions = args.num_actions
        self._candidate_strategy = args.candidate_strategy
        
        # Creating relabeled dataset
        assert args.original_dataset != args.relabeled_dataset

        # To keep track of the current episode ep and timestep t
        self._curr_ep = None
        self._ep_data_grp = None
        self._curr_t = -1

        self._PRE_INTV = -10
        self._INTV = 1

        # for binary testing, correct action is always Action 1. Check the overall accuracy.
        self._sanity_check_count = {"all": 0, "correct": 0}

        self._language_correction_path = args.language_correction
        if self._language_correction_path is not None:
            self._language_correction = np.load(self._language_correction_path, allow_pickle=True).item()
        else:
            self._language_correction = None

        self._single_relabeling = args.single_relabeling
        self._llm_hardcode_scale = args.llm_hardcode_scale

    def _setup_time(self):
        self._time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        os.makedirs(self._time, exist_ok=True)   

    def _setup_dataset(self, args):

        copyfile(args.original_dataset, args.relabeled_dataset)
        # use out_dataset_path to specify overwriting the relabeled dataset
        out_dataset_path = os.path.expanduser(args.relabeled_dataset)

        self.f = h5py.File(out_dataset_path, "r+")
        demos = list(self.f["data"].keys())
        inds = np.argsort([int(elem[5:]) for elem in demos])
        self.demos = [demos[i] for i in inds]

        # create log file
        self._log_file = open("{}/relabeling_log.txt".format(self._time), "w")

    def _setup_llm(self, args):

        if self._mode == "return_action":
            self._llm = LLMCriticReturnAction(args, self._time)
        elif self._mode == "edit_action":
            self._llm = LLMCriticEditAction(args, self._time)
        elif self._mode == "combine_onedim_action":
            self._llm = LLMCriticCombineOnedimAction(args, self._time)
        else:
            self._llm = LLMCritic(args, self._time)    

    def start_relabeling(self):

        for ep in self.demos:
            self._curr_ep = ep
            self._ep_data_grp = self.f["data/{}".format(self._curr_ep)]
            start_time = time.time()
            self.relabel_trajectory()
            end_time = time.time()
            elapsed_time = round(end_time - start_time, 1)

            if elapsed_time > 10:
                # Actually relabeling
                print("Current Episode: ", self._curr_ep)
                print("Current Accuracy: ", self._sanity_check_count["correct"] / self._sanity_check_count["all"])
                print("Time taken: ", elapsed_time, "seconds")

                self._log_file.write("Current Episode: {}\n".format(self._curr_ep))

                if self._sanity_check_count["all"] > 0:
                    acc = self._sanity_check_count["correct"] / self._sanity_check_count["all"]
                else:
                    acc = 0
                self._log_file.write("Overall Accuracy: {}\n".format(acc))

                self._log_file.write("Time taken: {} seconds\n".format(elapsed_time))
                self._log_file.write("\n")

        print("Done.")
        self.f.close()

    def relabel_trajectory(self):

        assert self._curr_t == -1 # confirm it's been reset

        intv_labels = self._ep_data_grp["intv_labels"][()]
        actions = self._ep_data_grp["actions"][()]
        traj_len = len(actions)

        if (intv_labels != self._PRE_INTV).all():
            print_color("No pre-intervention region for episode {}. Skip.".format(self._curr_ep), "red")
            return

        for i in range(traj_len - 1):
            self._curr_t = i

            if self._single_relabeling:
                # Only process single timestep before intervention
                if not (intv_labels[i] == self._PRE_INTV and intv_labels[i+1] == self._INTV):
                    continue               
            else:
                # Only process pre-intervention region
                if intv_labels[i] != self._PRE_INTV:
                    continue

            relabeled_action = self.relabel_state()

            # Relabel the original actions
            actions[i] = relabeled_action

        # relabel actions for trajectory
        del self._ep_data_grp["actions"] 
        self._ep_data_grp.create_dataset("actions", data=actions)

        # reset
        self._curr_t = -1

    def relabel_state(self):

        # no action generation and selection, just to test baselines
        if self._mode == "heuristics":
            return self._generate_actions_heuristic()
        elif self._mode == "human_gt":
            return self._generate_action_human()
        elif self._mode == "baseline":
            return self._generate_action_baseline()
        elif self._mode == "return_action":
            return self._generate_return_action()
        elif self._mode == "edit_action":
            return self._generate_edit_action()  
        elif self._mode == "llm_hardcode":
            return self._get_llm_hardcode_actions()

        # For each action, use existing policy to sample candidate replacement actions
        action_candidates, true_action_idx = self.generate_actions()

        print_color("Current Episode: {}, current timestep: {}".format(self._curr_ep, self._curr_t), "green")
        print_color("True action idx: {}".format(true_action_idx), "green")
        print_color("True action candidate: {}".format(action_candidates[true_action_idx]), "green")

        if self._mode == "combine_onedim_action":
            return self._generate_combine_ondim_action(action_candidates)

        # Get relabeled actions from LLM for each action
        relabeled_action, relabeled_action_idx = self.select_one_action(action_candidates)

        if relabeled_action_idx is not None and true_action_idx is not None:
            self._sanity_check_count["all"] += 1
            self._sanity_check_count["correct"] += relabeled_action_idx == true_action_idx
            self._log_file.write("Episode: {}, timestep: {} \nReturned answer: {} True answer: {}\nSuccess: {}\n\n".format(self._curr_ep, self._curr_t, 
                                                                                                                           relabeled_action_idx, true_action_idx, 
                                                                                                                           int(relabeled_action_idx == true_action_idx)))
            self._log_file.flush()

        return relabeled_action

    def generate_actions(self):
        if self._candidate_strategy == "policy":
            raise NotImplementedError # TODO: for now
            return self._get_policy_actions()

        elif self._candidate_strategy == "binary":
            return self._get_binary_actions(), 1

        elif self._candidate_strategy == "onedim":
            return self._get_onedim_actions(), 0 # random

        elif self._candidate_strategy == "mix_binary_onedim":
            return self._get_mix_binary_onedim_actions()
        
        elif self._candidate_strategy == "all_mixed":
            return self._get_all_mixed_actions(), 0 # random
            
        else:
            raise NotImplementedError
        
    def _get_policy_actions(self):
        # TODO: assume no history first
        obs = self._ep_data_grp["obs"]
        action_candidates = []
        obs_i = select_obs_idx(obs, self._curr_t)
        action_candidates = self._action_policy.generate_actions(obs_i, self._num_actions)
        return action_candidates

    def _get_binary_actions(self):
        original_actions = self._ep_data_grp["actions"][self._curr_t]
        relabeled_actions = self._ep_data_grp["actions_relabeled"][self._curr_t]
        return [original_actions, relabeled_actions]

    def _get_onedim_actions(self):
        nearest_intv_t = self._curr_t
        for i in range(self._curr_t, len(self._ep_data_grp["actions"][()])):
            if self._ep_data_grp["intv_labels"][i] == 1: # is intervention
                nearest_intv_t = i
                break
        # set the gripper value to be that of the nearest intervention
        original_actions_grip = self._ep_data_grp["actions"][nearest_intv_t][-1]
        actions_candidates = [np.array(a + [original_actions_grip]) for a in onedim_actions]
        
        return actions_candidates
    
    def _get_mix_binary_onedim_actions(self):
        binary = self._get_binary_actions()
        onedim = self._get_onedim_actions()

        old_good_index = 1
        good_action = binary[old_good_index]
        mixed = binary + onedim
        # random shuffle
        np.random.shuffle(mixed)
        new_good_index = find_index(mixed, good_action)

        return mixed, new_good_index

    def _get_all_mixed_actions(self):
        original_actions = self._ep_data_grp["original"][self._curr_t]
        modified_actions = self._ep_data_grp["modified"][self._curr_t]
        onedim_actions = self._ep_data_grp["onedim"][self._curr_t]
        gpt_actions = self._ep_data_grp["gpt"][self._curr_t]
        direct_modify_actions = self._ep_data_grp["direct_modify"][self._curr_t]
        
        return [original_actions, modified_actions, onedim_actions, gpt_actions, direct_modify_actions]

    def _get_llm_hardcode_actions(self):

        original_action = self._ep_data_grp["actions"][()][self._curr_t]

        assert self._language_correction is not None
        language_correction = self._language_correction[self._curr_ep][self._curr_t]
        
        language_correction = language_correction.replace('left bin', '__TEMP__')
        language_correction = language_correction.replace('right bin', '__TEMP__')
                
        lang_dict = {
            "left": [0,-0.2,0,0,0,0],
            "right": [0,0.2,0,0,0,0],
            "forward": [0.2,0,0,0,0,0],
            "backward": [-0.2,0,0,0,0,0],
            "up": [0,0,0.2,0,0,0],
            "down": [0,0,-0.2,0,0,0],
            "lower": [0,0,-0.2,0,0,0],
            "counter": [0,0,0,0,0,0.2],
        }
        
        onedim_action = None
        
        for k in lang_dict.keys():
            if k in language_correction:
                onedim_action = lang_dict[k]
            elif "clockwise" in language_correction:
                onedim_action = [0,0,0,0,0,-0.2]  
        
        if onedim_action is None:
            onedim_action = [0,0,0,0,0,0]  
            
        if self._llm_hardcode_scale > 0:
            onedim_action = np.array(onedim_action)
            onedim_action *= self._llm_hardcode_scale
            onedim_action = list(onedim_action)
            print(onedim_action)
            
        # grip
        if "open" in language_correction:
            onedim_action = onedim_action + [-1.]
        elif "close" in language_correction:
            onedim_action = onedim_action + [1.]
        else:     
            nearest_intv_t = self._curr_t
            for i in range(self._curr_t, len(self._ep_data_grp["actions"][()])):
                if self._ep_data_grp["intv_labels"][i] == 1: # is intervention
                    nearest_intv_t = i
                    break
            # set the gripper value to be that of the nearest intervention
            original_actions_grip = self._ep_data_grp["actions"][nearest_intv_t][-1]
            onedim_action = onedim_action + [original_actions_grip] 
        
        modified_action = onedim_action + original_action 
        
        return modified_action 
            
    def select_one_action(self, action_candidates):

        obs = self._ep_data_grp["obs"]
        obs_i = select_obs_idx(obs, self._curr_t)

        if self._candidate_strategy == "binary":
            # hardcode for binary testing: if action is the same, skip accuracy check
            if format_value(action_candidates[0]) == format_value(action_candidates[1]):
                print_color("Same action. Skip accuracy check.", "red")
                return action_candidates[0], None
            
        
        if self._language_correction is not None:
            language_correction = self._language_correction[self._curr_ep][self._curr_t]
            if language_correction == "":
                language_correction = None
        else:
            language_correction = None
        
        selected_action_idx = self._llm.eval(action_candidates, obs_i, language_correction=language_correction)
        selected_action = action_candidates[selected_action_idx]

        return selected_action, selected_action_idx
    
    def _generate_actions_heuristic(self):
        obs = self._ep_data_grp["obs"]
        obs_i = select_obs_idx(obs, self._curr_t)
        object = obs_i["object"]
        # TODO: customized to each environment

    def _generate_action_human(self):
        """ Ground truth human relabeling """
        human_gt = self._ep_data_grp["actions_relabeled"][self._curr_t]
        return human_gt
    
    def _generate_action_baseline(self):
        """ Baseline (original policy action) relabeling """
        baseline_action = self._ep_data_grp["actions"][self._curr_t]
        return baseline_action

    def _generate_edit_action(self):
        try:
            obs = self._ep_data_grp["obs"]
            obs_i = select_obs_idx(obs, self._curr_t)

            if self._language_correction is not None:
                language_correction = self._language_correction[self._curr_ep][self._curr_t]
                if language_correction == "":
                    language_correction = None
            else:
                language_correction = None

            policy_action = self._ep_data_grp["actions"][self._curr_t]

            selected_action = self._llm.eval([policy_action], obs_i, language_correction=language_correction)
            self._log_file.write("Episode: {}, timestep: {} \nReturned action: {}\n\n".format(self._curr_ep, 
                                                                                              self._curr_t, 
                                                                                              selected_action))
            self._log_file.flush()
            
            if selected_action is None:
                selected_action = self._ep_data_grp["actions"][self._curr_t] # original action
                self._log_file.write("Episode: {}, timestep: {} \nReturned action: None\n\n".format(self._curr_ep, 
                                                                                                  self._curr_t))
                self._log_file.flush()
            
        except:
            return self._ep_data_grp["actions"][self._curr_t]
        
        return selected_action
    
    def _generate_combine_ondim_action(self, action_candidates):
        if True: #try:
            obs = self._ep_data_grp["obs"]
            obs_i = select_obs_idx(obs, self._curr_t)

            if self._language_correction is not None:
                language_correction = self._language_correction[self._curr_ep][self._curr_t]
                if language_correction == "":
                    language_correction = None
            else:
                language_correction = None

            selected_action = self._llm.eval(action_candidates, obs_i, language_correction=language_correction)
            self._log_file.write("Episode: {}, timestep: {} \nReturned action: {}\n\n".format(self._curr_ep, 
                                                                                              self._curr_t, 
                                                                                              selected_action))
            self._log_file.flush()
            
            if selected_action is None:
                selected_action = self._ep_data_grp["actions"][self._curr_t] # original action
                self._log_file.write("Episode: {}, timestep: {} \nReturned action: None\n\n".format(self._curr_ep, 
                                                                                                  self._curr_t))
                self._log_file.flush()
            
        # except:
        #     return self._ep_data_grp["actions"][self._curr_t]
        
        return selected_action        

    def _generate_return_action(self):
        try:
            obs = self._ep_data_grp["obs"]
            obs_i = select_obs_idx(obs, self._curr_t)

            if self._language_correction is not None:
                language_correction = self._language_correction[self._curr_ep][self._curr_t]
                if language_correction == "":
                    language_correction = None
            else:
                language_correction = None

            selected_action = self._llm.eval(None, obs_i, language_correction=language_correction)
            self._log_file.write("Episode: {}, timestep: {} \nReturned action: {}\n\n".format(self._curr_ep, 
                                                                                              self._curr_t, 
                                                                                              selected_action))
            self._log_file.flush()
            
            if selected_action is None:
                selected_action = self._ep_data_grp["actions"][self._curr_t] # original action
                self._log_file.write("Episode: {}, timestep: {} \nReturned action: None\n\n".format(self._curr_ep, 
                                                                                                  self._curr_t))
                self._log_file.flush()
            
        except:
            return self._ep_data_grp["actions"][self._curr_t]
        
        return selected_action

def get_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--original_dataset', type=str, default="/home/huihanliu/LfLF_data/test.hdf5")
    parser.add_argument('--relabeled_dataset', type=str, default="/home/huihanliu/LfLF_data/test_relabeled.hdf5")
    parser.add_argument('--mode', type=str, default="llm_critic", choices=["llm_critic", "human_gt", "baseline", "heuristics", "return_action", "edit_action", "combine_onedim_action", "llm_hardcode"])
    parser.add_argument('--action_policy', type=str, default="nn", choices=["nn"])
    parser.add_argument('--policy', type=str, default=None)    
    parser.add_argument('--num_actions', type=int, default=5)
    parser.add_argument('--temperature', type=float, default=0.5)
    parser.add_argument('--candidate_strategy', type=str, default="policy", choices=["policy", "binary", "onedim", "mix_binary_onedim", "all_mixed"])
    parser.add_argument('--have_low_level_info', type=int, default=1)
    parser.add_argument('--gpt_model', type=str, default="gpt-35-turbo", choices=["gpt-35-turbo", "gpt-4", "gpt-4-32k"])
    parser.add_argument('--language_correction', type=str, default=None)
    parser.add_argument('--task_name', type=str, choices=["square", "can", "coffee", "threading", "toolhang"])
    parser.add_argument('--timeout', type=int, default=60)
    parser.add_argument('--single_relabeling', action='store_true')
    parser.add_argument('--llm_hardcode_scale', default=-1, type=int)
    
    return parser

if __name__ == "__main__":

    args = get_parser().parse_args()

    relabel_tool = RelabelTool(args)
    relabel_tool.start_relabeling()
