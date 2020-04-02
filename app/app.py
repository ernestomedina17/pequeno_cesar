from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_restful import Api
from resources.products import ProductEndpoint, ProductsEndpoint

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)


@app.route('/')
def home():
    return render_template('index.html')


# Food endpoints
api.add_resource(ProductEndpoint, '/product')       # PUT, GET & DELETE
api.add_resource(ProductsEndpoint, '/products')     # GET

#  paquetes: comida completa, fiesta, crazy_combo
# api.add_resource(Package, '/package/<string:name>')
# api.add_resource(Packages, '/packages')

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

# TODO: Run this app with uWSGI + Nginx
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
