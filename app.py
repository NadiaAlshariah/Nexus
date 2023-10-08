from flask import Flask, session, flash, redirect, url_for
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from flask_migrate import Migrate



db = SQLAlchemy()
DB_NAME = "users_database.db"

app = Flask(__name__)
app.config.from_object(Config)
app.config["SECRET_KEY"] = "secret word"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
app.config["UPLOAD_FOLDER"] = "static/uploads"
db.init_app(app)

migrate = Migrate(app, db)

from models import User, Comment, LikedPost, Post


def create_database(app):
    if not os.path.exists("Nexus/" + DB_NAME):
        db.create_all()


app.app_context().push()
create_database(app)

login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


from collections import Counter


def get_top_interests_and_update(user_id):
    user = User.query.get(user_id)

    if user is None:
        return []

    posts = Post.query.filter_by(user=user).order_by(Post.date.desc()).limit(20).all()

    comments = (
        Comment.query.filter_by(user_id=user.id)
        .order_by(Comment.date.desc())
        .limit(20)
        .all()
    )

    likes = (
        LikedPost.query.filter_by(user_id=user.id)
        .order_by(LikedPost.id.desc())
        .limit(20)
        .all()
    )

    interests = []
    for post in posts:
        topic = post.topic
        if topic:
            interests.append(post.topic)

    for comment in comments:
        post = comment.post
        topic = post.topic
        if topic:
            interests.append(topic)

    for like in likes:
        post = like.post
        topic = post.topic
        if topic:
            interests.append(topic)

    interest_counts = Counter(interests)
    top_interest = interest_counts.most_common(1)[0][0] if interest_counts else None

    user.top_interest = top_interest
