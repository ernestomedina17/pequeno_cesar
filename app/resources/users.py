from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_restful import Resource, reqparse
from security import admin_required
from werkzeug.security import safe_str_cmp
from models.users import User, Administrator
from metrics import metrics_req_latency, metrics_req_latency


class UserEndpoint(Resource):
    @admin_required
    @fresh_jwt_required
    @metrics_req_latency.time()
    def put(self, role):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A user cannot have a blank name')
        parser.add_argument('password',
                            type=str,
                            required=True,
                            help='A user cannot have a blank password')

        data = parser.parse_args()

        if safe_str_cmp(role, 'admin'):
            user = Administrator.find_by_name(data['name'])
            if user is None:
                user = Administrator(**data)
            else:
                user.password = data['password']

        elif safe_str_cmp(role, 'consumer'):
            user = User.find_by_name(data['name'])
            if user is None:
                user = User(**data)
            else:
                user.password = data['password']
        else:
            return {'message': 'Invalid role name'}, 400

        user.save_to_db()
        user.refresh()
        return user.json()

    @admin_required
    @fresh_jwt_required
    @metrics_req_latency.time()
    def delete(self, role):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A user cannot have a blank name')

        data = parser.parse_args()

        if safe_str_cmp(role, 'admin'):
            user = Administrator.find_by_name(data['name'])
            if user is None:
                return {'message': 'The user does not exist'}, 200
            elif safe_str_cmp(user.name, 'ernesto'):
                return {'message': 'User ernesto cannot be deleted'}, 400
            else:
                user.delete_from_db()

        elif safe_str_cmp(role, 'consumer'):
            user = User.find_by_name(data['name'])
            if user is None:
                return {'message': 'The user does not exist'}, 200
            else:
                user.delete_from_db()

        else:
            return {'message': 'Invalid role name'}, 400

        return {'message': "The user '{}' has been deleted".format(data["name"])}

    @admin_required
    @jwt_required
    @metrics_req_latency.time()
    def get(self, role):
        parser = reqparse.RequestParser()
        parser.add_argument('name',
                            type=str,
                            required=True,
                            help='A user cannot have a blank name')

        data = parser.parse_args()

        if safe_str_cmp(role, 'admin'):
            user = Administrator.find_by_name(data['name'])
            if user is None:
                return {'message': 'The user does not exist'}, 200
            elif safe_str_cmp(user.name, 'ernesto'):
                return {'message': 'User ernesto cannot be retrieved'}, 400

        elif safe_str_cmp(role, 'consumer'):
            user = User.find_by_name(data['name'])
            if user is None:
                return {'message': 'The user does not exist'}, 200

        else:
            return {'message': 'Invalid role name'}, 400

        return user.json()
