from flask.ext.restful import Resource
from flask import request, jsonify, g, url_for, abort, make_response
from flask.ext.httpauth import HTTPBasicAuth
from flask.ext.restful import Api

from models import User, db


todos = { 
    "23": "task 23 data"
}

auth = HTTPBasicAuth()
api = Api()


@auth.verify_password
def verify_password(username_or_token, password):
    # first try to authenticate by token
    user = User.verify_auth_token(username_or_token, api.app.config["SECRET_KEY"])
    if not user:
        # try to authenticate with username/password
        user = User.query.filter_by(username = username_or_token).first()
        if not user or not user.verify_password(password, api.app.config["SECRET_KEY"]):
            return False
    g.user = user
    return True

class Tasks(Resource):
    @auth.login_required
    def get(self, todo_id):
        return {todo_id: todos.get(todo_id, "task doesn't exist")}

class Users(Resource):
    """Users api"""
    def get(self, id):
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
        res = make_response(jsonify({"username": user.username }), 201)
        res.headers["Location"] = api.url_for(self, id = user.id, _external = True)
        return res

class Token(Resource):
    @auth.login_required
    def get(self):
        token = g.user.generate_auth_token(600, api.app.config["SECRET_KEY"])
        return jsonify({"token": token.edcode("ascii"), "duration": 600 })
