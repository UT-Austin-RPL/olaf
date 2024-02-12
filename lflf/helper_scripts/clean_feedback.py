import re
import numpy as np


language_correction_path = "/home/huihanliu/LfLF_data/language_correction_short.npy"
language_correction = np.load(language_correction_path, allow_pickle=True).item()

for ep in language_correction:
    text_lst = language_correction[ep]
    for i in range(len(text_lst)):
        s = re.sub(r'Output:\n*', "", text_lst[i])
        text_lst[i] = s
    language_correction[ep] = text_lst
    print(language_correction[ep])
    
np.save("language_correction_short_cleaned", language_correction)