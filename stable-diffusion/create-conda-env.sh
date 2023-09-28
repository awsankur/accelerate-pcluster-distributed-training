#!/bin/bash
#
#echo "Conda installation not found. Installing..."
wget -O miniconda.sh "https://repo.anaconda.com/miniconda/Miniconda3-py39_23.5.2-0-Linux-x86_64.sh" \
	&& bash miniconda.sh -b -p /apps/.conda \
      	&&  /apps/.conda/bin/conda init bash  

source /home/ubuntu/.bashrc	
conda create --name pytorch-py39 python=3.9

conda activate pytorch-py39
# PyTorch 1.12
#conda install pytorch==1.12.1 torchvision==0.14.1 torchaudio==0.13.1 pytorch-cuda=12.1 -c pytorch -c nvidia

conda install pytorch==2.0.0 torchvision==0.15.0 torchaudio==2.0.0 pytorch-cuda=11.8 -c pytorch -c nvidia


pip3 install diffusers
pip3 install transformers
pip3 install mosaicml-streaming
pip3 install mosaicml==0.15.0 --force
pip3 install accelerate
pip3 install wandb
pip3 install submitit
