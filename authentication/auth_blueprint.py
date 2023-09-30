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
from app import app
from models import User
from flask_login import login_user, logout_user, login_required
import bcrypt
import os
import pathlib
import requests
from google.oauth2 import id_token
from google_auth_oauthlib.flow import Flow
from pip._vendor import cachecontrol
import google.auth.transport.requests
import uuid
from flask_session import Session
import msal
import authentication.app_config as app_config


auth = Blueprint("auth", __name__, template_folder="templates")
os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"


GOOGLE_CLIENT_ID = (
    "1012123546203-eld9a29hj7cm7leol3psbq9dg790d6ca.apps.googleusercontent.com"
)

client_secret_file = os.path.join(pathlib.Path(__file__).parent, "client_secret.json")

flow = Flow.from_client_secrets_file(
    client_secrets_file=client_secret_file,
    scopes=[
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/userinfo.email",
        "openid",
    ],
    redirect_uri="http://localhost:5000/authentication/signup_callback",
)


def _build_auth_code_flow(authority=None, scopes=None):
    return _build_msal_app(authority=authority).initiate_auth_code_flow(
        scopes or app_config.SCOPE_MICROSOFT,
        redirect_uri=url_for("auth.microsoft_callback", _external=True),
    )


def _build_msal_app(cache=None, authority=None):
    return msal.ConfidentialClientApplication(
        app_config.CLIENT_ID,
        authority=authority or app_config.AUTHORITY,
        client_credential=app_config.CLIENT_SECRET,
        token_cache=cache,
    )


@auth.route("/microsoft_login")
def microsoft_login():
    scopes = app_config.SCOPE

    flow = _build_auth_code_flow(scopes=scopes)

    session["microsoft_flow"] = flow
    return redirect(flow["auth_uri"])


@auth.route("/loginWithGoogle")
def loginWithGoogle():
    authorization_url, state = flow.authorization_url()
    session["state"] = state
    return redirect(authorization_url)


@auth.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        password = password.encode("utf-8")

        user = User.query.filter_by(email=email).first()
        if user:
            if bcrypt.checkpw(password, user.password):
                flash("logged in", category="success")
                login_user(user, remember=True)
                return redirect(
                    url_for("index")
                )  # i should change this later to the home
            else:
                flash("Password is incorrect", category="error")
        else:
            flash("Email doesn't exist", category="error")

    return render_template("login.html")


@auth.route("/signup", methods=["POST", "GET"])
def signup():
    if request.method == "POST":
        email = request.form.get("email")
        username = request.form.get("username")
        password1 = request.form.get("password1")
        password2 = request.form.get("password2")

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("email already have been used", category="error")
        elif not ("@" in email and "." in email):
            flash("email is invalid", category="error")
        elif username_exists:
            flash("username already exist .. try a new username", category="error")
        elif len(username) < 3:
            flash("username is less than 3 characters", category="error")
        elif password1 != password2:
            flash("passwords doesn't match", category="error")
        elif len(password1) < 8:
            flash("password is less than 8 characters", category="error")
        else:
            # encryption of password
            password = password1.encode("utf-8")
            salt = bcrypt.gensalt()
            encrypted_password = bcrypt.hashpw(password, salt)
            new_user = User(
                email=email,
                username=username,
                password=encrypted_password,
            )
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("User created!")
            return redirect(url_for("index"))  # i should change it to home page

    return render_template("signup.html")


@auth.route("/logout")
@login_required
def logout():
    try:
        requests.post(
            "https://oauth2.googleapis.com/revoke",
            params={"token": flow.credentials.token},
            headers={"content-type": "application/x-www-form-urlencoded"},
        )
        logout_user()
        return redirect(url_for("index"))
    except:
        logout_user()
        session.clear()
        return redirect(url_for("index"))


@auth.route("/signup_callback")
def signup_callback():
    flow.fetch_token(authorization_response=request.url)

    if not session["state"] == request.args["state"]:
        abort(500)  # State does not match!

    credentials = flow.credentials
    request_session = requests.session()
    cached_session = cachecontrol.CacheControl(request_session)
    token_request = google.auth.transport.requests.Request(session=cached_session)

    id_info = id_token.verify_oauth2_token(
        id_token=credentials._id_token, request=token_request, audience=GOOGLE_CLIENT_ID
    )

    session["google_id"] = id_info.get("sub")
    session["name"] = id_info.get("name")
    return redirect(url_for("index"))


@auth.route("/microsoft_callback")
def microsoft_callback():
    try:
        flow = session.get("microsoft_flow")

        result = _build_msal_app().acquire_token_by_auth_code_flow(flow, request.args)

        if "error" in result:
            return render_template("auth_error.html", result=result)

        session["user"] = result.get("id_token_claims")

    except ValueError:
        pass

    return redirect(url_for("index"))
