# pequeno_cesar
This is a POC project to test Flask REST API with Neo4j DB using neomodel OGM lib.  
Jwt_extended provides Bearer tokens and redis an in memory blacklist db to track tokens once you logout.  
Gunicorn is used to serve the app in prod.  
Prometheus_client is used to implement the metrics instrumentation.  
An API Test collection is created with Postman.   
 
When coding you can run the flask app directly from app.py for an easy debugging, gunicorn is used with Docker.  