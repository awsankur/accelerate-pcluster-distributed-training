#!/bin/bash

# Without Monitoring
#pcluster create-cluster --cluster-configuration pcluster-config.yaml --cluster-name pcluster-ml --region us-west-2 --suppress-validators "type:InstanceTypeBaseAMICompatibleValidator" --rollback-on-failure "false"

# With Monitoring
pcluster create-cluster --cluster-configuration p4de-efa-config.yaml --cluster-name awsankur-pcluster-ml-with-monitoring --region us-west-2 --suppress-validators "type:InstanceTypeBaseAMICompatibleValidator" --rollback-on-failure "false"

