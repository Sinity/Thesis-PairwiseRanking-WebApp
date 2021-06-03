from flask import jsonify
from playhouse.shortcuts import model_to_dict
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from model import Ranking, Item, Comparison
from math import isnan

class RankingResource(Resource):
    @jwt_required()
    def get(self, uid):
        ranking = Ranking.get_or_none(id=uid)
        if ranking is None:
            return {'message': f'Ranking `{uid}` not found'}, 404
        if ranking.user.id != current_user.id:
            return {'message': f'Ranking belongs to another user'}, 409
        ranking_json = {'id': ranking.id,
                        'name': ranking.name,
                        'datasource': ranking.datasource,
                        'item_count': len(ranking.items),
                        'comp_count': len(ranking.comparisons)}
        if len(ranking.items) != 0:
            model = ranking.get_pairwise_model()
            ranking_json['items'] = [] 
            for item in ranking.items:
                coeff = model.coeff_by_id(str(item.id))
                stderr = coeff[1]
                if isnan(stderr):
                    stderr = 0
                idx = model.coefficients.index(coeff)
                rating = (idx / len(model.coefficients)) * 10
                ranking_json['items'].append({
                    'id': item.id,
                    'label': item.label,
                    'img_url': item.img_url,
                    'init_rating': item.init_rating,
                    'curr_rating': round(rating, 2),
                    'stderr': round(stderr, 2)})
        return jsonify(ranking=ranking_json)

    @jwt_required()
    def post(self, uid):
        ranking = Ranking.get_or_none(id=uid)
        if ranking is None:
            return {'message': f'Ranking `{uid}` not found'}, 404
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('anilist_username')
        parser.add_argument('anilist_statuses', action="append")
        parser.add_argument('steam_id')
        data = parser.parse_args()
        if ranking.datasource == 'anilist':
            ranking.add_items_from_anilist(data['anilist_username'], data['anilist_statuses'])
        elif ranking.datasource == 'steam':
            ranking.add_items_from_steam(data['steam_id'])
        return jsonify(message=f'Now ranking has {len(ranking.items)} items.')

    @jwt_required()
    def delete(self, uid):
        deleted_rows = Ranking.get(Ranking.id == uid).delete_instance()
        return jsonify(message=f'Deleted ({deleted_rows}) rankings.')

    @jwt_required()
    def put(self, uid):
        ranking = Ranking.get_or_none(Ranking.id == uid)
        if ranking is None:
            return {'message': f'Ranking `{uid}` not found'}, 404
        parser = reqparse.RequestParser(trim=True)
        parser.add_argument('name')
        args = parser.parse_args()
        if 'name' in args:
            ranking.name = args['name']
        ranking.save()
        return jsonify(message=f'Ranking {ranking.id} was modified')


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
        ranking_dicts = []
        for ranking in user_rankings:
            ranking_dicts.append({'id': ranking.id,
                                  'name': ranking.name,
                                  'datasource': ranking.datasource,
                                  'item_count': len(ranking.items)})
        return jsonify(rankings=ranking_dicts)

