from torch.utils.data import IterableDataset
from awsio.python.lib.io.s3.s3dataset import S3IterableDataset
from PIL import Image
import io
import numpy as np
from torchvision import transforms
from tifffile import imread

class ImageS3(IterableDataset):
    def __init__(self, urls, shuffle_urls=False, transform=None):
        self.s3_iter_dataset = S3IterableDataset(urls,
                                                 shuffle_urls)
        self.transform = transform

    def data_generator(self):
        try:
            while True:
                # Based on alphabetical order of files, sequence of label and image may change.
                label_fname, label_fobj = next(self.s3_iter_dataset_iterator)
                image_fname, image_fobj = next(self.s3_iter_dataset_iterator)
                
                label = int(label_fobj)
                #path, target = self.samples[idx]
                image_np= imread(image_fobj)
                
                #image_np = Image.open(io.BytesIO(image_fobj)).convert('RGB')
                
                # Apply torch vision transforms if provided
                if self.transform is not None:
                    image_np = self.transform(image_np)
                yield image_np, label

        except StopIteration:
            return
            
    def __iter__(self):
        self.s3_iter_dataset_iterator = iter(self.s3_iter_dataset)
        return self.data_generator()
        
    #def set_epoch(self, epoch):
    #    self.s3_iter_dataset.set_epoch(epoch)

# Example Torchvision transforms to apply on data    
preproc = transforms.Compose([
    transforms.ToTensor(),
    transforms.Normalize((0.485, 0.456, 0.406), (0.229, 0.224, 0.225)),
    transforms.Resize((100, 100))
])

train_dataset = ImageS3(["s3://pcluster-ml-workshop/DeepPhenotype_PBMC_ImageSet_YSeverin/Training"], transform=preproc)

train_loader = torch.utils.data.DataLoader(train_dataset, num_workers=4, batch_size=32)

for epoch in range(1):
    for i, data in enumerate(train_loader, 0):
        pass



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

