# -*- coding: Utf-8 -*

import sys
import hashlib
import pymysql
from flask import jsonify, session
from config import DATABASE_HOST, DATABASE_NAME, DATABASE_PASS, DATABASE_SOCK, DATABASE_USER

def encrypt_string(string: str):
    return hashlib.sha512(string.encode()).hexdigest()

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
        user["password"] = encrypt_string(user["password"])
        self.cursor.execute("SELECT username FROM user WHERE username='{username}'".format(**user))
        database_result = self.cursor.fetchall()
        if len(database_result) > 0:
            return jsonify(error="account already exists")
        self.cursor.execute("INSERT INTO user (username, password) VALUES ('{username}', '{password}')".format(**user))
        return jsonify(result="account created")

    @connect_to_database
    def login_user(self, user: dict):
        if "username" in session:
            return jsonify(error="already logged to an account")
        user["password"] = encrypt_string(user["password"])
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
        self.cursor.execute(f"SELECT user_id, password FROM user WHERE username='{username}'")
        user_id, password = self.cursor.fetchall()[0]
        result = {
            "user_id": user_id,
            "username": username,
            "password": password
        }
        return jsonify(result=result)

    @connect_to_database
    def add_task(self, task_infos: dict):
        if "username" not in session:
            return jsonify(error="you must be logged in")
        username = session["username"]
        self.cursor.execute(f"SELECT user_id FROM user WHERE username='{username}'")
        user_id = self.cursor.fetchall()[0][0]
        self.cursor.execute("INSERT INTO task (title) VALUES ('{title}')".format(**task_infos))
        title = task_infos["title"]
        self.cursor.execute(f"SELECT task_id FROM task WHERE title='{title}'")
        task_id = self.cursor.fetchall()[-1][0]
        self.cursor.execute(f"INSERT INTO user_has_task (fk_user_id, fk_task_id) VALUES ({user_id}, {task_id})")
        return jsonify(result="new task added")

    @connect_to_database
    def get_all_user_tasks(self):
        if "username" not in session:
            return jsonify(error="you must be logged in")
        username = session["username"]
        tasks = list()
        self.cursor.execute(f"SELECT task.* FROM ((user_has_task JOIN user ON (user.username='{username}' AND user_has_task.fk_user_id=user.user_id)) JOIN task ON user_has_task.fk_task_id=task.task_id)")
        for task_id, title, begin, end, status in self.cursor.fetchall():
            task = dict()
            task[task_id] = {
                "title": title,
                "begin": begin.strftime("%Y-%m-%d %H:%M:%S"),
                "end": end if end is None else end.strftime("%Y-%m-%d %H:%M:%S"),
                "status": status
            }
            tasks.append(task)
        return jsonify(result={"tasks": tasks})

    @connect_to_database
    def get_task_infos(self, task_id: int):
        if "username" not in session:
            return jsonify(error="you must be logged in")
        self.cursor.execute(f"SELECT title, begin, end, status FROM task WHERE task_id={task_id}")
        database_result = self.cursor.fetchall()
        if len(database_result) == 0:
            return jsonify(error="task id does not exist")
        title, begin, end, status = database_result[0]
        task = {
            "title": title,
            "begin": begin.strftime("%Y-%m-%d %H:%M:%S"),
            "end": end if end is None else end.strftime("%Y-%m-%d %H:%M:%S"),
            "status": status
        }
        return jsonify(result=task)

    @connect_to_database
    def delete_task(self, task_id: int):
        if "username" not in session:
            return jsonify(error="you must be logged in")
        self.cursor.execute(f"SELECT * FROM task WHERE task_id={task_id}")
        database_result = self.cursor.fetchall()
        if len(database_result) == 0:
            return jsonify(error="task id does not exist")
        self.cursor.execute(f"DELETE FROM user_has_task WHERE fk_task_id={task_id}")
        self.cursor.execute(f"DELETE FROM task WHERE task_id={task_id}")
        return jsonify(result="task deleted")

    @connect_to_database
    def update_task(self, task_id: int, new_values: dict):
        if "username" not in session:
            return jsonify(error="you must be logged in")
        self.cursor.execute(f"SELECT * FROM task WHERE task_id={task_id}")
        database_result = self.cursor.fetchall()
        if len(database_result) == 0:
            return jsonify(error="task id does not exist")
        keywords = {key: f"'{value}'" for key, value in new_values.items()}
        if keywords["begin"] == keywords["end"]:
            keywords["end"] = "null"
        keywords["task_id"] = task_id
        self.cursor.execute("UPDATE task SET title={title}, begin={begin}, end={end}, status={status} WHERE task_id={task_id}".format(**keywords))
        return jsonify(result="update done")