from flask import Flask, render_template, after_this_request
from flask_jwt_extended import JWTManager, jwt_required, jwt_refresh_token_required, get_raw_jwt
from flask_restful import Api, Resource
from models.security import User
from neomodel import config
from resources.products import ProductEndpoint, ProductsEndpoint
from models.catalog import Catalog
from resources.security import LoginEndpoint, RefreshableTokenEndpoint, RefreshTokenEndpoint
from resources.users import UserEndpoint

app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'this-123-is-MY-super-secret-432-KEY-@@@###'
app.config['JWT_ALGORITHM'] = 'HS512'
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = 300  # seconds
app.config['JWT_REFRESH_TOKEN_EXPIRES'] = 43200  # 12 hours
app.config['JWT_BLACKLIST_ENABLED'] = True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] = ['access', 'refresh']
# TODO: Replace these values with some ENV variables
config.DATABASE_URL = 'bolt://neo4j:qwerty99@172.17.0.1:7687'
jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(username):
    user = User.find_by_name(username)
    if user is None:
        return None
    return user.name


@jwt.user_claims_loader
def add_claims_to_access_token(username):
    user = User.find_by_name(username)
    if user is None:
        return None
    if user.is_admin():
        return {'role': 'admin'}  # PUT, GET & DELETE
    return {'role': 'consumer'}  # Only GETs


@jwt.expired_token_loader
def my_expired_token_callback(expired_token):
    token_type = expired_token['type']
    return {
               'status': 401,
               'sub_status': 42,
               'msg': 'The {} token has expired'.format(token_type)
           }, 401


@jwt.invalid_token_loader
def invalid_token_callback(error):
    return {'description': 'Signature verification failed.',
            'error': 'invalid_token'}, 401


@jwt.unauthorized_loader
def missing_token_callback(error):
    return {'description': 'Request does not contain an access token.',
            'error': 'authorization_required'}, 401


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return {'description': 'The token is not fresh',
            'error': 'fresh_token_required'}, 401


@jwt.revoked_token_loader
def revoked_token_callback():
    return {'description': 'The token has been revoked.',
            'error': 'token_revoked'}, 401


# TODO: Persist Blacklisted tokens into Neo4j or Redis
blacklist = set()


@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    jti = decrypted_token['jti']
    return jti in blacklist


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


# User and Security endpoints
# Blacklist Fresh
class LogoutEndpoint(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200


# Blacklist Non Fresh
class LogoutRefreshEndpoint(Resource):
    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        blacklist.add(jti)
        return {"message": "Successfully logged out"}, 200


# Users can GET, Admins can PUT, GET and DELETE.
api.add_resource(LoginEndpoint, '/login')  # Gives back a fresh token
api.add_resource(RefreshableTokenEndpoint, '/refreshable')  # Gives back a refreshable token using a fresh token
api.add_resource(RefreshTokenEndpoint, '/refresh')  # Get non fresh token from a refreshable token
api.add_resource(LogoutRefreshEndpoint, '/logout')  # Blacklist the current refresh_token
api.add_resource(LogoutEndpoint, '/logout2')  # Blacklist the current access_token
api.add_resource(UserEndpoint, '/user/<string:role>')  # Manage Users


# TODO: Run this app with uWSGI + Nginx in a Docker container
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
