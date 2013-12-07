import os
from flask import Flask, abort, request, jsonify, g, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.httpauth import HTTPBasicAuth
from flask import make_response
from flask.ext.restful import Api


app = Flask(__name__, static_url_path="")
app.config.from_pyfile("settings.cfg")

api = Api(app, prefix=app.config["BASE_API_URL"])

db = SQLAlchemy(app)

@app.route("/")
def index():
    return make_response(open("static/index.html").read())