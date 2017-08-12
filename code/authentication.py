import time
from flask_restful import reqparse, Resource

import queries


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
    def set_cursor(cls, dbname, username):
        cls.cursor = queries.MyCursor(dbname, username)

    def post(self):
        request_data = Auth.parser.parse_args()
        query = "SELECT * FROM {} " \
                "WHERE username = '{}' AND " \
                "password = '{}' AND " \
                "'{}' = ANY (whitelisted_ips)".format(
                    'api_users',
                    request_data['username'],
                    request_data['password'],
                    request_data['ip'])

        response = Auth.cursor.send_query(query)
        if response:
            return {
                'authenticated': True,
                "timestamp": int(time.time())
            }
        else:
            return {'response': 'Failed to Authenticate.'}, 401
