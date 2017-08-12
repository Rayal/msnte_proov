import time
from flask import Flask
from flask_restful import Api, Resource, reqparse

import queries

app = Flask(__name__)
api = Api(app)

cursor = queries.MyCursor('messente_proovikas', 'undo')

@app.route('/')
def hello_world():
    return 'Hello World!'


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

        response = cursor.send_query(query)
        if response:
            return {
                'authenticated': True,
                "timestamp": int(time.time())
            }
        else:
            return {'response': 'Not found'}, 404

api.add_resource(Auth, "/auth")

if __name__ == '__main__':
    app.run()
