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
    parser.add_argument('--data_path_original', type=str, default=None)
    parser.add_argument('--data_path_modified', type=str, default=None)
    parser.add_argument('--data_path_onedim', type=str, default=None)
    parser.add_argument('--data_path_gpt', type=str, default=None)
    parser.add_argument('--data_path_direct_modify', type=str, default=None)
    parser.add_argument('--data_path_output', type=str, default=None) 
    return parser

def create_action(input_data_ep, output_data_ep, name):
    actions = input_data_ep["actions"][()]
    output_data_ep.create_dataset(name, data=actions)

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
    data_path_modified = args.data_path_modified
    data_path_onedim = args.data_path_onedim
    data_path_gpt = args.data_path_gpt
    data_path_direct_modify = args.data_path_direct_modify

    # output directory
    data_path_output = args.data_path_output
    copyfile(data_path_original, data_path_output)

    # obtaining data
    f_output, demos = obtain_data(data_path_output)
    
    f_original, _ = obtain_data(data_path_original)
    f_modified, _ = obtain_data(data_path_modified)
    f_onedim, _ = obtain_data(data_path_onedim)
    f_gpt, _ = obtain_data(data_path_gpt)
    f_direct_modify, _ = obtain_data(data_path_direct_modify)
    
    for ep in demos:
        data_ep = f_output["data"][ep]
        intv_labels = data_ep["intv_labels"][()]
        actions = data_ep["actions"][()]
        traj_len = len(actions)
        
        data_ep_original = f_original["data"][ep]
        data_ep_modified = f_modified["data"][ep]
        data_ep_onedim = f_onedim["data"][ep]
        data_ep_gpt = f_gpt["data"][ep]            
        data_ep_direct_modify = f_direct_modify["data"][ep]
        
        create_action(input_data_ep=data_ep_original, output_data_ep=data_ep, name="original")
        create_action(input_data_ep=data_ep_modified, output_data_ep=data_ep, name="modified")
        create_action(input_data_ep=data_ep_onedim, output_data_ep=data_ep, name="onedim")
        create_action(input_data_ep=data_ep_gpt, output_data_ep=data_ep, name="gpt")
        create_action(input_data_ep=data_ep_direct_modify, output_data_ep=data_ep, name="direct_modify")