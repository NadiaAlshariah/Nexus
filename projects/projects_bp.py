from flask import Blueprint, render_template

projects_bp = Blueprint("projects", __name__, template_folder="templates")

@projects_bp.route("/")
def projects():
    return render_template("index.html")