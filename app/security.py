from flask_jwt_extended import (get_jwt_claims, verify_jwt_in_request, create_access_token,
                                jwt_refresh_token_required, get_jwt_identity, create_refresh_token,
                                fresh_jwt_required)
from flask_restful import Resource, reqparse
from functools import wraps
from metrics import metrics_req_latency, metrics_req_in_progress, metrics_req_count
from werkzeug.security import safe_str_cmp
from models.users import User
import base64


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return {'message': 'Forbidden'}, 403
        else:
            return fn(*args, **kwargs)
    return wrapper


def configure_JWTManager(jwt, tokens_blacklist):
    @jwt.user_identity_loader
    def user_identity_lookup(username):
        user = User.find_by_name(username)
        if user is None:
            return None
        return user.name

    @jwt.user_claims_loader
    def add_claims_to_access_token(username):
        user = User.find_by_name(username)
        if user is None:
            return None
        if user.is_admin():
            return {'role': 'admin'}  # PUT, GET & DELETE
        return {'role': 'consumer'}  # Only GETs

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        entry = tokens_blacklist.get(jti)
        if entry:
            return True
    return False


def get_user():
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help='A login cannot have a blank username')
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help='A login cannot have a blank password')

    # TODO: Figure out how to send and receive an encrypted password from Postman
    data = parser.parse_args()
    # TODO: Store/Retrieve encrypted passwords from the DB.
    user = User.find_by_name(data['username'])
    password = user.password
    if user is None or not safe_str_cmp(user.password, password):
        return None
    return user


class LoginEndpoint(Resource):
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def post(self):
        user = get_user()
        if user is None:
            metrics_req_count.labels(method='POST', endpoint='/login', status_code='401').inc()
            return {"message": "Bad username or password"}, 401
        metrics_req_count.labels(method='POST', endpoint='/login', status_code='200').inc()
        return {'fresh_token': create_access_token(identity=user.name, fresh=True)}, 200


class RefreshableTokenEndpoint(Resource):
    @fresh_jwt_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def post(self):
        metrics_req_count.labels(method='POST', endpoint='/refreshable', status_code='200').inc()
        return {'refresh_token': create_refresh_token(identity=get_jwt_identity(),
                                                      user_claims=get_jwt_claims())}, 200


class RefreshTokenEndpoint(Resource):
    @jwt_refresh_token_required
    @metrics_req_latency.time()
    @metrics_req_in_progress.track_inprogress()
    def post(self):
        metrics_req_count.labels(method='POST', endpoint='/refresh', status_code='200').inc()
        return {'access_token': create_access_token(identity=get_jwt_identity(),
                                                    fresh=False,
                                                    user_claims=get_jwt_claims())}, 200
