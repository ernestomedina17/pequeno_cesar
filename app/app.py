from flask import Flask, render_template
from flask_jwt_extended import JWTManager, jwt_required, get_raw_jwt, jwt_refresh_token_required
from flask_restful import Api, Resource
from resources.products import ProductEndpoint, ProductsEndpoint
from models.catalog import Catalog
from resources.users import UserEndpoint
from errors import errors
from neomodel import config
from config import set_app_config
from security import configure_JWTManager, LoginEndpoint, RefreshableTokenEndpoint, RefreshTokenEndpoint
from prometheus_client import multiprocess, generate_latest, CollectorRegistry
from metrics import metrics_req_latency, metrics_req_count, metrics_req_in_progress
import redis

app = Flask(__name__)
api = Api(app=app, errors=errors)
app_conf = set_app_config()
app.config.from_object(app_conf)
config.DATABASE_URL = app_conf.NEO4J_DB_URL
jwt = JWTManager(app)
tokens_blacklist = redis.StrictRedis(host=app_conf.REDIS_DB_SERVER,
                                     port=6379,
                                     db=0,
                                     decode_responses=True)
configure_JWTManager(jwt, tokens_blacklist)


@app.before_first_request
def load_catalog():
    Catalog.load_nodes()
    Catalog.load_relations()
    Catalog.load_users()


@app.route('/')
@metrics_req_latency.time()
@metrics_req_in_progress.track_inprogress()
def home():
    metrics_req_count.labels(method='GET', endpoint='/', status_code='200').inc()  # Increment the counter
    return render_template('index.html')


@app.route('/metrics')
def metrics():
    registry = CollectorRegistry()
    multiprocess.MultiProcessCollector(registry)
    return generate_latest(registry), 200


# Valid product categories are: Pizza, Complement, Drink, Sauce and Package
api.add_resource(ProductEndpoint, '/product/<string:category>')  # PUT, GET & DELETE

# Return all the products
api.add_resource(ProductsEndpoint, '/products')  # GET

# Users can GET, Admins can PUT, GET and DELETE.
# Gives back a fresh token
api.add_resource(LoginEndpoint, '/login')  # POST

# Gives back a refreshable token using a fresh token
api.add_resource(RefreshableTokenEndpoint, '/refreshable')  # POST

# Get non fresh token from a refreshable token
api.add_resource(RefreshTokenEndpoint, '/refresh')  # POST


# Blacklist fresh_tokens and access_tokens
class LogoutEndpoint(Resource):
    @jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def post(self):
        jti = get_raw_jwt()['jti']
        tokens_blacklist.setex(name=jti, time=app_conf.access_expires, value=jti)
        metrics_req_count.labels(method='POST', endpoint='/logout2', status_code='200').inc()
        return {"message": "Successfully logged out2"}, 200


api.add_resource(LogoutEndpoint, '/logout2')  # POST


# Blacklist Refresh tokens.
class LogoutRefreshEndpoint(Resource):
    @jwt_refresh_token_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def post(self):
        jti = get_raw_jwt()['jti']
        tokens_blacklist.setex(name=jti, time=app_conf.refresh_expires, value=jti)
        metrics_req_count.labels(method='POST', endpoint='/logout', status_code='200').inc()
        return {"message": "Successfully logged out"}, 200


api.add_resource(LogoutRefreshEndpoint, '/logout')  # POST

# CRUD for Users, only 'admin' or 'consumer' roles are allowed
api.add_resource(UserEndpoint, '/user/<string:role>')  # PUT, GET & DELETE


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
