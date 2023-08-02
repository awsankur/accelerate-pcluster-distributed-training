#!/bin/bash

# Without Monitoring
#pcluster create-cluster --cluster-configuration pcluster-config.yaml --cluster-name pcluster-ml --region us-west-2 --suppress-validators "type:InstanceTypeBaseAMICompatibleValidator" --rollback-on-failure "false"

# With Monitoring
pcluster create-cluster --cluster-configuration pcluster-with-monitoring-config.yaml --cluster-name pcluster-ml-with-monitoring --region us-west-2 --suppress-validators "type:InstanceTypeBaseAMICompatibleValidator" --rollback-on-failure "false"

