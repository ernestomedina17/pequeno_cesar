#!/usr/bin/env bash

# Add your user to the docker group so you don't need to use sudo
# docker pull neo4j:4.0.2
# mkdir -p $HOME/neo4j/{data,logs,import,plugins,conf}

# This version was selected for their compatibility with the latest neomodel lib
IMAGE_VERSION='neo4j:3.3.9'

### OPTIONAL ARGs
#   --env NEO4J_dbms_connectors_default__listen__address='0.0.0.0' \
#    -v $HOME/neo4j/data:/data \
#    -v $HOME/neo4j/logs:/logs \
#    -v $HOME/neo4j/import:/var/lib/neo4j/import \
#    -v $HOME/neo4j/plugins:/plugins \
#    -v $HOME/neo4j/conf:/var/lib/neo4j/conf \

docker run \
    --name pequeno_cesar_db \
    -p 172.17.0.1:7474:7474 -p 172.17.0.1:7687:7687 \
    --rm \
    -d \
    --env NEO4J_AUTH=neo4j/${NEO4J_DB_PASSWORD} \
    --env NEO4J_dbms_memory_pagecache_size=2G \
    --env NEO4J_dbms_memory_heap_max__size=2G \
    ${IMAGE_VERSION}
