import bcrypt
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
from app import db, app
from models import User, Upload
from flask_login import login_required, current_user
import os

settings = Blueprint("settings", __name__, template_folder="templates")


@settings.route("/")
@login_required
def settings_page():
    return render_template("settings.html")


@settings.route("/changeName", methods=["POST", "GET"])
@login_required
def changeName():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        if request.method == "POST":
            input_ = request.form.get("text")
            if input_ != "" and input_ != None:
                user.name = input_
                db.session.commit()
                flash("name has been changed")
    else:
        flash("error has occured")
    return redirect(url_for("settings.settings_page"))


@settings.route("/uploadProfilePicture", methods=["POST"])
@login_required
def uploadProfilePicture():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        if "file" not in request.files:
            flash("no file part")
            return redirect(request.referrer)
        file = request.files["file"]
        if file.name == "":
            flash("no image has been added")
            return redirect(request.referrer)
        if file:
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], file.filename))
            user.profile_picture = file.filename
            db.session.commit()
            flash("image has been uploaded")
            return redirect(request.referrer)
    flash("error has occured")
    return redirect(url_for("settings.settings_page"))


@settings.route("/changeBio", methods=["POST", "GET"])
@login_required
def changeBio():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        if request.method == "POST":
            input_ = request.form.get("text")
            if input_ != "" and input_ != None:
                user.bio = input_
                db.session.commit()
                flash("bio has been changes")
    else:
        flash("error has occured")
    return redirect(url_for("settings.settings_page"))


@settings.route("/changeUsername", methods=["POST", "GET"])
@login_required
def changeUsername():
    user = User.query.filter_by(username=current_user.username).first()
    if user:
        if request.method == "POST":
            input_ = request.form.get("text")
            if input_ != "" and input_ != None and input_ > 3:
                user.username = input_
                db.session.commit()
                flash("name has been changes")
    else:
        flash("error has occured")
    return redirect(url_for("settings.settings_page"))


@settings.route("/changePassword", methods=["POST", "GET"])
@login_required
def changePassword():
    password = request.form.get("password1")
    password = password.encode("utf-8")

    user = User.query.filter_by(username=current_user.username).first()
    if user != None:
        if user.password != None:
            if bcrypt.checkpw(password, user.password):
                password2 = request.form.get("password2")
                password3 = request.form.get("password3")
                if password2 == password3:
                    password = password2.encode("utf-8")
                    salt = bcrypt.gensalt()
                    encrypted_password = bcrypt.hashpw(password, salt)
                    user.password = encrypted_password
                    db.session.commit()
                    flash("password has been changed")
                else:
                    flash("new passwords doesnt match")
            else:
                flash("Ur old password doesnt match")

    return redirect(url_for("settings.settings_page"))
