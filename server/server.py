from flask import Flask
from flask import make_response, send_file
from models import db
from api import api, Tasks, Users, Token


app = Flask(__name__, static_url_path="")
app.config.from_pyfile("settings.cfg")
db.init_app(app)
api.init_app(app)
api.prefix = api.app.config["BASE_API_URL"]
api.add_resource(Tasks, "/tasks/<string:todo_id>")
api.add_resource(Users, "/users", "/users/<int:id>")
api.add_resource(Token, "/token")

@app.route("/")
def index():
    if app.config["DEBUG"]:
        return make_response(open("../client/dist/index.html").read())
    else:
        return send_file(open("static/index.html").read())
