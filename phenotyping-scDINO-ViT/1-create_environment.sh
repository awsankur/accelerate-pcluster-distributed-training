#!/bin/bash
#
#echo "Conda installation not found. Installing..."
wget -O miniconda.sh "https://repo.anaconda.com/miniconda/Miniconda3-py38_23.3.1-0-Linux-x86_64.sh" \
	&& bash miniconda.sh -b -p /apps/.conda \
      	&&  /apps/.conda/bin/conda init bash  

source /home/ec2-user/.bashrc	
conda create --name pytorch-py38 python=3.8 

conda activate pytorch-py38
# PyTorch 1.13
conda install pytorch==1.13.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=11.6 -c pytorch -c nvidia
pip3 install -r requirements.txt
sudo wget -qO /apps/.conda/envs/pytorch-py38/bin/yq https://github.com/mikefarah/yq/releases/latest/download/yq_linux_amd64
sudo chmod a+x /apps/.conda/envs/pytorch-py38/bin/yq

# S3 streaming with TorchData
# https://github.com/pytorch/data
# Try later
#pip install torchdata==0.5.1

# S3 streaming
# https://github.com/aws/amazon-s3-plugin-for-pytorch
wget https://aws-s3-plugin.s3.us-west-2.amazonaws.com/binaries/0.0.1/bd37e27/awsio-0.0.1%2Bbd37e27-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl 
pip install awsio-0.0.1%2Bbd37e27-cp38-cp38-manylinux_2_17_x86_64.manylinux2014_x86_64.whl 

