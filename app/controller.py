# -*- coding: Utf-8 -*

from flask import request
from app import app
from app.models import EPyTodoAPI

@app.route("/register", methods=["POST"])
def register():
    api = EPyTodoAPI()
    return api.register_user(request.json)

@app.route("/signin", methods=["POST"])
def login():
    api = EPyTodoAPI()
    return api.login_user(request.json)

@app.route("/signout", methods=["POST"])
def logout():
    api = EPyTodoAPI()
    return api.logout_user()

@app.route("/user", methods=["GET"])
def user():
    api = EPyTodoAPI()
    return api.get_user_infos()

# @app.route("/user/task/<int:id>", methods=["GET", "POST"])
# def task():
#     pass