import os
import argparse
from datasets import load_dataset, DatasetDict
from transformers import AutoTokenizer


import math
from timeit import default_timer as timer
import torch



src = "bloyal/oas_paired_human_sars_cov_2"
train_sample_count = 10000
test_sample_count = int(train_sample_count * 0.2)

train_dataset = load_dataset(src, split=f"train[:{train_sample_count}]")
test_dataset = load_dataset(src, split=f"test[:{test_sample_count}]")
dataset = DatasetDict({"train": train_dataset, "test": test_dataset}).rename_column(
    "sequence_alignment_aa_heavy", "text"
)


tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t6_8M_UR50D")
sequence_length = 142


def tokenize_data(examples, tokenizer, sequence_length):
    encoding = tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=sequence_length,
    )
    return encoding


encoded_dataset = dataset.map(
    tokenize_data,
    batched=True,
    num_proc=os.cpu_count(),
    remove_columns=dataset["train"].column_names,
    fn_kwargs={
        "tokenizer": tokenizer,
        "sequence_length": sequence_length,
    },
)

encoded_dataset.set_format("torch", columns=["input_ids", "attention_mask"])


example = encoded_dataset["train"][0]
print(example["input_ids"])
print(tokenizer.decode(example["input_ids"]))

train_s3_uri = "./data/train"
test_s3_uri = "./data/test"

encoded_dataset["train"].save_to_disk(train_s3_uri)
encoded_dataset["test"].save_to_disk(test_s3_uri)
