import h5py
import numpy as np
import random
from shutil import copyfile
import os
from lflf.utils.llm_utils import *

PRE_INTV = -10

def get_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--data_path_original', type=str)
    parser.add_argument('--data_path_relabeled', type=str)
    parser.add_argument('--data_path_output', type=str)
    parser.add_argument('--scale', type=float, default=1) # whether to scale one-dim action
    return parser

if __name__ == "__main__":

    args = get_parser().parse_args()

    def obtain_data(data_path):
        f = h5py.File(data_path, "r+")
        # Obtain the list of trajectory keys
        demos = list(f["data"].keys())
        inds = np.argsort([int(elem[5:]) for elem in demos])
        demos = [demos[i] for i in inds]
        return f, demos
    
    data_path_original = args.data_path_original
    data_path_relabeled = args.data_path_relabeled
    data_path_output = args.data_path_output

    copyfile(data_path_original, data_path_output)

    f_output, demos = obtain_data(data_path_output)
    f_original, _ = obtain_data(data_path_original)
    f_relabeled, _ = obtain_data(data_path_relabeled)
    
    print("f_output: ", f_output)
    print("f_original: ", f_original)
    print("f_relabeled: ", f_relabeled)

    for ep in demos:
        data_ep = f_output["data"][ep]
        intv_labels = data_ep["intv_labels"][()]
        actions = data_ep["actions"][()]
        traj_len = len(actions)

        assert len(f_original["data"][ep]["actions"][()]) == len(f_relabeled["data"][ep]["actions"][()])

        for i in range(traj_len):
            # Only process pre-intervention region
            if intv_labels[i] != PRE_INTV:
                continue
            
            original_action = f_original["data"][ep]["actions"][i]
            relabeled_action = f_relabeled["data"][ep]["actions"][i]
            
            relabeled_action_gripper = relabeled_action[-1] 

            original_no_gripper = original_action[:-1]
            relabeled_no_gripper = relabeled_action[:-1]
            
            print(onedim_actions)
            print(relabeled_no_gripper)
            assert list(relabeled_no_gripper) in onedim_actions # from llm_utils
            relabeled_no_gripper_scaled = relabeled_no_gripper * args.scale
            action_no_gripper = original_no_gripper + relabeled_no_gripper_scaled
            action_no_gripper = np.clip(action_no_gripper, -1, 1)
            actions[i] = np.append(action_no_gripper, relabeled_action_gripper)
            
            print()
            print("original:  ", original_no_gripper.round(2))
            print("relabeled: ", relabeled_no_gripper_scaled.round(2))
            print("combined:  ", actions[i].round(2))
            print()

        print(ep, (actions == data_ep["actions"][()]).all())

        del data_ep["actions"] 
        data_ep.create_dataset("actions", data=actions)
