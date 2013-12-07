from flask.ext.restful import Resource
from flask import request, jsonify, g, url_for
from server import api
from server.app import config
from models import User


todos = { 
    "23": "task 23 data"
}

auth = HTTPBasicAuth()

@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token)
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password, config["SECRET_KEY"]):
            return False
    g.user = user
    return True

class TodoSimple(Resource):
    @auth.login_required
    def get(self, todo_id):
        return {todo_id: todos.get(todo_id, "task doesn't exist")}

class Users(object):
    """Users api"""
    def get(self, user_id):
    	user = User.query.get(id)
    	if not user:
        	abort(400)
    	return jsonify({"username": user.username })

    def post(self):
        username = request.json.get("username")
        password = request.json.get("password")
        if username is None or password is None:
            abort(400) # missing arguments
        if User.query.filter_by(username = username).first() is not None:
            abort(400) # existing user
        user = User(username = username)
        user.hash_password(password)
        db.session.add(user)
        db.session.commit()
        return jsonify({"username": user.username }), 201, {"Location": url_for("get_user", id = user.id, _external = True)}

class Token(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600, config["SECRET_KEY"])
        return jsonify({"token": token.decode("ascii"), "duration": 600 })

api.add_resource(TodoSimple, "/<string:todo_id>")
api.add_resource(Users, "/users/<int:id>")
api.add_resource(Token, "/token")
