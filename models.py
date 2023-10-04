from app import db
from flask_login import UserMixin
from sqlalchemy import LargeBinary, func


class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    friend_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    external_id = db.Column(db.String(150), unique=True)
    e_mail = db.Column(db.String(145), unique=False)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(LargeBinary)
    name = db.Column(db.String(150))
    bio = db.Column(db.String(500))
    location = db.Column(db.String(150))
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
    external = db.Column(db.Boolean)
    posts = db.relationship("Post")
    friends = db.relationship(
        "User",
        secondary="friendship",
        primaryjoin="User.id == Friendship.user_id",
        secondaryjoin="User.id == Friendship.friend_id",
        backref="user_friends",
    )


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    text_type = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
