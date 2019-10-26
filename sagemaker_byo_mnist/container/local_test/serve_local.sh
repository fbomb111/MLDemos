#!/bin/sh

image=$1

# docker run -v $(pwd)/local_test:/opt/ml -p 8080:8080 --rm ${image} serve
docker run -p 8080:8080 --rm ${image} application/serve
