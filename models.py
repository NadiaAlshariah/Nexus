from app import db
from flask_login import UserMixin
from sqlalchemy import LargeBinary, func


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
