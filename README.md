# LfLF

## Learning from Language Feedback

<br>

### Running it locally

Setup:
```
conda create -n lflf python=3.8
cd LfLF
pip install -e .
pip install -r requirements.txt
```


#### downloading dataset:

```
python lflf/helper_scripts/download_file.py 
```

#### parallel relabeling:

change ```--mode``` to be one of {```edit_action```, ```return_action```, ```llm_critic```}

```
python lflf/scripts/relabeling_actions_parallel.py --original_dataset data/round01_square.hdf5 --relabeled_dataset data/round01_square_edit_action_long.hdf5 --mode edit_action --candidate_strategy onedim --num_actions 8 --gpt_model gpt-35-turbo --language_correction data/language_correction_long.npy --temperature 0.5 --num_threads 100
```

#### non-parallel relabeling:

Specify the trajectory with ```--ep```.

change ```--mode``` to be one of {```edit_action```, ```return_action```, ```llm_critic```}

```
python lflf/scripts/relabeling_actions_single_traj.py --original_dataset data/round01_square.hdf5 --relabeled_dataset data/round01_square_edit_action_long.hdf5 --mode edit_action --candidate_strategy onedim --num_actions 8 --gpt_model gpt-35-turbo --language_correction data/language_correction_long.npy --temperature 0.5 --ep demo_84
```




### If running on Huihan's machine, here's are the exact commands to run: 


#### parallel relabeling:

onedim action:
```
python lflf/scripts/relabeling_actions_parallel.py --original_dataset /home/huihanliu/LfLF_data/round01_relabeled_combined_ll.hdf5 --relabeled_dataset /home/huihanliu/LfLF_data/round01_onedim_gpt4.hdf5 --mode llm --action_policy nn --candidate_strategy onedim --num_actions 8 --gpt_model gpt-4-32k --language_correction /home/huihanliu/LfLF_data/language_correction_dict.npy --temperature 0.5 --num_thread 100
```

gpt directly output action:
```
python lflf/scripts/relabeling_actions_parallel.py --original_dataset /home/huihanliu/LfLF_data/round01_relabeled_combined_ll.hdf5 --relabeled_dataset /home/huihanliu/LfLF_data/round01_return_action_gpt4.hdf5 --mode llm --action_policy nn --candidate_strategy onedim --num_actions 8 --gpt_model gpt-4-32k --language_correction /home/huihanliu/LfLF_data/language_correction_dict.npy --temperature 0.5 --return_action --num_thread 100
```

#### non-parallel (to visualize outputs for one single trajectory):
Specify the trajectory with ```--ep```.

onedim action:
```
python lflf/scripts/relabeling_actions_single_traj.py --original_dataset /home/huihanliu/LfLF_data/round01_relabeled_combined_ll.hdf5 --relabeled_dataset /home/huihanliu/LfLF_data/test_one_demo.hdf5 --mode llm --action_policy nn --candidate_strategy onedim --num_actions 8 --gpt_model gpt-4-32k --language_correction /home/huihanliu/LfLF_data/language_correction_dict.npy --ep demo_137
```

gpt directly output action:
```
python lflf/scripts/relabeling_actions_single_traj.py --original_dataset /home/huihanliu/LfLF_data/round01_relabeled_combined_ll.hdf5 --relabeled_dataset /home/huihanliu/LfLF_data/round01_return_action_gpt4.hdf5 --mode llm --action_policy nn --candidate_strategy onedim --num_actions 8 --gpt_model gpt-4-32k --language_correction /home/huihanliu/LfLF_data/language_correction_dict.npy --temperature 0.5  --ep demo_137 --return_action 
```

You can visualize the existing results in ```/home/huihanliu/LfLF/relabel_outputs``` including prompts and gpt responses.
