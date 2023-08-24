#!/bin/bash

aws cloudformation create-stack --stack-name ankur-vpc-stack --template-body file://Large-Scale-VPC.yaml --parameters ParameterKey=SubnetsAZ,ParameterValue=us-west-2b --capabilities CAPABILITY_IAM
