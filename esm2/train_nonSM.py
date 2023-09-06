# Copyright 2019-2020 Amazon.com, Inc. or its affiliates. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License"). You
# may not use this file except in compliance with the License. A copy of
# the License is located at
#
#     http://aws.amazon.com/apache2.0/
#
# or in the "license" file accompanying this file. This file is
# distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF
# ANY KIND, either express or implied. See the License for the specific
# language governing permissions and limitations under the License.

# model_checkpoint="facebook/esm2_t48_15B_UR50D" # 15B params
# model_checkpoint="facebook/esm2_t36_3B_UR50D"
# model_checkpoint="facebook/esm2_t33_650M_UR50D"
# model_checkpoint="facebook/esm2_t30_150M_UR50D"
# model_checkpoint="facebook/esm2_t12_35M_UR50D"
# model_checkpoint = "facebook/esm2_t6_8M_UR50D"  # 8M params

# torchrun train.py --train_sample_count=50000 --model_id="facebook/esm2_t33_650M_UR50D" --num_epochs=3

import os
import argparse
from datasets import load_from_disk, load_dataset, DatasetDict
import math
from timeit import default_timer as timer
import torch
from torch.optim import AdamW
from torch.utils.data import DataLoader
from torch.utils.data.distributed import DistributedSampler
from tqdm.auto import tqdm
from transformers import (
    AutoTokenizer,
    AutoModelForMaskedLM,
    DataCollatorForLanguageModeling,
    set_seed,
    get_scheduler,
    SchedulerType,
)

## SageMaker Distributed code.
#from smdistributed.dataparallel.torch.parallel.distributed import (
#    DistributedDataParallel as DDP,
#)
#import smdistributed.dataparallel.torch.distributed as dist


import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP

dist.init_process_group("nccl")

def parse_args():
    """Parse the arguments."""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--lr", type=float, default=5e-5, help="Learning rate to use for training."
    )
    parser.add_argument(
        "--lr_scheduler_type",
        type=SchedulerType,
        default="linear",
        help="The scheduler type to use.",
        choices=[
            "linear",
            "cosine",
            "cosine_with_restarts",
            "polynomial",
            "constant",
            "constant_with_warmup",
        ],
    )
    parser.add_argument(
        "--max_length",
        type=int,
        default=142,
        help="Max length of sequence for collator.",
    )
    parser.add_argument(
        "--model_dir",
        type=str,
        default='./model',
        help="Path to model output folder.",
    )
    parser.add_argument(
        "--model_id",
        type=str,
        default="facebook/esm2_t33_650M_UR50D",
        help="Model id to use for training.",
    )
    parser.add_argument(
        "--num_epochs", type=int, default=1, help="Number of epochs to train."
    )
    parser.add_argument(
        "--num_warmup_steps",
        type=int,
        default=0,
        help="Number of steps for the warmup in the lr scheduler.",
    )
    parser.add_argument(
        "--per_device_eval_batch_size",
        type=int,
        default=8,
        help="Batch size (per device) for the evaluation dataloader.",
    )
    parser.add_argument(
        "--per_device_train_batch_size",
        type=int,
        default=8,
        help="Batch size (per device) for the training dataloader.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        default=42,
        help="Random seed.",
    )
    parser.add_argument(
        "--logging_steps",
        type=int,
        default=10,
        help="Number of steps between logging updates.",
    )
    parser.add_argument(
        "--gradient_accumulation_steps",
        type=int,
        default=1,
        help="Number of steps between gradient optimization.",
    )
    parser.add_argument(
        "--train_sample_count",
        type=int,
        default=None,
        help="Number of training samples to pre-process.",
    )
    parser.add_argument(
        "--steps_this_run",
        type=int,
        default=None,
        help="Max number of steps.",
    )

    args, _ = parser.parse_known_args()
    return args


def calc_perplexity(loss):
    try:
        perplexity = math.exp(loss)
    except OverflowError:
        perplexity = float("inf")
    return perplexity


