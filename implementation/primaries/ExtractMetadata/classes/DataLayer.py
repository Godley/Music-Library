import sqlite3

class MusicData(object):
    def __init__(self, database):
        self.database = database
        self.createMusicTable()

    def createMusicTable(self):
        connection = self.connect()
        c = connection.cursor()
        c.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='pieces';''')
        result = c.fetchall()
        if len(result) == 0:
            c.execute('''CREATE TABLE pieces
                 (filename text)''')
        self.disconnect(connection)

    def connect(self):
        conn = sqlite3.connect(self.database)
        return conn

    def addPiece(self, filename, data):
        connection = self.connect()
        cursor = connection.cursor()
        thing = (filename,)
        cursor.execute('INSERT INTO pieces VALUES(?)',thing)
        self.disconnect(connection)

    def disconnect(self, connection):
        connection.close()