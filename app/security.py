from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request
from functools import wraps
from flask import jsonify
from app import jwt


@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.name


@jwt.user_claims_loader
def add_claims_to_access_token(user):
    if user.is_admin():
        return {'role': 'admin'}
    return {'role': 'peasant'}


def admin_required(fn):
    @wraps(fn)
    def wrapper(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt_claims()
        if claims['role'] != 'admin':
            return jsonify(msg='Forbidden'), 403
        else:
            return fn(*args, **kwargs)
    return wrapper
