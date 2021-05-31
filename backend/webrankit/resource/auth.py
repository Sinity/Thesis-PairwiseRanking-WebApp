from app import jwt
from flask import jsonify
from playhouse.shortcuts import model_to_dict
from flask_restful import Resource, reqparse
from model import User
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, current_user
from uuid import UUID

@jwt.user_identity_loader
def user_identity_lookup(user_model_instance):
    return user_model_instance.id

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    user_id_from_token = jwt_data["sub"]
    return User.get_or_none(id=UUID(user_id_from_token))

def admin_required(func):
    @jwt_required()
    def wrapper(*args, **kwargs):
        if not current_user.is_admin():
            return {'message': 'Access denied, admin only'}, 403
        return func(*args, **kwargs)
    return wrapper

class AuthResource(Resource):
    @jwt_required(refresh=True)
    def get(self):
        token = create_access_token(identity=current_user)
        return jsonify(access_token=token)

    def post(self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('email', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()
        user = User.get_or_none(email = data['email'])
        if user is None:
            return {'message': 'Auth failed; no such user.'}, 401
        if not user.verify_password(data['password']):
            return {'message': 'Auth failed; password mismatch.'}, 401
        atoken = create_access_token(identity=user)
        rtoken = create_refresh_token(identity=user)
        identity = {'email': user.email, 'id': user.id}
        return jsonify(identity=identity, access_token=atoken, refresh_token=rtoken)

