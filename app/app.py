from flask import Flask, render_template
from flask_jwt_extended import JWTManager
from flask_restful import Api

app = Flask(__name__)
api = Api(app)
jwt = JWTManager(app)


@app.before_first_request
def create_tables():
    pass


@app.route('/')
def home():
    return render_template('index.html')

# Imagine this API provides the resources to create this web site: https://mexico.littlecaesars.com/productos

# Food endpoints
#  pizza: crazy curnch, pepperoni clasica, 3 meat treat, ultimate supreme, hula hawaiian, queso, deep!deep! dish
#  complementos: crazy bread relleno, crazy bread, italian cheese bread, caesar wings
# api.add_resource(Product, '/product/<string:name>')
# api.add_resource(Products, '/products')

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
app.run(host='0.0.0.0', port=8080, debug=True)
