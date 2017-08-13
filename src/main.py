import logging
import time
from logging.handlers import RotatingFileHandler

from flask import Flask
from flask_restful import Api, Resource, reqparse

from src.authentication import Auth
import src.config as config

logger = logging.getLogger(__name__)
#logging.basicConfig(filename="logged.log", level=logging.DEBUG)
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
api = Api(app)

app_config = config.get_config('/etc/messente/config/config')

try:
    Auth.set_cursor(
        app_config['dbname'],
        app_config['dbuser'],
        app_config['dbpass'],
        app_config['dbhost']
    )
    logger.debug("{}:: Database credentials found in config file.".format(time.time()))
except KeyError:
    logger.error("{}:: Database credentials not found in config file.".format(time.time()))
    exit(-1)


@app.route('/')
def hello_world():
    return {'message': 'Hello World!'}


if __name__ == '__main__':
    api.add_resource(Auth, "/auth")

    app.run()
