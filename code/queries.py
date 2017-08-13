import psycopg2


class MyCursor:
    def __init__(self, dbname):
        self.dbname = dbname

    def send_query(self, query):
        connection = psycopg2.connect("dbname={}".format(self.dbname))
        cursor = connection.cursor()

        cursor.execute(query)
        response = cursor.fetchall()

        connection.close()
        return response



