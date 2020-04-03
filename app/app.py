from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_restful import Api
from neomodel import config
from resources.products import ProductEndpoint, ProductsEndpoint
from models.catalog import Catalog

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)

config.DATABASE_URL = 'bolt://neo4j:qwerty99@localhost:7687'


@app.before_first_request
def load_catalog():
    Catalog.load_nodes()
    Catalog.load_relations()


@app.route('/')
def home():
    return render_template('index.html')


# Valid product categories are: Pizza, Complement, Drink, Sauce and Package
api.add_resource(ProductEndpoint, '/product/<string:category>')  # PUT, GET & DELETE

# Return all the products
api.add_resource(ProductsEndpoint, '/products')  # GET

#  Tiendas
# api.add_resource(Store, '/store/<int:user_id>')
# api.add_resource(Stores, '/stores')
# api.add_resource(SearchStores, '/stores')

#  User endpoints
# api.add_resource(User, '/user/<int:user_id>')           # Person
# api.add_resource(UserRegister, '/register')             # Create Person
# api.add_resource(UserLogin, '/login')                   # Login
# api.add_resource(UserLogout, '/logout')                 # Blacklist the token, not user
# api.add_resource(TokenRefresh, '/refresh')              # Refresh the token

# TODO: Run this app with uWSGI + Nginx in a Docker container
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
