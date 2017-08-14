import logging
import time
from flask_restful import reqparse, Resource

import src.queries as queries
from src.app_logging import config_logger
from src.common import CommonVariables

logger = None


# Configures the logger used in this file with the correct settings to log to file.
def set_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger = config_logger(logger, CommonVariables.logfile)
    print(CommonVariables.logfile)


# The REST resource that handles authentication.
class Auth(Resource):
    # The parser parses through the json request to get the needed info.
    parser = reqparse.RequestParser()
    parser.add_argument('service',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")
    parser.add_argument('ip',
                        type=str,
                        required=True,
                        help="This field cannot be left blank")

    # Initialises the DB interface MyCursor
    @classmethod
    def set_cursor(cls, *args, **kwargs):
        cls.cursor = queries.MyCursor(*args, **kwargs)

    # The api allows for POST requests only.
    def post(self):
        # Connect to the database
        if not Auth.cursor.connect():
            logger.error("Unable to connect to database.")
            return {}, 503

        request_data = Auth.parser.parse_args()

        # Put together a query and send it.
        query = "SELECT * from {}" \
                " WHERE username = '{}'".format(
                    'api_users',
                    request_data['username'])
        response = next(iter(Auth.cursor.send_query(query)), None)

        # If there is no user with such a name...
        if not response:
            logger.info("Service: {}; Authentication failed: User does not exist.".format(
                request_data['service']
            ))
            return {}, 404

        response = dict(zip(CommonVariables.api_users_table, response))

        # If the user exists but the password doesn't match
        if response['password'] != request_data['password']:
            logger.info("Service: {}; User: {}; Authentication failed: Wrong password.".format(
                request_data['service'],
                response['account_id']
            ))
            return {}, 404

        # If the username and password are OK, but the IP address isn't whitelisted
        if request_data['ip'] not in response['whitelisted_ips']:
            logger.info("Service: {}; User: {}; Authentication failed: IP address not whitelisted.".format(
                request_data['service'],
                response['account_id']
            ))
            return {}, 403

        # And here it all checks out and the user is authenticated.
        logger.info("Service: {}; User: {}; Authentication successful".format(
            request_data['service'],
            response['account_id']
        ))

        return {
            'authenticated': True,
            "timestamp": int(time.time())
        }
