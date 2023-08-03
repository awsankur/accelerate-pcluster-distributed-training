import os
import time
import glob
import torch
from torchvision import transforms
from torch.utils.data import DataLoader
from tifffile import imread

import multiprocessing as mp


class Dataset(torch.utils.data.Dataset):
    #'Characterizes a dataset for PyTorch'
    def __init__(self, img_dir):
    
        #'Initialization'
        self.img_dir = img_dir
        self.files = glob.glob(img_dir + '/**/*.tiff', recursive=True)
     
    def __len__(self):
        # 'Denotes the total number of samples'
        return len(self.files)
        
    def __getitem__(self, index):
        # Select sample
        image_np = imread(self.files[index])

        #Return a Torch tensor
        image_np = image_np.astype(float)
        image_np = torch.from_numpy(image_np).permute(2, 0, 1)

        transform = transforms.Compose([
                transforms.Resize(size=(220,224)),
                transforms.CenterCrop(220)
                ])

        
        image = transform(image_np)

        return image, index

img_dir = '/data/data/DeepPhenotype_PBMC_ImageSet_YSeverin/Training/'
train_dataset = Dataset(img_dir)

number_of_cpus = mp.cpu_count()
number_of_gpus = torch.cuda.device_count()

max_num_workers = int(number_of_cpus/number_of_gpus)

print('Max num workers = {}'.format(max_num_workers))

num_epochs = 3
for num_workers in range(0,max_num_workers+2,2):
    train_loader = DataLoader(train_dataset,shuffle=True,num_workers=num_workers,batch_size=32,pin_memory=True)
    start = time.time()

    for epoch in range(num_epochs):
        for i, data in enumerate(train_loader, 0):
            pass
    end = time.time()
    time_taken_secs = end - start
    avg_time_per_epoch_secs = time_taken_secs/num_epochs 
    print("Avg time per epoch:{} second, num_workers={}".format(avg_time_per_epoch_secs, num_workers))


