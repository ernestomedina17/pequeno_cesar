<<<<<<< HEAD
from flask_restful import Resource, reqparse
from models.products import Product
from flask_jwt import jwt_required
=======
from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from models.products import Pizza, Complement, Drink, Sauce, Package, Products
from flask_jwt_extended import jwt_required, get_jwt_claims
from security import admin_required


def validate_category(category):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help='A product cannot have a blank name')

    data = parser.parse_args()

    if safe_str_cmp(category, 'Pizza'):
        product = Pizza.find_by_name(data['name'])

    elif safe_str_cmp(category, 'Complement'):
        product = Complement.find_by_name(data['name'])

    elif safe_str_cmp(category, 'Drink'):
        product = Drink.find_by_name(data['name'])

    elif safe_str_cmp(category, 'Sauce'):
        product = Sauce.find_by_name(data['name'])

    elif safe_str_cmp(category, 'Package'):
        product = Package.find_by_name(data['name'])

    else:
        return None, None

    return product, data
>>>>>>> 7aa93a5445c9ddec183559c448340e9a5aca848c


# CRUD Product - API Endpoint
class ProductEndpoint(Resource):

<<<<<<< HEAD
    def put(self):
        parser = reqparse.RequestParser()
        #  pizza: crazy crunch, pepperoni clasica, 3 meat treat, ultimate supreme, hula hawaiian, queso, deep!deep! dish
        #  complementos: crazy bread relleno, crazy bread, italian cheese bread, caesar wings
        #  drinks: pepsi 2L
        #  salsas: crazy sauce
=======
    @admin_required
    def put(self, category):
        parser = reqparse.RequestParser()
>>>>>>> 7aa93a5445c9ddec183559c448340e9a5aca848c
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A product cannot have a blank name')
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help='A product cannot have a blank price')
<<<<<<< HEAD
        parser.add_argument('category',
                            type=str,
                            required=True,
                            choices=('Pizza', 'Complement', 'Drink', 'Sauce'),
                            help='Bad choice: {error_msg}')
        parser.add_argument('ingredients',
                            type=list,
                            required=True,
                            location='json',
                            help='A product cannot have a blank list of ingredients')
=======
>>>>>>> 7aa93a5445c9ddec183559c448340e9a5aca848c
        parser.add_argument('units',
                            type=int,
                            required=False,
                            help='Set the quantity of units')

<<<<<<< HEAD
        data = parser.parse_args()
        product = Product.find_by_name(data['name'])
        data['ingredients'] = [ingredient.upper() for ingredient in data['ingredients']]

        if product is None:
            product = Product(**data)
        else:
            product.price = data['price']
            product.category = data['category']
            product.ingredients = data['ingredients']
            product.units = data['units']
