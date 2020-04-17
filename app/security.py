from flask_jwt_extended import (get_jwt_claims, verify_jwt_in_request, jwt_required, get_raw_jwt,
                                create_access_token, jwt_refresh_token_required, get_jwt_identity,
                                create_refresh_token, fresh_jwt_required)
from flask_restful import Resource, reqparse
from functools import wraps
from werkzeug.security import safe_str_cmp
from models.users import User


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

    @jwt.expired_token_loader
    def my_expired_token_callback(expired_token):
        token_type = expired_token['type']
        return {
                   "status": 412,
                   "msg": "The {} token has expired".format(token_type)
               }, 412

    @jwt.invalid_token_loader
    def invalid_token_callback():
        return {'description': 'Signature verification failed.',
                'error': 'invalid_token'}, 401

    @jwt.unauthorized_loader
    def missing_token_callback():
        return {'description': 'Request does not contain an access token.',
                'error': 'authorization_required'}, 401

    @jwt.needs_fresh_token_loader
    def token_not_fresh_callback():
        return {'description': 'The token is not fresh',
                'error': 'fresh_token_required'}, 401

    @jwt.revoked_token_loader
    def revoked_token_callback():
        return {'description': 'The token has been revoked.',
                'error': 'token_revoked'}, 401

    @jwt.token_in_blacklist_loader
    def check_if_token_in_blacklist(decrypted_token):
        jti = decrypted_token['jti']
        entry = tokens_blacklist.get(jti)
        if entry:
            return True
    return False


# Blacklist Refreshed Access Tokens, can be used for Fresh tokens too.
class LogoutEndpoint(Resource):
    def __init__(self, tokens_blacklist, access_expires):
        self.tokens_blacklist = tokens_blacklist
        self.access_expires = access_expires

    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        self.tokens_blacklist.setex(name=jti, time=self.access_expires, value=jti)
        return {"message": "Successfully logged out2"}, 200


# Blacklist Refresh tokens.
class LogoutRefreshEndpoint(Resource):
    def __init__(self, tokens_blacklist, refresh_expires):
        self.tokens_blacklist = tokens_blacklist
        self.refresh_expires = refresh_expires

    @jwt_refresh_token_required
    def post(self):
        jti = get_raw_jwt()['jti']
        self.tokens_blacklist.setex(name=jti, time=self.refresh_expires, value=jti)
        return {"message": "Successfully logged out"}, 200


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

    data = parser.parse_args()
    user = User.find_by_name(data['username'])

    if user is None or not safe_str_cmp(user.password, data['password']):
        return None
    return user


class LoginEndpoint(Resource):
    def post(self):
        user = get_user()
        if user is None:
            return {"message": "Bad username or password"}, 401
        return {'fresh_token': create_access_token(identity=user.name, fresh=True)}


class RefreshableTokenEndpoint(Resource):
    @fresh_jwt_required
    def post(self):
        return {'refresh_token': create_refresh_token(identity=get_jwt_identity(),
                                                      user_claims=get_jwt_claims())}, 200


class RefreshTokenEndpoint(Resource):
    @jwt_refresh_token_required
    def post(self):
        return {'access_token': create_access_token(identity=get_jwt_identity(),
                                                    fresh=False,
                                                    user_claims=get_jwt_claims())}, 200

