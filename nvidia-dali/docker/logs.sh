#!/bin/bash

source docker.properties

echo "Running Container to test DALI dataloader"
docker logs -f ${docker_container_name}
