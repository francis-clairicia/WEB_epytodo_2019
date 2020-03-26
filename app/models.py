# -*- coding: Utf-8 -*

import sys
import pymysql
from flask import jsonify, session
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASS, DATABASE_SOCK, DATABASE_USER

def connect_to_database(treatment_function):
    params = {
        "host": str(DATABASE_HOST),
        "user": str(DATABASE_USER),
        "passwd": str(DATABASE_PASS),
        "db": str(DATABASE_NAME),
        "unix_socket": str(DATABASE_SOCK),
    }
    def wrapper(api, *args, **kwargs):
        try:
            with pymysql.connect(**params) as cursor:
                cursor.execute("USE" + " " + params["db"])
                api.cursor = cursor
                json = treatment_function(api, *args, **kwargs)
        except Exception as e:
            print(f"Caught error: {e}", file=sys.stderr)
            json = jsonify(error="internal error")
        return json
    return wrapper

class EPyTodoAPI():
    def __init__(self):
        self.cursor = None

    @connect_to_database
    def register_user(self, user: dict):
        self.cursor.execute("SELECT username FROM user WHERE username='{username}'".format(**user))
        database_result = self.cursor.fetchall()
        if len(database_result) > 0:
            return jsonify(error="account already exists")
        self.cursor.execute("INSERT INTO user (username, password) VALUES ('{username}', '{password}')".format(**user))
        return jsonify(result="account created")

    @connect_to_database
    def login_user(self, user: dict):
        if "username" in session:
            return jsonify(error="already login to an account")
        self.cursor.execute("SELECT * FROM user WHERE username='{username}' AND password='{password}'".format(**user))
        database_result = self.cursor.fetchall()
        if len(database_result) == 0:
            return jsonify(error="login or password does not match")
        session["username"] = user["username"]
        return jsonify(result="signin successful")

    def logout_user(self):
        if "username" in session:
            session.pop("username", None)
        return jsonify(result="signout successful")

    @connect_to_database
    def get_user_infos(self):
        if "username" not in session:
            return jsonify(error="you must be logged in")
        username = session["username"]
        self.cursor.execute(f"SELECT * FROM user WHERE username='{username}'")
        database_result = self.cursor.fetchall()[0]
        result = {
            "user_id": database_result[0],
            "username": database_result[1],
            "password": database_result[2]
        }
        return jsonify(result=result)

    # @connect_to_database
    # def get_task_infos(self, task_id: int):
    #     if "username" not in session:
    #         return jsonify(error="you must be logged in")
    #     return jsonify(result="None")
        