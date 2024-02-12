import h5py
from shutil import copyfile
import os
import numpy as np
import time
import threading
import queue

from lflf.utils.data_utils import select_obs_idx
from lflf.utils.llm_utils import *
from lflf.utils.random_utils import *
from lflf.models.critic import LLMCritic, LLMCriticReturnAction, LLMCriticEditAction, LLMCriticCombineOnedimAction
from lflf.scripts.relabeling_actions import RelabelTool, get_parser

import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Timeout - the operation took too long.")
timeout_duration = 20 * 60  # wait for 40 minutes
signal.signal(signal.SIGALRM, timeout_handler)

class RelabelToolParallel(RelabelTool):

    def __init__(self, args, curr_ep, time):
        
        self._curr_ep = curr_ep
        self._time = time
        
        super().__init__(args)

        self._curr_ep = curr_ep # in case it is overwritten by super().__init__()
        # To keep track of the current episode ep and timestep t
        self._ep_data_grp = self.f["data/{}".format(self._curr_ep)]

        # log dir
        os.makedirs(self._time, exist_ok=True) 
        self._log_file = open("{}/{}_result.txt".format(self._time, self._curr_ep), "w")

    def _setup_time(self):
        assert self._time is not None

    def _setup_llm(self, args):

        if self._mode == "return_action":
            self._llm = LLMCriticReturnAction(args, self._time, per_ep=self._curr_ep)
        elif self._mode == "edit_action":
            self._llm = LLMCriticEditAction(args, self._time, per_ep=self._curr_ep)
        elif self._mode == "combine_onedim_action":
            self._llm = LLMCriticCombineOnedimAction(args, self._time, per_ep=self._curr_ep)
        else:
            self._llm = LLMCritic(args, self._time, per_ep=self._curr_ep)    

    def _setup_dataset(self, args):   

        # use original dataset because no need to overwrite here
        original_dataset_path = os.path.expanduser(args.original_dataset)

        self.f = h5py.File(original_dataset_path, "r")

    def relabel_trajectory(self):

        start_time = time.time()

        assert self._curr_t == -1 # confirm it's been reset

        intv_labels = self._ep_data_grp["intv_labels"][()]
        actions = self._ep_data_grp["actions"][()]
        traj_len = len(actions)

        if (intv_labels != self._PRE_INTV).all():
            print_color("No pre-intervention region for episode {}. Skip.".format(self._curr_ep), "red")

            self._log_file.write("Current Episode: {}\n".format(self._curr_ep))
            self._log_file.write("No pre-intervention region for episode {}. Skip.".format(self._curr_ep))
            self._log_file.flush()
            return {"actions": actions, 
                "acc_count": self._sanity_check_count}

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
        
        end_time = time.time()
        elapsed_time = round(end_time - start_time, 1)

        self._log_file.write("Current Episode: {}\n".format(self._curr_ep))

        if self._sanity_check_count["all"] > 0:
            acc = self._sanity_check_count["correct"] / self._sanity_check_count["all"]
        else:
            acc = 0
        self._log_file.write("Overall Accuracy: {}\n".format(acc))

        self._log_file.write("Time taken: {} seconds\n".format(elapsed_time))
        self._log_file.write("\n")
        self._log_file.flush()

        return {"actions": actions, 
                "acc_count": self._sanity_check_count}


class WorkerClass:
    def __init__(self, args):
        self.args = args

        self.task_queue = queue.Queue()
        self.done_queue = queue.Queue()

        self.num_threads = args.num_threads

    # Function to be executed in parallel
    def worker(self):
        for func, args in iter(self.task_queue.get, 'STOP'):
            print(func, args)
            result = self.calculate(func, args)
            self.done_queue.put(result)

    # Function that performs the actual work
    def calculate(self, func, args):
        result = func(*args)
        return result

    # Function to be executed by each worker
    def do_work(self, args, curr_ep, time):
        relabel_tool = RelabelToolParallel(args, curr_ep, time)
        res = relabel_tool.relabel_trajectory()
        return {"ep": curr_ep, 
                "actions": res["actions"], 
                "acc_count": res["acc_count"]}
    
    def start(self):

        args = self.args
        assert args.original_dataset != args.relabeled_dataset
        copyfile(args.original_dataset, args.relabeled_dataset)

        original_dataset_path = os.path.expanduser(args.original_dataset)
        f_original = h5py.File(original_dataset_path, "r+")
        demos = list(f_original["data"].keys())
        inds = np.argsort([int(elem[5:]) for elem in demos])
        self.demos = [demos[i] for i in inds]
        f_original.close()

        curr_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime(time.time()))
        os.makedirs(curr_time, exist_ok=True)   
        
        for ep in self.demos:
            # Put tasks into the queue in the format (function to execute, arguments)
            self.task_queue.put((self.do_work, (args, ep, curr_time)))

        # Start worker threads
        for i in range(self.num_threads):
            threading.Thread(target=self.worker).start()

        actions_dict = {}

        acc_count = {"correct": 0, "all": 0}

        for i in range(len(self.demos)):
            try:
                signal.alarm(timeout_duration)
                ep_dict = self.done_queue.get()
                signal.alarm(0)
            except TimeoutError as e:
                print_color("Finished with progress: {}/{}".format(len(actions_dict), len(self.demos)), "red")
                break
            finally:
                signal.alarm(0)
            
            actions_dict[ep_dict["ep"]] = ep_dict["actions"]
            print("Finish episode {}".format(ep_dict["ep"]))
            print_color("Progress: {}/{}".format(len(actions_dict), len(self.demos)), "green")

            acc_count["correct"] += ep_dict["acc_count"]["correct"]
            acc_count["all"] += ep_dict["acc_count"]["all"]
        
            np.save("parallel_actions_dict_buffer_{}".format(curr_time), actions_dict)
            np.save("parallel_acc_count_buffer_{}".format(curr_time), acc_count)
        
        out_dataset_path = os.path.expanduser(args.relabeled_dataset)
        f_out = h5py.File(out_dataset_path, "r+")     

        print_color("\nWriting actions to dataset...\n", "yellow")

        for ep in self.demos:
            ep_data_grp = f_out["data/{}".format(ep)]
            # relabel actions for trajectory
            if ep not in actions_dict or actions_dict[ep] is None:
                print_color("No actions for episode {}. Skip.".format(ep), "red")
                continue
            
            new_actions = actions_dict[ep]
            del ep_data_grp["actions"] 
            ep_data_grp.create_dataset("actions", data=new_actions)

        # Stop the worker threads
        for i in range(self.num_threads):
            self.task_queue.put('STOP')

        acc = acc_count["correct"] / acc_count["all"] if acc_count["all"] > 0 else 0
        print_color("Overall Accuracy: {}".format(acc), "green")
        
        print("Done.")
        f_out.close()

def main(args):
    worker_class = WorkerClass(args)
    worker_class.start()
    
    
if __name__ == "__main__":

    parser = get_parser()
    parser.add_argument('--num_threads', type=int, default=10)

    args = parser.parse_args()
    main(args) 
    
