import time
from flask import Flask
from flask_restful import Api, Resource, reqparse

from authentication import Auth

app = Flask(__name__)
api = Api(app)
Auth.set_cursor('messente_proovikas', 'undo')


@app.route('/')
def hello_world():
    return 'Hello World!'


api.add_resource(Auth, "/auth")

if __name__ == '__main__':
    app.run()
