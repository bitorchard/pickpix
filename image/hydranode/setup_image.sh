#!/bin/bash

docker build --tag hydranode:latest . --no-cache
docker save hydranode > hydranode.tar
microk8s ctr image import hydranode.tar
