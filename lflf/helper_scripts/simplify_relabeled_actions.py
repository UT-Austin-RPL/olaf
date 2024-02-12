import h5py
import numpy as np
import random
from shutil import copyfile
import os

PRE_INTV = 20

data_path = "/home/huihanliu/round01_human_relabeled.hdf5"
res_data_path = "/home/huihanliu/round01_human_relabeled_simplified_noise.hdf5"

def obtain_data(data_path):
    f = h5py.File(data_path, "r+")
    # Obtain the list of trajectory keys
    demos = list(f["data"].keys())
    inds = np.argsort([int(elem[5:]) for elem in demos])
    demos = [demos[i] for i in inds]
    return f, demos

def process_action(action):
    replaced_action = action.copy()
    replaced_action[:5] = 0
    max_idx = np.argmax(abs(action[:5]))
    replaced_action[max_idx] = action[max_idx]
    
    for i in range(5):
        if max_idx != i:
            replaced_action[i] += np.random.normal(loc=0.0, scale=0.001)
    
    print(replaced_action)
    
    return replaced_action


copyfile(data_path, res_data_path)
out_dataset_path = os.path.expanduser(res_data_path)

f, demos = obtain_data(out_dataset_path)
for ep in demos:
    data_ep = f["data"][ep]
    intv_labels = data_ep["intv_labels"][()]
    actions = data_ep["actions"][()]
    traj_len = len(actions)

    for i in range(traj_len):
        # Only process pre-intervention region
        if intv_labels[i] != PRE_INTV:
            continue
        
        actions[i] = process_action(actions[i])
        
    del data_ep["actions"] 
    data_ep.create_dataset("actions", data=actions)
