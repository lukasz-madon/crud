from flask import Flask
from flask import make_response


app = Flask(__name__, static_path='')

@app.route('/')
def index():
    return make_response(open('static/index.html').read())