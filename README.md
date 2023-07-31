# Accelearte Distributed Training on AWS ParallelCluster

## 0. Prerequisites
We assume a Slurm cluster is already created. For a step-by-step set of instructions to create a cluster, please follow this [repo](https://github.com/aws-samples/aws-distributed-training-workshop-pcluster/tree/main)

Model: [scDINO](https://github.com/JacobHanimann/scDINO/tree/master) with Vision Transformers

## 1. Download Deep Phenotyping Image Data
Execute ./1-download-data.sh to download the image data, unzip it, create a S3 bucket pcluster-ml-workshop and upload to the S3 bucket. You can find more information about the dataset here. This dataset has 90852 images in the Training set and 22712 images in the Test set.

## 2. Approaches
1. Baseline results with a cluster of g4dn.12xlarge instances
2. NCCL Tests
3. Scaling with EFA
4. DALI dataloaders
5. Storage Strategy
6. GPU Performance
7. Better Transformers
8. Fully Sharded Data Parallel

### 3. Baseline results 
