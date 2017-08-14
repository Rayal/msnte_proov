import logging
import time
from flask import Flask
from flask_restful import Api

from src import queries
from src import authentication
from src.app_logging import config_logger, get_handler
from src.authentication import Auth
from src.common import CommonVariables
import src.config as config


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


app = Flask(__name__)
api = Api(app)


# Getting app config from file
app_config = config.get_config('/etc/messente/config/config')


# Setting up logger so that it logs to the correct file
if 'logfile' in app_config:
    CommonVariables.logfile = app_config['logfile']
else:
    logger.warning("{}:: Log file address not found in config file. Resorting to default: {}".format(
        time.time(),
        CommonVariables.logfile
    ))

logger = config_logger(logger, CommonVariables.logfile)
app.logger.addHandler(get_handler(CommonVariables.logfile))
authentication.set_logger()
queries.set_logger()


# Setting up our database interface with the credentials from the config file.
try:
    Auth.set_cursor(
        app_config['dbname'],
        app_config['dbuser'],
        app_config['dbpass'],
        app_config['dbhost']
    )
    logger.debug("Database credentials found in config file.")
except KeyError:
    logger.error("Database credentials not found in config file.")
    exit(-1)


@app.route('/')
def hello_world():
    return {'message': 'Hello World!'}


if __name__ == '__main__':
    app.logger.setLevel(logging.DEBUG)
    api.add_resource(Auth, "/auth") # http://localhost:5000/auth

    app.run()
