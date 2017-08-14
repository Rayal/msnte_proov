import logging
import psycopg2
import sys

from src.app_logging import config_logger
from src.common import CommonVariables

logger = None


# Configures the logger used in this file with the correct settings to log to file.
def set_logger():
    global logger
    logger = logging.getLogger(__name__)
    logger = config_logger(logger, CommonVariables.logfile)
    print(CommonVariables.logfile)


# Class that acts as an interface to the DB.
class MyCursor:
    def __init__(self, dbname, dbuser, dbpass, dbhost):
        self.dbname = dbname
        self.dbuser = dbuser
        self.dbpass = dbpass
        self.dbhost = dbhost
        self.connection = None
        self.cursor = None

    # Create a connection to the database
    def connect(self):
        try:
            self.connection = psycopg2.connect("dbname={} user={} password={} host={}".format(
                self.dbname,
                self.dbuser,
                self.dbpass,
                self.dbhost
            ))
        except:
            logger.error(str(sys.exc_info()[1]))
            return False
        return True

    # Send a given query to the database and return the results (if any)
    def send_query(self, query):
        cursor = self.connection.cursor()
        response = []
        try:
            cursor.execute(query)
            response = cursor.fetchall()
        except:
            logger.error(str(sys.exc_info()[1]))
            return False

        return response

    # Disconnect from the database.
    def disconnect(self):
        self.connection.close()
