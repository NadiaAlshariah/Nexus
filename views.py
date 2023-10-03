from flask import Blueprint, render_template, redirect, url_for, request, flash
from app import app
from flask_login import login_required


@app.route("/")
def index():
    return render_template("index.html")
