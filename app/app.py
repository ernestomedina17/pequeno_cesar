from flask import Flask, render_template
from flask_jwt_extended import JWTManager, get_jwt_claims, verify_jwt_in_request
from flask_restful import Api
from neomodel import config
from resources.products import ProductEndpoint, ProductsEndpoint
from models.catalog import Catalog
from resources.security import LoginEndpoint


app = Flask(__name__)
api = Api(app)
app.config['JWT_SECRET_KEY'] = 'this-123-is-MY-super-secret-432-KEY-@@@###'
config.DATABASE_URL = 'bolt://neo4j:qwerty99@localhost:7687'
jwt = JWTManager(app)


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.name


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    if user.is_admin():
        return {'role': 'admin'}    # PUT, GET & DELETE
    return {'role': 'consumer'}     # Only GETs


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

# User endpoints
# Users can GET, Admins can PUT, GET and DELETE.
api.add_resource(LoginEndpoint, '/login')
# api.add_resource(User, '/user/<int:user_id>')           # Person
# api.add_resource(UserRegister, '/register')             # Create Person

# api.add_resource(UserLogout, '/logout')                 # Blacklist the token, not user
# api.add_resource(TokenRefresh, '/refresh')              # Refresh the token

# TODO: Run this app with uWSGI + Nginx in a Docker container
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
