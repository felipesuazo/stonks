from . import db


class Subscription(db.Model):
    __tablename__ = 'subscriptions'

    id = db.Column(db.String(), primary_key=True)
    type = db.Column(db.String())
    secret = db.Column(db.String())
    broadcaster_user_name = db.Column(db.String())
    broadcaster_user_id = db.Column(db.String())
    created_at = db.Column(db.DateTime())
