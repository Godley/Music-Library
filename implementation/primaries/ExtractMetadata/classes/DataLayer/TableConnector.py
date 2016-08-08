import sqlite3

class TableConnector(object):
    def __init__(self, database):
        self.database = database

    def connect(self):
        '''
        method to create new sqlite connection and set up the cursor
        :return: connection object, cursor object
        '''
        conn = sqlite3.connect(self.database)
        return conn, conn.cursor()

    def disconnect(self, connection):
        """
        method which shuts down db connection
        :param connection: connection object
        :return: None
        """
        connection.close()