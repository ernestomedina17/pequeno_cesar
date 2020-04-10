from flask_jwt_extended import jwt_refresh_token_required, fresh_jwt_required
from flask_restful import Resource
from security import admin_required


class UserEndpoint(Resource):
    @admin_required
    @fresh_jwt_required
    def put(self):
        pass

    @admin_required
    @fresh_jwt_required
    def delete(self):
        pass

    @admin_required
    @jwt_refresh_token_required
    def get(self):
        pass
