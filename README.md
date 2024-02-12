# Olaf

## Interactive Robot Learning from Verbal Correction

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
