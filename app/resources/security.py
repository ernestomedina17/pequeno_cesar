from flask_jwt_extended import create_access_token
from flask_restful import Resource, reqparse
from models.security import User
from werkzeug.security import safe_str_cmp


class LoginEndpoint(Resource):

    def post(self):
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
            return {"msg": "Bad username or password"}, 401

        access_token = create_access_token(identity=user)
        return {"access_token": access_token}, 200


