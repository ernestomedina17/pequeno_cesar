#!/usr/bin/env bash

IMAGE_VERSION='grafana/grafana:6.7.3'

docker run \
    --name pequeno_cesar_grafana \
    -p 172.17.0.1:3000:3000 \
    --rm \
    -d \
    ${IMAGE_VERSION}

# http://172.17.0.1:3000
# user:admin, password:admin

