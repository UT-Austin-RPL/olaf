import gdown, os
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)
gdown.download('https://drive.google.com/uc?export=download&id=1W70HAOUwlPyjOEGxakFkaLCwhgRCZ12b', os.path.join(data_dir,'round01_square.hdf5') , quiet=False)
gdown.download('https://drive.google.com/uc?export=download&id=1r9vFr3g6s1Xccnqc9Qi6Gux2tZQgxAbv', os.path.join(data_dir,'language_correction_long.npy'), quiet=False)
gdown.download('https://drive.google.com/uc?export=download&id=1Dimnk2u-4k28NXfWvwM3z522_wXFV1RJ', os.path.join(data_dir,'language_correction_short.npy'), quiet=False)
