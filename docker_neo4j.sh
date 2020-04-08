#!/usr/bin/env bash

IMAGE_VERSION='neo4j:3.3.9'
# Add your user to the docker group, and re-login
docker pull ${IMAGE_VERSION}

### OPTIONAL ARGs
# mkdir -p $HOME/neo4j/{data,logs,import,plugins,conf}
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
    --env NEO4J_AUTH=neo4j/qwerty99 \
    --env NEO4J_dbms_memory_pagecache_size=2G \
    --env NEO4J_dbms_memory_heap_max__size=2G \
    ${IMAGE_VERSION}

#sleep 5
#curl http://localhost:5000  # Catalog.load functions get trigger
#./venv/bin/neomodel_install_labels app.py app.models --db 'bolt://neo4j:qwerty99@localhost:7687'

