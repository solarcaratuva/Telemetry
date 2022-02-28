from flask import Flask 
from config import Config 

from flask_sqlalchemy import SQLAlchemy 
from flask_socketio import SocketIO 
from flask_basicauth import BasicAuth

app = Flask(__name__)
app.config.from_object(Config)
app.static_folder = 'static'
db = SQLAlchemy(app)

socketio = SocketIO(app)
basic_auth = BasicAuth(app)

print(app.config['SQLALCHEMY_DATABASE_URI'])

from app import models, routes, events
from app.models import Base 
db.Model = Base

db.create_all()
