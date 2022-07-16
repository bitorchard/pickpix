#!/bin/bash

docker build --tag apache-django-base:local . --no-cache
docker save apache-django-base > apache-django-base.tar
microk8s ctr image import apache-django-base.tar
