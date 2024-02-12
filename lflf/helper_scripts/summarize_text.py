import h5py
from shutil import copyfile
import os
import numpy as np
import time
import re

from lflf.utils.data_utils import *
from lflf.utils.llm_utils import *
from lflf.utils.random_utils import *
from lflf.models.critic import FeedbackSummaryAgent

def get_parser():
    from argparse import ArgumentParser
    parser = ArgumentParser()
    parser.add_argument('--original_npy', type=str)
    return parser

if __name__ == "__main__":

    args = get_parser().parse_args()

    language_correction = np.load(args.original_npy, allow_pickle=True).item()

    critic = FeedbackSummaryAgent(llm_model="gpt-4")

    for ep in language_correction:
        text_lst = language_correction[ep]
        unique_text = list(set(text_lst))
        
        for text in unique_text:
            if len(text) == 0:
                continue
            response = critic.eval(text)
            print_color(response, "green")
            
            for i in range(len(text_lst)):
                if text_lst[i] == text:
                    text_lst[i] = response
        
        language_correction[ep] = text_lst
        print(language_correction[ep])
        print()
        print()

    np.save("{}_short".format(args.original_npy[:-5]), language_correction)
    print("Start cleaning")

    for ep in language_correction:
        text_lst = language_correction[ep]
        for i in range(len(text_lst)):
            s = re.sub(r'Output:\n*', "", text_lst[i])
            text_lst[i] = s
        language_correction[ep] = text_lst
        print(language_correction[ep])
        print()
        print()

    np.save("{}_short_cleaned".format(args.original_npy[:-5]), language_correction)
  

