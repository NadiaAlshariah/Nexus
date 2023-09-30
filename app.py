from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os


db = SQLAlchemy()
DB_NAME = "users_database.db"

app = Flask(__name__)
app.config.from_object(Config)
app.config["SECRET_KEY"] = "secret word"
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
db.init_app(app)


from models import User


def create_database(app):
    if not os.path.exists("Nexus/" + DB_NAME):
        db.create_all()


app.app_context().push()
create_database(app)

login_manager = LoginManager()
login_manager.login_view = "login"
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))
