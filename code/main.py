import logging
import time
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api, Resource, reqparse

from authentication import Auth
import config

logger = logging.getLogger(__name__)
#logging.basicConfig(filename="logged.log", level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)

app_config = config.get_config('config/config')

if 'dbname' in app_config:
    Auth.set_cursor(app_config['dbname'])
    logger.debug("{}:: Database name '{}' found in config file.".format(time.time(), app_config['dbname']))
else:
    logger.error("{}:: Database name not found in config file.".format(time.time()))
    exit(-1)


@app.route('/')
def hello_world():
    return {'message': 'Hello World!'}


if __name__ == '__main__':
    api.add_resource(Auth, "/auth")

    app.run()
