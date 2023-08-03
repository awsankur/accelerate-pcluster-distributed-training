#!/bin/bash

source docker.properties

docker run -t -d --gpus all --name ${docker_container_name} --shm-size 8G -v /home/ec2-user/test-dali-dataloaders/multi-channel-images/data/:/data/ ${registry}/${docker_image_name} 