def report_metrics(
    rank, start_time, loss, epoch, steps, sample_count, token_count, prefix=None
):
    reported_loss = loss.detach().float()
    now = timer()
    duration = now - start_time
    samples_per_sec = sample_count / duration
    tokens_per_sec = token_count / duration
    perplexity = calc_perplexity(reported_loss)
    if prefix:
        prefix = prefix + " "
    if rank == 0:
        print(
            f"Epoch: {epoch}, Step: {steps}, {prefix}Loss: {reported_loss:0.4f}, {prefix}Perplexity: {perplexity:0.4f}, {prefix}Samples/sec: {samples_per_sec:0.4f}, {prefix}Tokens/sec: {tokens_per_sec:0.4f}"
        )

    return None


def main(args):

    run_start = timer()
    if args.seed is not None:
        set_seed(args.seed)
        torch.manual_seed(args.seed)
        torch.cuda.manual_seed(args.seed)

    device = torch.device("cuda")

    world_size = dist.get_world_size()
    rank = dist.get_rank()
    #local_rank = dist.get_local_rank()

    print(f"Start running DDP on rank {rank}.")

    ## Load model
    model = AutoModelForMaskedLM.from_pretrained(args.model_id)
    model.to(device)
    model = DDP(model, find_unused_parameters=True)
    #torch.cuda.set_device(local_rank)
    #model.cuda(local_rank)

    is_root = rank == 0

    if args.train_sample_count is not None:
        if rank > 0:
            torch.distributed.barrier()
        dataset = get_data(args.train_sample_count)
        train_dataset = dataset["train"]
        eval_dataset = dataset["test"]
        if rank == 0:
            torch.distributed.barrier()
    else:
        train_dataset = load_from_disk(args.training_dir)
        eval_dataset = load_from_disk(args.eval_dir)

    if is_root:
        print(f"Loaded train_dataset length is: {len(train_dataset)}")
        print(f"Loaded test_dataset length is: {len(eval_dataset)}")

    tokenizer = AutoTokenizer.from_pretrained(args.model_id)
    tokenizer.model_max_length = args.max_length
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=tokenizer, mlm_probability=0.15
    )

    train_sampler = None
    eval_sampler = None
    if world_size > 1:  # if more than one core
        train_sampler = DistributedSampler(
            train_dataset,
            num_replicas=world_size,
            rank=rank,
            shuffle=True,
        )
        eval_sampler = DistributedSampler(
            eval_dataset,
            num_replicas=world_size,
            rank=rank,
            shuffle=True,
        )

    train_loader = DataLoader(
        train_dataset,
        collate_fn=data_collator,
        batch_size=args.per_device_train_batch_size,
        sampler=train_sampler,
        shuffle=False if train_sampler else True,
    )
    eval_loader = DataLoader(
        eval_dataset,
        collate_fn=data_collator,
        batch_size=args.per_device_eval_batch_size,
        sampler=eval_sampler,
        shuffle=False if eval_sampler else True,
    )

    # Define training metrics
    num_update_steps_per_epoch = len(train_loader)
    num_total_training_steps = args.num_epochs * num_update_steps_per_epoch
    total_train_batch_size = args.per_device_train_batch_size * world_size
    samples_processed_per_logging_update = total_train_batch_size * args.logging_steps
    tokens_processed_per_logging_update = (
        samples_processed_per_logging_update * args.max_length
    )

    # Define eval metrics

    num_eval_steps_per_epoch = len(eval_loader)
    total_eval_batch_size = args.per_device_eval_batch_size * world_size
    samples_processed_per_eval = total_eval_batch_size * num_eval_steps_per_epoch
    tokens_processed_per_eval = samples_processed_per_eval * args.max_length

    ## Load and configure model
    model = AutoModelForMaskedLM.from_pretrained(args.model_id)
    model.to(device)
    optimizer = AdamW(model.parameters(), args.lr)
    lr_scheduler = get_scheduler(
        name=args.lr_scheduler_type,
        optimizer=optimizer,
        num_warmup_steps=args.num_warmup_steps,
        num_training_steps=num_total_training_steps,
    )

    if is_root:
        print("***** Running training *****")
        print(f"\nNum examples: {len(train_dataset)}")
        print(f"\nNum Epochs: {args.num_epochs}")
        print(
            f"\nInstantaneous batch size per device = {args.per_device_train_batch_size}"
        )
        print(
            f"\nTotal train batch size (w. parallel, distributed & accumulation) = {total_train_batch_size}"
        )
        print(f"\nTotal optimization steps = {num_total_training_steps}")

    # Only show the progress bar once on each machine.
    progress_bar = tqdm(
        range(num_total_training_steps), disable=not is_root, miniters=1
    )
    completed_steps = 0
    starting_epoch = 0

    # Start training loop
    for epoch in range(starting_epoch, args.num_epochs):
        if is_root:
            print("######################### Train #########################")
        model.train()
        for idx, batch in enumerate(train_loader):
            train_loop_start_time = timer()
            progress_bar.update(1)
            batch = {
                k: v.to(device) for k, v, in batch.items()
            }  # Transfer data to accelerator
            outputs = model(**batch)  # Forward pass
            optimizer.zero_grad()  # Set all tensor gradients to zero
            loss = outputs.loss  # Calculate loss
            loss.backward()  # Calculate new gradients with backprop
            lr_scheduler.step()  # Update scheduler

            if ((idx + 1) % args.gradient_accumulation_steps == 0) or (
                idx + 1 == num_update_steps_per_epoch
            ):
                optimizer.step()

            completed_steps += 1
            if (idx + 1) % args.logging_steps == 0:
                report_metrics(
                    rank,
                    train_loop_start_time,
                    loss,
                    epoch,
                    completed_steps,
                    samples_processed_per_logging_update,
                    tokens_processed_per_logging_update,
                    "Training",
                )

        if is_root:
            print("######################### Eval #########################")
        eval_start_time = timer()
        model.eval()
        eval_running_loss = 0
        for batch in eval_loader:
            with torch.no_grad():
                batch = {k: v.to(device) for k, v, in batch.items()}
                outputs = model(**batch)
            eval_loss = outputs.loss
            eval_running_loss += eval_loss.detach().float() / num_eval_steps_per_epoch

        report_metrics(
            rank,
            eval_start_time,
            eval_running_loss,
            epoch,
            completed_steps,
            samples_processed_per_eval,
            tokens_processed_per_eval,
            "Eval",
        )

    # Save checkpoint for evaluation (xm.save ensures only one process save)
    if is_root:
        model = model.module if hasattr(model, "module") else model
        os.makedirs(args.model_dir, exist_ok=True)
        checkpoint = {"state_dict": model.state_dict()}
        path = f"{args.model_dir}/checkpoint.pt"
        torch.save(checkpoint, path)

        print("##### Model saved to: ", f"{args.model_dir}/checkpoint.pt")
        print(f"Run completed in {timer() - run_start} sec.")


def tokenize_data(examples, tokenizer, sequence_length):
    encoding = tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=sequence_length,
    )
    return encoding


def get_data(train_sample_count):
    src = "bloyal/oas_paired_human_sars_cov_2"
    test_sample_count = int(train_sample_count * 0.2)
    train_dataset = load_dataset(src, split=f"train[:{train_sample_count}]")
    test_dataset = load_dataset(src, split=f"test[:{test_sample_count}]")
    dataset = DatasetDict({"train": train_dataset, "test": test_dataset}).rename_column(
        "sequence_alignment_aa_heavy", "text"
    )
    tokenizer = AutoTokenizer.from_pretrained("facebook/esm2_t6_8M_UR50D")
    sequence_length = 142
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
    return encoded_dataset


if __name__ == "__main__":
    args = parse_args()
    main(args)

