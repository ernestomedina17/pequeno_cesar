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
def home():
    return render_template('index.html')


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
    def post(self):
        jti = get_raw_jwt()['jti']
        tokens_blacklist.setex(name=jti, time=app_conf.access_expires, value=jti)
        return {"message": "Successfully logged out2"}, 200


api.add_resource(LogoutEndpoint, '/logout')  # POST


# Blacklist Refresh tokens.
class LogoutRefreshEndpoint(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        tokens_blacklist.setex(name=jti, time=app_conf.refresh_expires, value=jti)
        return {"message": "Successfully logged out"}, 200


api.add_resource(LogoutRefreshEndpoint, '/logout2')  # POST

# CRUD for Users, only 'admin' or 'consumer' roles are allowed
api.add_resource(UserEndpoint, '/user/<string:role>')  # PUT, GET & DELETE

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
