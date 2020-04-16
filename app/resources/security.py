from flask_jwt_extended import (create_access_token, jwt_refresh_token_required, get_jwt_identity,
                                create_refresh_token, fresh_jwt_required, get_jwt_claims)
from flask_restful import Resource, reqparse
from models.security import User
from werkzeug.security import safe_str_cmp


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

