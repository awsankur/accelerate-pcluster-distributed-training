#!/bin/bash

#SBATCH --wait-all-nodes=1
#SBATCH --nodes=4
#SBATCH --cpus-per-task=16
#SBATCH --ntasks-per-node=1
#SBATCH --exclusive
#SBATCH --output /apps/accelerate-pcluster-distributed-training/nvme_out_%j.out
#SBATCH --error /apps/accelerate-pcluster-distributed-training/nvme_err_%j.err

cd /apps/accelerate-pcluster-distributed-training/

srun ./copy_data_nvme_drive.sh
