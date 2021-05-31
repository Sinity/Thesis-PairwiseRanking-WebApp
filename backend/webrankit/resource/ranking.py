from flask import jsonify
from playhouse.shortcuts import model_to_dict
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from model import Ranking, Item, Comparison

class RankingResource(Resource):
    @jwt_required()
    def get(self, uid):
        ranking = Ranking.get_or_none(id=uid)
        if ranking is not None:
            return model_to_dict(ranking)
        if ranking.user is not current_user:
            return {'message': f'Ranking doesnt belong to user'}, 409
        return {'message': f'Ranking `{uid}` not found'}, 404

    @jwt_required()
    def delete(self, uid):
        query = Ranking.delete(id=uid)
        deleted_rows = query.execute()
        return jsonify(message=f'Deleted ({deleted_rows}) rankings')

    # @jwt_required()
    # def put(self, uid):
    #     usr = User.get_or_none(id=uid)
    #     if usr is None:
    #         return {'message': f'User `{uid}` not found'}, 404
    #     parser = reqparse.RequestParser(trim=True)
    #     parser.add_argument('email')
    #     parser.add_argument('password')
    #     args = parser.parse_args()
    #     if 'email' in args:
    #         usr.email = args['email']
    #     if 'password' in args:
    #         usr.set_password_hash(args['password'])
    #     usr.save()
    #     return model_to_dict(usr)


class RankingCollectionResource(Resource):
    @jwt_required()
    def post(self):
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('name')
        parser.add_argument('source')
        data = parser.parse_args()
        if Ranking.get_or_none(Ranking.name == data['name']) is not None:
            return {'message': f"Ranking with such name already exists"}, 409
        ranking = Ranking.create(user=current_user.id, name=data['name'], datasource=data['source'])
        return jsonify(message=f'Ranking {ranking.name} was created, id={ranking.id}')

    @jwt_required()
    def get(self):
        user_rankings = Ranking.select().where(Ranking.user == current_user.id)
        ranking_dicts = list(user_rankings.dicts())
        return jsonify(rankings=ranking_dicts)

    # @jwt_required()
    # def delete(self):
    #     query = User.delete()
    #     deleted_rows = query.execute()
    #     return jsonify(message=f'Deleted all ({deleted_rows}) users')

