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
from models import User
from flask_login import login_required, current_user

settings = Blueprint("settings", __name__, template_folder="templates")


@settings.route("/")
@login_required
def settings_page():
    return render_template("settings.html")


@settings.route("/changeName")
@login_required
def changeName():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.name = "placeholder for new name"
        db.session.commit()
        flash("name has been changes")
    else:
        flash("error has occured")
    return redirect(url_for("settings.settings_page"))


@settings.route("/uploadProfilePicture")
@login_required
def uploadProfilePicture():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.name = "placeholder for new name"
        db.session.commit()
        flash("name has been changes")
    else:
        flash("error has occured")
    return redirect(url_for("settings.settings_page"))


@settings.route("/changeBio")
@login_required
def changeBio():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.name = "placeholder for new name"
        db.session.commit()
        flash("name has been changes")
    else:
        flash("error has occured")
    return redirect(url_for("settings.settings_page"))


@settings.route("/changeUsername")
@login_required
def changeUsername():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.name = "placeholder for new name"
        db.session.commit()
        flash("name has been changes")
    else:
        flash("error has occured")
    return redirect(url_for("settings.settings_page"))


@settings.route("/changePassword")
@login_required
def changePassword():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        user.name = "placeholder for new name"
        db.session.commit()
        flash("name has been changes")
    else:
        flash("error has occured")
    return redirect(url_for("settings.settings_page"))
