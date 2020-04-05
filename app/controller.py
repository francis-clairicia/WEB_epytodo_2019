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

@app.route("/user/task", methods=["GET"])
def tasks():
    api = EPyTodoAPI()
    return api.get_all_user_tasks()

@app.route("/user/task/<int:id>", methods=["GET", "POST"])
def get_or_update_task(id: int):
    api = EPyTodoAPI()
    if request.method == "POST":
        return api.update_task(id, request.json)
    return api.get_task_infos(id)

@app.route("/user/task/add", methods=["POST"])
def add_task():
    api = EPyTodoAPI()
    return api.add_task(request.json)

@app.route("/user/task/del/<int:id>", methods=["POST"])
def delete_task(id: int):
    api = EPyTodoAPI()
    return api.delete_task(id)