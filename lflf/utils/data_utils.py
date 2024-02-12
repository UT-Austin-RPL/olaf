import numpy as np

def select_obs_idx(obs, idx):
    d = dict()
    for key in obs:
        d[key] = obs[key][idx]
    return d

def find_index(lst, item):
    for i, arr in enumerate(lst):
        if np.array_equal(arr, item):
            return i
    raise ValueError("Item not found in the list")
