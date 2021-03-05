from peewee import *

db = SqliteDatabase('database.db')

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    id = AutoField()
    email = CharField()

class Ranking(BasModel):
    id = AutoField()
    user = ForeignKeyField(User, backref='rankings')

class Item(BaseModel):
    id = UUIDField(primary_key=True)
    ranking = ForeignKeyField(Ranking, backref='items')

class Comparison(BaseModel):
    id = AutoField()
    ranking = ForeignKeyField(Ranking, backref='comparisons')
    item1 = ForeignKeyField(Item, backref='comparisons')
    win1 = IntegerField()
    item2 = ForeignKeyField(Item, backref='comparisons')
    win2 = IntegerField()

