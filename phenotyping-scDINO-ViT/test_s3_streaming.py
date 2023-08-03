import torch
from torch.utils.data import IterableDataset
from awsio.python.lib.io.s3.s3dataset import S3Dataset

from PIL import Image
import io
import numpy as np
from torchvision import transforms
from tifffile import imread

class S3ImageSet(S3Dataset):
    def __init__(self, urls, transform=None):
        super().__init__(urls)
        self.transform = transform

    def __getitem__(self, idx):

        img_name, img = super(S3ImageSet, self).__getitem__(idx)
        
        img_tmp = io.BytesIO(img)

        #print(img_tmp)

        img = Image.open(io.BytesIO(img))

        print(img_name)
        print(img)

        #path, target = self.samples[idx]

        #image_np= imread(img_name)

        #img_name, img = super(S3ImageSet, self).__getitem__(idx)
        # Convert bytes object to image
        #img = Image.open(io.BytesIO(img)).convert('RGB')
        
        # Apply preprocessing functions on data
        if self.transform is not None:
            img = self.transform(img)
        return img, idx


# Example Torchvision transforms to apply on data    
preproc = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    transforms.Resize((100, 100))
])

train_dataset = S3ImageSet(["s3://pcluster-ml-workshop/DeepPhenotype_PBMC_ImageSet_YSeverin/Training"], transform=preproc)

train_loader = torch.utils.data.DataLoader(train_dataset, num_workers=4, batch_size=32)

for epoch in range(1):
    for i, data in enumerate(train_loader, 0):
        import pdb;pdb.set_trace()
        #pass



# TORCHDATA
# from torchdata.datapipes.iter import IterableWrapper, S3FileLister, S3FileLoader

# s3_prefixes = IterableWrapper(['s3://pcluster-ml-workshop/DeepPhenotype_PBMC_ImageSet_YSeverin/'])

# dp_s3_urls = S3FileLister(s3_prefixes,request_timeout_ms=100,region='us-west-2')

# dp_s3_files = S3FileLoader(dp_s3_urls)
# for url, fd in dp_s3_files: # Start loading data
#     data = fd.read()
#     import pdb;pdb.set_trace()

# #for d in dp_s3_urls:
# #    print(d)

# #import pdb;pdb.set_trace()

# #dp_s3_urls = s3_prefixes.list_files_by_s3(request_timeout_ms=100)

# #for d in dp_s3_urls:
# #    import pdb;pdb.set_trace()

