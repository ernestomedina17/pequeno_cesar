# Pequeno Cesar
This is a POC project to test Flask REST API with Neo4j DB using neomodel OGM lib.  
Jwt_extended provides Bearer tokens and redis blacklist your token when you logout.  
Gunicorn and Docker are used to serve the app. 
Metric instrumentation is implemented with the prometheus_client lib.  
An API Test collection is created with Postman.   
  
In order to successfully start the container you need to set:
- **Docker Environment variables**:
    - APP_MODE; string, valid values are: 'dev', 'test' or 'prod'

- **Docker Secrets**: The app will expect them to be at /run/secrets/<secret_name>
  - neo4j_db_user; 'neo4j'
  - neo4j_db_password; string
  - default_app_user_name; string
  - default_app_user_password; string
  - default_app_admin_name; string 
  - default_app_admin_password; string
  - jwt_secret_key; string

Check out the **docker-compose.yml** for details.

# Postman Test
In order to successfully run the Postman test you need to set these variables in Postman:
- host: 172.17.0.1:5000
- fresh_token: none
- refresh_token: none
- access_token: none
- user_fresh_token: none
- default_app_user_name: must match the value of the secret with the same name.
- default_app_user_password: must match the value of the secret with the same name.
- default_app_admin_name: must match the value of the secret with the same name.
- default_app_admin_password: must match the value of the secret with the same name.

# Prometheus and Grafana
Prometheus and Grafana are configured via docker-compose volumes.
