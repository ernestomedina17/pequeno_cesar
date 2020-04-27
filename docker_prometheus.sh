#!/usr/bin/env bash

IMAGE_VERSION='prom/prometheus:v2.17.2'

docker run \
    --name pequeno_cesar_prometheus \
    -p 172.17.0.1:9090:9090 \
    --rm \
    -d \
    ${IMAGE_VERSION}

# http://172.17.0.1:9090/graph
# http://172.17.0.1:9090/consoles/prometheus.html
