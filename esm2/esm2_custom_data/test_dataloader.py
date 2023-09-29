import os
import torch
from torch.utils.data import DataLoader
from datasets import load_from_disk, load_dataset, DatasetDict

from transformers import (
    AutoTokenizer,
    EsmForMaskedLM,
    DataCollatorForLanguageModeling,
    set_seed,
    get_scheduler,
    SchedulerType,
)

src = "bloyal/oas_paired_human_sars_cov_2"
model_id = "facebook/esm2_t33_650M_UR50D"



train_sample_count = 500000
    
train_dataset = load_from_disk('./data/train')

tokenizer = AutoTokenizer.from_pretrained(model_id)


data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer, mlm_probability=0.15
)
train_loader = DataLoader(
    train_dataset,
    collate_fn=data_collator,
    batch_size=8
)

for (idx,batch) in enumerate(train_loader):
    print('Len of batch = ' + str(len(batch['input_ids'])))
    import pdb;pdb.set_trace()

