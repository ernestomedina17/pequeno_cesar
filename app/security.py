from flask_jwt_extended import get_jwt_claims, verify_jwt_in_request
from functools import wraps


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
