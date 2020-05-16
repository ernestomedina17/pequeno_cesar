from flask_jwt_extended import jwt_required, fresh_jwt_required
from flask_restful import Resource, reqparse
from security import admin_required
from werkzeug.security import safe_str_cmp
from models.users import User, Administrator
from metrics import metrics_req_latency, metrics_req_in_progress, metrics_req_count
import base64
import os
from cryptography.fernet import Fernet


def encrypt_password(password):
    # Secret files
    file_encryption_key = open(os.path.expanduser('/run/secrets/encryption_key'), 'rb')
    encryption_key = file_encryption_key.read()
    file_encryption_key.close()
    fer = Fernet(encryption_key)

    encoded_password = base64.b64encode(bytes(password, 'utf-8'))
    encrypted_password = fer.encrypt(encoded_password)

    return encrypted_password.strip().decode()


class UserEndpoint(Resource):
    @admin_required
    @fresh_jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
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
                user = Administrator(name=data['name'], password=encrypt_password(data['password']))
            else:
                user.password = encrypt_password(data['password'])

        elif safe_str_cmp(role, 'consumer'):
            user = User.find_by_name(data['name'])
            if user is None:
                user = User(name=data['name'], password=encrypt_password(data['password']))
            else:
                user.password = encrypt_password(data['password'])
        else:
            metrics_req_count.labels(method='PUT', endpoint='/user', status_code='400').inc()
            return {'message': 'Invalid role name'}, 400

        user.save_to_db()
        user.refresh()
        metrics_req_count.labels(method='PUT', endpoint='/user', status_code='200').inc()
        return user.json_full(), 200

    @admin_required
    @fresh_jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
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
                metrics_req_count.labels(method='DELETE', endpoint='/user', status_code='200').inc()
                return {'message': 'The user does not exist'}, 200
            elif safe_str_cmp(user.name, 'ernesto'):
                metrics_req_count.labels(method='DELETE', endpoint='/user', status_code='400').inc()
                return {'message': 'User ernesto cannot be deleted'}, 400
            else:
                user.delete_from_db()

        elif safe_str_cmp(role, 'consumer'):
            user = User.find_by_name(data['name'])
            if user is None:
                metrics_req_count.labels(method='DELETE', endpoint='/user', status_code='200').inc()
                return {'message': 'The user does not exist'}, 200
            else:
                user.delete_from_db()

        else:
            metrics_req_count.labels(method='DELETE', endpoint='/user', status_code='400').inc()
            return {'message': 'Invalid role name'}, 400

        metrics_req_count.labels(method='DELETE', endpoint='/user', status_code='200').inc()
        return {'message': "The user '{}' has been deleted".format(data["name"])}, 200

    @admin_required
    @jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
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
                metrics_req_count.labels(method='GET', endpoint='/user', status_code='200').inc()
                return {'message': 'The user does not exist'}, 200
            elif safe_str_cmp(user.name, 'ernesto'):
                metrics_req_count.labels(method='GET', endpoint='/user', status_code='400').inc()
                return {'message': 'User ernesto cannot be retrieved'}, 400

        elif safe_str_cmp(role, 'consumer'):
            user = User.find_by_name(data['name'])
            if user is None:
                metrics_req_count.labels(method='GET', endpoint='/user', status_code='200').inc()
                return {'message': 'The user does not exist'}, 200

        else:
            metrics_req_count.labels(method='GET', endpoint='/user', status_code='400').inc()
            return {'message': 'Invalid role name'}, 400

        metrics_req_count.labels(method='GET', endpoint='/user', status_code='200').inc()
        return user.json(), 200
