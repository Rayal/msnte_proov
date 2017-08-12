import psycopg2


class MyCursor:
    def __init__(self, dbname, username = "undo"):
        self.dbname = dbname
        self.username = username

    def send_query(self, query):
        connection = psycopg2.connect("dbname={} user={}".format(self.dbname, self.username))
        cursor = connection.cursor()

        cursor.execute(query)
        response = cursor.fetchall()

        connection.close()
        return response



