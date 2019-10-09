#!/bin/sh

image=$1

mkdir -p local_test/test_dir/model
mkdir -p local_test/test_dir/output

rm local_test/test_dir/model/*
rm local_test/test_dir/output/*

docker run -v $(pwd)/local_test/test_dir:/opt/ml --rm ${image} train
