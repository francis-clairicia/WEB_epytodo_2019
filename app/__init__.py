# -*- coding: Utf-8 -*

import random
import string
from flask import Flask

app = Flask(__name__)
app.config.from_object("config")
app.secret_key = "".join(random.sample(string.ascii_letters + string.digits, 20))

from app import views
from app import controller