#!/usr/bin/env bash

sudo docker pull neo4j:4.0.2
mkdir -p $HOME/neo4j/{data,logs,import,plugins,conf}
sudo docker run \
    --name pequeno_cesar \
    -p 7474:7474 -p 7687:7687 \
    -d \
    --rm \
    -v $HOME/neo4j/data:/data \
    -v $HOME/neo4j/logs:/logs \
    -v $HOME/neo4j/import:/var/lib/neo4j/import \
    -v $HOME/neo4j/plugins:/plugins \
    -v $HOME/neo4j/conf:/var/lib/neo4j/conf \
    --env NEO4J_AUTH=neo4j/qwerty99 \
    --env NEO4J_dbms_memory_pagecache_size=2G \
    --env NEO4J_dbms_memory_heap_max__size=2G \
    neo4j:4.0.2
