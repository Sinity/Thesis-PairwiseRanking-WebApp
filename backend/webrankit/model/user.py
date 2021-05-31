from peewee import *
from .base import *
from passlib.hash import pbkdf2_sha256 as sha256

class User(UUIDModel):
    email = CharField(default='')
    password = CharField(default='')

    def is_admin(self):
        return email == 'ezo.dev@gmail.com'

    def set_password_hash(self, password_plaintext):
        self.password = sha256.hash(password_plaintext)
    def verify_password(self, password_candidate):
        try:
            return sha256.verify(password_candidate, self.password)
        except:
            return False

