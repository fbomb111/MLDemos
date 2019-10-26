#!/bin/sh

image=$1

# mkdir -p local_test/model
# mkdir -p local_test/output

# rm local_test/model/*
# rm local_test/output/*

# docker run -v $(pwd)/container/application:/opt/ml --rm ${image} train
docker run --rm ${image} application/train