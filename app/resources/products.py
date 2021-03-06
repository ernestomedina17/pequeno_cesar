from werkzeug.security import safe_str_cmp
from flask_restful import Resource, reqparse
from models.products import Pizza, Complement, Drink, Sauce, Package, Products
from flask_jwt_extended import get_jwt_claims, fresh_jwt_required, jwt_refresh_token_required, jwt_required
from security import admin_required
from metrics import metrics_req_latency, metrics_req_in_progress, metrics_req_count


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


# CRUD Product - API Endpoint
class ProductEndpoint(Resource):

    @admin_required
    @fresh_jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def put(self, category):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A product cannot have a blank name')
        parser.add_argument('price',
                            type=float,
                            required=True,
                            help='A product cannot have a blank price')
        parser.add_argument('units',
                            type=int,
                            required=False,
                            help='Set the quantity of units')

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
            metrics_req_count.labels(method='PUT', endpoint='/product', status_code='400').inc()
            return {'message': 'Invalid category name'}, 400

        product.save_to_db()
        product.refresh()
        metrics_req_count.labels(method='PUT', endpoint='/product', status_code='200').inc()
        return product.json()

    # If no Authorization header is sent it throws an error 500, which needs to be handled hopefully by Nginx.
    # flask_jwt_extended.exceptions.NoAuthorizationError: Missing Authorization Header
    @jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def get(self, category):
        claims = get_jwt_claims()
        if not claims['role']:
            metrics_req_count.labels(method='GET', endpoint='/product', status_code='401').inc()
            return {'message': 'No authorization'}, 401

        product, data = validate_category(category)
        if product is None:
            metrics_req_count.labels(method='GET', endpoint='/product', status_code='400').inc()
            return {'message': "The product '{}' does not exist".format(data["name"])}, 400
        metrics_req_count.labels(method='GET', endpoint='/product', status_code='200').inc()
        return product.json()

    @admin_required
    @fresh_jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def delete(self, category):
        product, data = validate_category(category)
        if product is None and data is None:
            metrics_req_count.labels(method='DELETE', endpoint='/product', status_code='400').inc()
            return {'message': 'Invalid category name'}, 400
        elif product is None and data is not None:
            metrics_req_count.labels(method='DELETE', endpoint='/product', status_code='400').inc()
            return {'message': "The product '{}' does not exist or has already been deleted".format(data["name"])}, 400
        else:
            product.delete_from_db()
        metrics_req_count.labels(method='DELETE', endpoint='/product', status_code='200').inc()
        return {'message': "The product '{}' has been deleted".format(data["name"])}, 200


# Retrieve a list of all the products
class ProductsEndpoint(Resource):
    @jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def get(self):
        metrics_req_count.labels(method='GET', endpoint='/products', status_code='200').inc()
        return Products.json()
