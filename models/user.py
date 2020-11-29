from starlette.authentication import BaseUser

from . import db


class User(db.Model, BaseUser):
    __tablename__ = 'users'

    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String())
    avatar = db.Column(db.String())
    follow_to = db.Column(db.String())

    def is_authenticated(self) -> bool:
        return True

    def display_name(self) -> str:
        return self.username
