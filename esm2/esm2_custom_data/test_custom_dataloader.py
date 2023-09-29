import os
from datasets import load_from_disk, load_dataset, DatasetDict
import glob
import pandas as pd
import torch
from torch.utils.data import DataLoader

from transformers import (
    AutoTokenizer,
    EsmForMaskedLM,
    DataCollatorForLanguageModeling,
    set_seed,
    get_scheduler,
    SchedulerType,
)

class Dataset(torch.utils.data.Dataset):
    #'Characterizes a dataset for PyTorch'
    def __init__(self, list_IDs, file_index_map_df):
    
        #'Initialization'
        self.file_index_map = file_index_map_df
        self.list_IDs = list_IDs
        self.data_dir = './sample-amgen-data'
        self.files = glob.glob(self.data_dir+"/*")
        
    def __len__(self):
        # 'Denotes the total number of samples'
        return len(self.list_IDs)
        
    def __getitem__(self, index):
        #'Generates one sample of data'
        # Select sample
        ID = self.list_IDs[index]
        #print(ID)
        file_index_map_df = self.file_index_map
        data_dir = self.data_dir
        files = self.files
        
        
        file_num = file_index_map_df.loc[(ID >= file_index_map_df['start_line_num']) & (ID <= file_index_map_df['end_line_num'])==True,'file_num']
        start_line_num = file_index_map_df.loc[file_index_map_df['file_num']==file_num.iloc[0],'start_line_num']
        
        local_ID = ID - start_line_num.iloc[0]
        
        # Read from sharded files
        one_file_path = files[file_num.iloc[0]]
        
        df = pd.read_parquet(one_file_path, engine='pyarrow')
        input_ids = torch.from_numpy(df['input_ids'][local_ID])
        attention_mask = torch.from_numpy(df['attention_mask'][local_ID])

        sample = {'input_ids':input_ids, 'attention_mask':attention_mask}
        
        
        return sample


file_index_map_df = pd.read_csv('./file_index_map_df.csv')

num_lines = max(file_index_map_df['end_line_num'])
nTrain = round(0.8*num_lines)


train_partition = list(range(0,nTrain))


train_dataset = Dataset(train_partition,file_index_map_df)




train_loader = DataLoader(
    train_dataset,
    batch_size=8
)


for (idx,batch) in enumerate(train_loader):
    print('Len of batch = ' + str(len(batch['input_ids'])))
    import pdb;pdb.set_trace()

