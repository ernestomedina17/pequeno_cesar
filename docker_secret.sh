#!/bin/bash

# your user must be part of the docker group
docker swarm init
printf $NEO4J_DB_PASSWORD | docker secret create neo4j_db_password -
printf $JWT_SECRET_KEY | docker secret create jwt_secret_key -

