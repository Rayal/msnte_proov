import logging
import psycopg2
import sys

logger = logging.getLogger(__name__)

class MyCursor:
    def __init__(self, dbname, dbuser, dbpass, dbhost):
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbhost = dbhost
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = psycopg2.connect("dbname={} user={} password={} host={}".format(
                self.dbname,
                self.dbuser,
                self.dbpass,
                self.dbhost
            ))
        except:
            logger.error("{}:: " + str(sys.exc_info()[1]))
            return False
        return True

    def send_query(self, query):
        cursor = self.connection.cursor()
        response = []
        try:
            cursor.execute(query)
            response = cursor.fetchall()
        except:
            logger.error("{}:: " + str(sys.exc_info()[1]))
            return False

        return response

    def disconnect(self):
        self.connection.close()