=======
        if safe_str_cmp(category, 'Pizza'):
            parser.add_argument('ingredients',
                                type=list,
                                required=True,
                                location='json',
                                help='A pizza cannot have a blank list of ingredients')
            parser.add_argument('form',
                                type=str,
                                required=True,
                                choices=('REDONDA', 'CUADRADA'),
                                help='A pizza cannot have a blank form')
            data = parser.parse_args()
            product = Pizza.find_by_name(data['name'])
            data['ingredients'] = [ingredient.upper() for ingredient in data['ingredients']]

            if product is None:
                product = Pizza(**data)
            else:
                product.price = data['price']
                product.units = data['units']
                product.ingredients = data['ingredients']
                product.form = data['form']

        elif safe_str_cmp(category, 'Complement'):
            parser.add_argument('ingredients',
                                type=list,
                                required=True,
                                location='json',
                                help='A complement cannot have a blank list of ingredients')
            parser.add_argument('description',
                                type=str,
                                required=True,
                                help='A complement cannot have a blank description')
            data = parser.parse_args()
            product = Complement.find_by_name(data['name'])
            data['ingredients'] = [ingredient.upper() for ingredient in data['ingredients']]

            if product is None:
                product = Complement(**data)
            else:
                product.price = data['price']
                product.units = data['units']
                product.ingredients = data['ingredients']
                product.description = data['description']

        elif safe_str_cmp(category, 'Drink'):
            parser.add_argument('brand',
                                type=str,
                                required=True,
                                help='A drink cannot have a blank brand')
            parser.add_argument('litres',
                                type=float,
                                required=True,
                                help='A drink cannot have a blank number of litres')
            data = parser.parse_args()
            product = Drink.find_by_name(data['name'])

            if product is None:
                product = Drink(**data)
            else:
                product.price = data['price']
                product.units = data['units']
                product.brand = data['brand']
                product.litres = data['litres']

        elif safe_str_cmp(category, 'Sauce'):
            parser.add_argument('description',
                                type=str,
                                required=True,
                                help='A sauce cannot have a blank description')
            data = parser.parse_args()
            product = Sauce.find_by_name(data['name'])

            if product is None:
                product = Sauce(**data)
            else:
                product.price = data['price']
                product.units = data['units']
                product.description = data['description']

        elif safe_str_cmp(category, 'Package'):
            parser.add_argument('pizzas',
                                type=list,
                                required=False,
                                location='json',
                                help='A package needs a list of pizzas')
            parser.add_argument('complements',
                                type=list,
                                required=False,
                                location='json',
                                help='A package needs a list of complements')
            parser.add_argument('drinks',
                                type=list,
                                required=False,
                                location='json',
                                help='A package needs a list of drinks')
            parser.add_argument('sauces',
                                type=list,
                                required=False,
                                location='json',
                                help='A package needs a list of sauces')
            data = parser.parse_args()
            product = Package.find_by_name(data['name'])

            if product is None:
                product = Package(**data)
            else:
                product.price = data['price']
                product.units = data['units']
                if data['pizzas']:
                    product.pizzas = data['pizzas']
                if data['complements']:
                    product.pizzas = data['complements']
                if data['drinks']:
                    product.pizzas = data['drinks']
                if data['sauces']:
                    product.pizzas = data['sauces']

        else:
            return {'message': 'Invalid category name'}, 400
>>>>>>> 7aa93a5445c9ddec183559c448340e9a5aca848c

        product.save_to_db()
        product.refresh()
        return product.json()

<<<<<<< HEAD
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A product cannot have a blank name')

        data = parser.parse_args()
        product = Product.find_by_name(data['name'])

        if product is None:
            return {'message': "The product '{}' does not exist".format(data["name"])}

        return product.json()

    def delete(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A product cannot have a blank name')

        data = parser.parse_args()
        product = Product.find_by_name(data['name'])

        if product is None:
            return {'message': "The product '{}' does not exist or has already been deleted".format(data["name"])}
        else:
            product.delete_from_db()

=======
    # If no Authorization header is sent it throws an error 500, which needs to be handled hopefully by Nginx.
    # flask_jwt_extended.exceptions.NoAuthorizationError: Missing Authorization Header
    @jwt_required
    def get(self, category):

        claims = get_jwt_claims()
        if not claims['role']:
            return {'message': 'No authorization'}, 401

        product, data = validate_category(category)
        if product is None:
            return {'message': "The product '{}' does not exist".format(data["name"])}, 400
        return product.json()

    @admin_required
    def delete(self, category):
        product, data = validate_category(category)
        if product is None and data is None:
            return {'message': 'Invalid category name'}, 400
        elif product is None and data is not None:
            return {'message': "The product '{}' does not exist or has already been deleted".format(data["name"])}, 400
        else:
            product.delete_from_db()
>>>>>>> 7aa93a5445c9ddec183559c448340e9a5aca848c
        return {'message': "The product '{}' has been deleted".format(data["name"])}


# Retrieve a list of all the products
<<<<<<< HEAD
class Products(Resource):
    def get(self):
        pass
=======
class ProductsEndpoint(Resource):
    @jwt_required
    def get(self):
        return Products.json()
>>>>>>> 7aa93a5445c9ddec183559c448340e9a5aca848c
