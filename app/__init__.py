from flask import Flask 
from config import Config 

from flask_sqlalchemy import SQLAlchemy 
from flask_socketio import SocketIO 
from flask_basicauth import BasicAuth

from app.runs import RunTracker
from app.data import Info


app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)

socketio = SocketIO(app)
basic_auth = BasicAuth(app)
runTracker = RunTracker()
randData = Info()

print(app.config['SQLALCHEMY_DATABASE_URI'])

from app import models, routes, events
from app.models import Base 
db.Model = Base
