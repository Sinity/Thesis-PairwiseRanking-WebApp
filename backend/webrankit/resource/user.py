from flask import jsonify
from playhouse.shortcuts import model_to_dict
from flask_restful import Resource, reqparse
from model import User
from flask_jwt_extended import jwt_required, current_user
from .auth import admin_required

class UserResource(Resource):
    @admin_required
    def get(self, uid):
        usr = User.get_or_none(id=uid)
        if usr is not None:
            return model_to_dict(usr)
        return {'message': f'User `{uid}` not found'}, 404

    @admin_required
    def delete(self, uid):
        query = User.delete(id=uid)
        deleted_rows = query.execute()
        return jsonify(message=f'Deleted ({deleted_rows}) users')

    @admin_required
    def put(self, uid):
        usr = User.get_or_none(id=uid)
        if usr is None:
            return {'message': f'User `{uid}` not found'}, 404
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('email')
        parser.add_argument('password')
        args = parser.parse_args()
        if 'email' in args:
            usr.email = args['email']
        if 'password' in args:
            usr.set_password_hash(args['password'])
        usr.save()
        return model_to_dict(usr)


class UserCollectionResource(Resource):
    #@admin_required
    def post(self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('email', help = 'This field cannot be blank', required = True)
        parser.add_argument('password', help = 'This field cannot be blank', required = True)
        data = parser.parse_args()
        if User.get_or_none(email = data['email']) is not None:
            return {'message': f"User '{data['email']}' already exists."}, 409
        usr = User.create(email = data['email'])
        usr.set_password_hash(data['password'])
        usr.save()
        return jsonify(message=f'User {usr.email} was created, id={usr.id}')

    @admin_required
    def get(self):
        users = User.select()
        user_dicts = list(users.dicts())
        return jsonify(users=user_dicts)

    @admin_required
    def delete(self):
        query = User.delete()
        deleted_rows = query.execute()
        return jsonify(message=f'Deleted all ({deleted_rows}) users')

