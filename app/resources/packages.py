from flask_restful import Resource, reqparse
from models.products import Product, Products
from flask_jwt import jwt_required


# CRUD Product - API Endpoint
class PackageEndpoint(Resource):
    #  paquetes: comida completa, fiesta, crazy_combo
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A package cannot have a blank name')
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help='A package cannot have a blank price')
        parser.add_argument('products',
                            type=list,
                            required=True,
                            location='json',
                            help='A package cannot have a blank list of products')

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
class PackagesEndpoint(Resource):
    def get(self):
        return Products.json()
