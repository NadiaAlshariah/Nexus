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
    posts = db.relationship("Post", backref="user")
    comments = db.relationship("Comment", backref="user")
    friends = db.relationship(
        "User",
        secondary="friendship",
        primaryjoin="User.id == Friendship.user_id",
        secondaryjoin="User.id == Friendship.friend_id",
        backref="user_friends",
    )
    liked_posts = db.relationship("LikedPost", backref="user", lazy=True)
    interests = db.relationship("UserInterest", back_populates="user")
    top_interest = db.Column(db.String(80))


class Interest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)


class UserInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    interest_id = db.Column(db.Integer, db.ForeignKey("interest.id"), nullable=False)

    user = db.relationship("User", backref="user_interests")
    interest = db.relationship("Interest")


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    topic = db.Column(db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    comments = db.relationship("Comment", backref="post")
    likes = db.relationship("LikedPost", back_populates="post")


class LikedPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
    post = db.relationship("Post", back_populates="likes")


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(10000))
    date = db.Column(db.DateTime(timezone=True), default=func.now())
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id", ondelete="CASCADE"), nullable=False
    )
    post_id = db.Column(
        db.Integer, db.ForeignKey("post.id", ondelete="CASCADE"), nullable=False
    )
