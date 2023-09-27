#!/bin/bash


# P4de
pcluster create-cluster --cluster-configuration p4de-efa-config-no-ami.yaml --cluster-name awsankur-p4de-pcluster --region us-west-2 --suppress-validators "type:InstanceTypeBaseAMICompatibleValidator" --rollback-on-failure "false"
# P5
#pcluster create-cluster --cluster-configuration p5-config.yaml --cluster-name awsankur-p5-pcluster --region us-west-2 --suppress-validators "type:InstanceTypeBaseAMICompatibleValidator" --rollback-on-failure "false"

#g5
#pcluster create-cluster --cluster-configuration g5-config.yaml --cluster-name awsankur-g5-pcluster --region us-west-2 --suppress-validators "type:InstanceTypeBaseAMICompatibleValidator" --rollback-on-failure "false"
