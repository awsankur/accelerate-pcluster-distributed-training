#!/bin/bash

# Make sure you have installed the AWS Command Line Interface:
pip3 install awscli

# Pcluster Dependencies
python3 -m pip install flask==2.2.5
# Node.js
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.38.0/install.sh | bash
chmod ug+x ~/.nvm/nvm.sh
source ~/.nvm/nvm.sh
nvm install --lts
node --version

# Install AWS ParallelCluster:
pip3 install aws-parallelcluster
