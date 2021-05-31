#from app import app
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, current_user
#from model import User
#from playhouse.shortcuts import model_to_dict

class IndexResource(Resource):
    @jwt_required(optional=True)
    def get(self):
        if not current_user:
            return {'message': 'Not authenticated!'}, 401
        return jsonify(message='Hello from Flask!')

