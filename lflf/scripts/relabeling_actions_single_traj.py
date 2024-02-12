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
from lflf.models.critic import LLMCritic, LLMCriticReturnAction, LLMCriticEditAction
from lflf.scripts.relabeling_actions import RelabelTool, get_parser
from lflf.scripts.relabeling_actions_parallel import RelabelToolParallel
import signal

def timeout_handler(signum, frame):
    raise TimeoutError("Timeout - the operation took too long.")
timeout_duration = 20 * 60  # wait for 20 minutes
signal.signal(signal.SIGALRM, timeout_handler)


class WorkerClassSingle:
    def __init__(self, args):
        self.args = args

        self.task_queue = queue.Queue()
        self.done_queue = queue.Queue()

        self.num_threads = 1

        self.ep = args.ep

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

        self.task_queue.put((self.do_work, (args, self.ep, curr_time)))

        # Only one thread
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
        
        out_dataset_path = os.path.expanduser(args.relabeled_dataset)
        f_out = h5py.File(out_dataset_path, "r+")     

        print_color("\nWriting actions to dataset...\n", "yellow")

        # Stop the worker threads
        for i in range(self.num_threads):
            self.task_queue.put('STOP')

        acc = acc_count["correct"] / acc_count["all"] if acc_count["all"] > 0 else 0
        print_color("Overall Accuracy: {}".format(acc), "green")
        
        print("Done.")
        f_out.close()

def main(args):
    worker_class = WorkerClassSingle(args)
    worker_class.start()
    
    
if __name__ == "__main__":

    parser = get_parser()
    parser.add_argument('--ep', type=str)

    args = parser.parse_args()
    main(args) 
    
