from flask import Flask
from datetime import datetime
from flask_jwt_extended import JWTManager
from WebApp.converter import convert_size

app = Flask(__name__)
app.config.from_pyfile('/WebApp/config.py')
jwt = JWTManager(app)

# Import functions in Jinja
app.jinja_env.globals.update(convert_size=convert_size, datetime=datetime, int=int)

from WebApp import routes
