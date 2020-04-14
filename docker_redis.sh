#!/usr/bin/env bash

IMAGE_VERSION='redis:5.0.8-alpine3.11'

docker run \
    --name pequeno_cesar_redis \
    -p 172.17.0.1:6379:6379 \
    --rm \
    -d \
    ${IMAGE_VERSION}
