from app import db
from flask_login import UserMixin
from sqlalchemy import LargeBinary, func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    username = db.Column(db.String(150), unique=True)
    password = db.Column(LargeBinary)
    date_created = db.Column(db.DateTime(timezone=True), default=func.now())
