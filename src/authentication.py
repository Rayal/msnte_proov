import logging
import time
from flask_restful import reqparse, Resource

import src.queries as queries
from src.app_logging import config_logger
from src.common import CommonVariables

logger = None


def set_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger = config_logger(logger, CommonVariables.logfile)
    print(CommonVariables.logfile)


class Auth(Resource):
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

    @classmethod
    def set_cursor(cls, *args, **kwargs):
        cls.cursor = queries.MyCursor(*args, **kwargs)

    def post(self):
        if not Auth.cursor.connect():
            logger.error("Unable to connect to database.")
            return {}, 503

        request_data = Auth.parser.parse_args()

        query = "SELECT * from {}" \
                " WHERE username = '{}'".format(
                    'api_users',
                    request_data['username'])
        response = next(iter(Auth.cursor.send_query(query)), None)

        if not response:
            logger.info("Service: {}; Authentication failed: User does not exist.".format(
                request_data['service']
            ))
            return {}, 404

        response = dict(zip(CommonVariables.api_users_table, response))

        if response['password'] != request_data['password']:
            logger.info("Service: {}; User: {}; Authentication failed: Wrong password.".format(
                request_data['service'],
                response['account_id']
            ))
            return {}, 404

        if request_data['ip'] not in response['whitelisted_ips']:
            logger.info("Service: {}; User: {}; Authentication failed: IP address not whitelisted.".format(
                request_data['service'],
                response['account_id']
            ))
            return {}, 403

        logger.info("Service: {}; User: {}; Authentication successful".format(
            request_data['service'],
            response['account_id']
        ))

        return {
            'authenticated': True,
            "timestamp": int(time.time())
        }
