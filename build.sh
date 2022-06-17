#!/bin/sh

DOCKER_TAG=pythonstock/pythonstock:2206

# sudo rm -rf data
# sudo rm -f jobs/nohup.out
rm -rf data
rm -f jobs/nohup.out

echo " docker build -f Dockerfile -t ${DOCKER_TAG} ."
docker build -f Dockerfile -t ${DOCKER_TAG} .
echo "#################################################################"
echo " docker push ${DOCKER_TAG} "

mkdir data

