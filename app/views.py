# -*- coding: Utf-8 -*

import os
from flask import render_template, send_from_directory, session
from app import app

@app.route("/", methods=["GET"])
@app.route("/index", methods=["GET"])
def index():
    return render_template("index.html", username=session.get("username", None))

@app.route("/favicon.ico", methods=["GET"])
def favicon():
    return send_from_directory(os.path.join(app.root_path, "static"), "img/favicon.ico", mimetype="image/vnd.microsoft.icon")

@app.route("/signup_page", methods=["GET"])
def register_form():
    return render_template("signup_page.html")

@app.route("/login_page", methods=["GET"])
def login_form():
    return render_template("login_page.html")