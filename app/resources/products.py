from flask_restful import Resource, reqparse
from models.products import Product
from flask_jwt import jwt_required


# CRUD Product - API Endpoint
class ProductEndpoint(Resource):

    def put(self):
        parser = reqparse.RequestParser()
        #  pizza: crazy crunch, pepperoni clasica, 3 meat treat, ultimate supreme, hula hawaiian, queso, deep!deep! dish
        #  complementos: crazy bread relleno, crazy bread, italian cheese bread, caesar wings
        #  drinks: pepsi 2L
        #  salsas: crazy sauce
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A product cannot have a blank name')
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help='A product cannot have a blank price')
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
        parser.add_argument('units',
                            type=int,
                            required=False,
                            help='Set the quantity of units')

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

        product.save_to_db()
        product.refresh()
        return product.json()

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

        return {'message': "The product '{}' has been deleted".format(data["name"])}


# Retrieve a list of all the products
class Products(Resource):
    def get(self):
        pass
