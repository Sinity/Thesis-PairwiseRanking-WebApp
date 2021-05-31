import uuid
from peewee import *
from app import db_wrapper

class BaseModel(db_wrapper.Model):
    pass

class UUIDModel(BaseModel):
    id = BinaryUUIDField(primary_key=True, default=uuid.uuid4)
