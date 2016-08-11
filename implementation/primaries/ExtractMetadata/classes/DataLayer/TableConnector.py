import sqlite3
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return hashdict(d)

class TableConnector(object):
    def __init__(self, database):
        self.database = database

    def connect(self):
        '''
        method to create new sqlite connection and set up the cursor
        :return: connection object, cursor object
        '''
        conn = sqlite3.connect(self.database)
        conn.row_factory = dict_factory
        return conn, conn.cursor()

    def disconnect(self, connection):
        """
        method which shuts down db connection
        :param connection: connection object
        :return: None
        """
        connection.close()