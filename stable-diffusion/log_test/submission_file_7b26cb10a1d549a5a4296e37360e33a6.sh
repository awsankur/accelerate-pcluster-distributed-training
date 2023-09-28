#!/bin/bash

# Parameters
#SBATCH --error=/apps/accelerate-pcluster-distributed-training/stable-diffusion/log_test/%j_0_log.err
#SBATCH --job-name=submitit
#SBATCH --nodes=1
#SBATCH --open-mode=append
#SBATCH --output=/apps/accelerate-pcluster-distributed-training/stable-diffusion/log_test/%j_0_log.out
#SBATCH --partition=dev
#SBATCH --signal=USR2@90
#SBATCH --time=1
#SBATCH --wckey=submitit

# command
export SUBMITIT_EXECUTOR=slurm
srun --unbuffered --output /apps/accelerate-pcluster-distributed-training/stable-diffusion/log_test/%j_%t_log.out --error /apps/accelerate-pcluster-distributed-training/stable-diffusion/log_test/%j_%t_log.err /apps/.conda/envs/pytorch-py39/bin/python3 -u -m submitit.core._submit /apps/accelerate-pcluster-distributed-training/stable-diffusion/log_test
