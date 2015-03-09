import sqlite3

class MusicData(object):
    def __init__(self, database):
        self.database = database
        self.createMusicTable()
        self.createInstrumentTable()

    def createMusicTable(self):
        connection, cursor = self.connect()
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='pieces';''')
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('''CREATE TABLE pieces
                 (filename text)''')
        self.disconnect(connection)

    def createInstrumentTable(self):
        connection, cursor = self.connect()
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='instruments';''')
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('''CREATE TABLE instruments
                 (name text)''')
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='instruments_piece_join';''')
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('''CREATE TABLE instruments_piece_join
                 (instrument_id INTEGER, piece_id INTEGER)''')
        self.disconnect(connection)


    def connect(self):
        conn = sqlite3.connect(self.database)
        return conn, conn.cursor()

    def addPiece(self, filename, data):
        connection, cursor = self.connect()
        thing = (filename,)
        cursor.execute('INSERT INTO pieces VALUES(?)',thing)
        connection.commit()
        cursor.execute('SELECT ROWID FROM pieces WHERE filename=?', thing)
        result = cursor.fetchall()[0][0]
        if "instruments" in data:
            instrument_ids = []
            for name in data["instruments"]:
                cursor.execute('SELECT ROWID FROM instruments WHERE name=?', (name,))
                if len(cursor.fetchall()) == 0:
                    cursor.execute('INSERT INTO instruments VALUES(?)', (name,))
                    connection.commit()
                    cursor.execute('SELECT ROWID FROM instruments WHERE name=?', (name,))
                inst_id = cursor.fetchall()
                instrument_ids.append(inst_id[0][0])
            for index in instrument_ids:
                cursor.execute('INSERT INTO instruments_piece_join VALUES(?,?)', (index,result,))
        connection.commit()
        self.disconnect(connection)

    def getPiece(self, filename):
        connection, cursor = self.connect()
        thing = (filename,)
        cursor.execute('SELECT * FROM pieces WHERE filename=?',thing)
        result = cursor.fetchall()
        self.disconnect(connection)
        return result

    def getInstrumentId(self, instrument, connection, cursor):
        cursor.execute('SELECT ROWID FROM instruments WHERE name=?', (instrument,))
        result = cursor.fetchall()
        return result[0][0]

    def getPiecesByInstrument(self, instrument):
        connection, cursor = self.connect()
        instrument_id = self.getInstrumentId(instrument, connection, cursor)
        cursor.execute('SELECT piece_id FROM instruments_piece_join WHERE instrument_id=?', (instrument_id,))
        result = cursor.fetchall()
        file_list = []
        for element in result:
            cursor.execute('SELECT filename FROM pieces WHERE ROWID=?', element)
            file_list.append(cursor.fetchone())
        self.disconnect(connection)
        return file_list

    def disconnect(self, connection):
        connection.close()