#!/bin/bash

#SBATCH --wait-all-nodes=1
#SBATCH --nodes=1
#SBATCH --cpus-per-task=16
#SBATCH --ntasks-per-node=1
#SBATCH --exclusive
#SBATCH --output /apps/accelerate-pcluster-distributed-training/phenotyping-scDINO-ViT/std_out_%j.out
#SBATCH --error /apps/accelerate-pcluster-distributed-training/phenotyping-scDINO-ViT/std_err_%j.err

source /home/ec2-user/.bashrc
conda activate pytorch-py38

cd /apps/accelerate-pcluster-distributed-training/phenotyping-scDINO-ViT/pyscripts/

srun python3 mean_std_dataset.py

