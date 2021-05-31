from flask import Flask
app = Flask(__name__)

from flask_cors import CORS
CORS(app)

from flask_jwt_extended import JWTManager
app.config['JWT_SECRET_KEY'] = 'jwt-secret-string'
jwt = JWTManager(app)

#app.config.from_object('config.Configuration')
#app.config['DATABASE'] = 'sqlite:////database.db'

from playhouse.flask_utils import FlaskDB
from peewee import SqliteDatabase
db = SqliteDatabase('/home/sinity/dev/pwrank/db')
db_wrapper = FlaskDB(app, db)

from flask_restful import Api
from resource import *
api = Api(app)
api.add_resource(IndexResource, '/', '/greeting')
api.add_resource(AuthResource, '/auth')
api.add_resource(UserResource, '/auth/user/<uuid:uid>')
api.add_resource(UserCollectionResource, '/auth/user')
api.add_resource(RankingResource, '/ranking/<uuid:uid>')
api.add_resource(RankingCollectionResource, '/ranking')
