from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    request,
    flash,
    session,
    abort,
)
from app import db
from models import User, Post
from flask_login import login_required, current_user

user_bp = Blueprint("user", __name__, template_folder="templates")


@user_bp.route("/")
def user_profile(username):
    user = User.query.filter_by(username=username).first()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.date.desc()).all()
    if user:
        return render_template(
            "user.html", user=user, posts=posts, current_user=current_user
        )
    else:
        return "no user has this username"
