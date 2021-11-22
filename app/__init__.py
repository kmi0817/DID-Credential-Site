from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO, send

app = Flask(__name__)
app.config["SECRET_KEY"] = 'asd'
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db" # db name is data.db
db = SQLAlchemy(app)
socketio = SocketIO(app)

from app import routes