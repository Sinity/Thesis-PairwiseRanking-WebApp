from flask import jsonify
from playhouse.shortcuts import model_to_dict
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
from model import Ranking, Item, Comparison
from uuid import UUID

class CompareResource(Resource):
    @jwt_required()
    def get(self, ranking_uid):
        ranking = Ranking.get_or_none(id=ranking_uid)
        if ranking is None:
            return {'message': f'Ranking `{uid}` not found.'}, 404
        if ranking.user.id != current_user.id:
            return {'message': f'Ranking belongs to another user.'}, 409

        model = ranking.get_pairwise_model()
        comp = model.next_comparison()
        item1 = Item.get_or_none(id=UUID(comp[0]))
        if item1 is None:
            return {'message': f'Item `{comp[0]}` not found'}, 404
        item2 = Item.get_or_none(id=UUID(comp[1]))
        if item2 is None:
            return {'message': f'Item `{comp[1]}` not found'}, 404

        items = []
        items.append({
            'id': item1.id,
            'label': item1.label,
            'img_url': item1.img_url})
        items.append({
            'id': item2.id,
            'label': item2.label,
            'img_url': item2.img_url})
        return jsonify(comparison=items)

    @jwt_required()
    def post(self, ranking_uid):
        ranking = Ranking.get_or_none(id=ranking_uid)
        if ranking is None:
            return {'message': f'Ranking `{uid}` not found'}, 404
        parser = reqparse.RequestParser(trim=True, bundle_errors=True)
        parser.add_argument('winitem')
        parser.add_argument('loseitem')
        data = parser.parse_args()

        id1 = UUID(data['winitem'])
        item1 = Item.get_or_none(id=id1)
        if item1 is None:
            return {'message': f'Item `{id1}` not found'}, 404
        id2 = UUID(data['loseitem'])
        item2 = Item.get_or_none(id=id2)
        if item2 is None:
            return {'message': f'Item `{id2}` not found'}, 404
        
        comp = Comparison.compare(item1, item2, item1.id)
        model = ranking.get_pairwise_model()
        return jsonify(coeff=str(model.coefficients),
                       comparison_count=len(ranking.comparisons),
                       comp=model_to_dict(comp))

