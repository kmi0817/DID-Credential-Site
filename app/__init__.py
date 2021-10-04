from flask import Flask
# from app import routes

app = Flask(__name__)
app.config["SECRET_KEY"] = 'asd'

from app import routes