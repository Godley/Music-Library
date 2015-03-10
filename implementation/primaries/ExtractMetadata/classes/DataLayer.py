import sqlite3

class MusicData(object):
    def __init__(self, database):
        self.database = database
        self.createMusicTable()
        self.createInstrumentTable()
        self.createComposerTable()
        self.createKeyTable()

    def createKeyTable(self):
        connection, cursor = self.connect()
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='keys';''')
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('''CREATE TABLE keys
                 (name text, fifths int, mode text)''')
            keys = [("C major",0,"major",),
                    ("G major",1,"major",),
                    ("D major",2,"major",),
                    ("A major",3,"major",),
                    ("E major",4,"major",),
                    ("C# major",5,"major",),
                    ("F# major",6,"major",),
                    ("A minor",0,"minor",)]
            for key in keys:
                cursor.execute('INSERT INTO keys VALUES(?,?,?)', key)


        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='key_piece_join';''')
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('CREATE TABLE key_piece_join(key_id INTEGER, piece_id INTEGER)')
        connection.commit()
        self.disconnect(connection)

    def createMusicTable(self):
        connection, cursor = self.connect()
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='pieces';''')
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('''CREATE TABLE pieces
                 (filename text, title text)''')
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

    def createComposerTable(self):
        connection, cursor = self.connect()
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='composers';''')
        result = cursor.fetchall()
        if len(result) == 0:
            #cursor.execute('''CREATE TABLE composers
                 #(name text,birth DATE,death DATE,country text)''')
            cursor.execute('''CREATE TABLE composers
                 (name text)''')
        cursor.execute('''SELECT name FROM sqlite_master WHERE type='table' AND name='composer_piece_join';''')
        result = cursor.fetchall()
        if len(result) == 0:
            cursor.execute('''CREATE TABLE composer_piece_join
                 (composer_id INTEGER, piece_id INTEGER)''')
        self.disconnect(connection)


    def connect(self):
        conn = sqlite3.connect(self.database)
        return conn, conn.cursor()

    def addPiece(self, filename, data):
        connection, cursor = self.connect()
        title = ""
        if "title" in data:
            title = data["title"]
        input = (filename,title,)
        cursor.execute('INSERT INTO pieces VALUES(?,?)',input)
        connection.commit()
        select_input = (filename,)
        cursor.execute('SELECT ROWID FROM pieces WHERE filename=?', select_input)
        result = cursor.fetchall()[0][0]
        if "instruments" in data:
            instrument_ids = []
            for name in data["instruments"]:
                query = 'SELECT ROWID FROM instruments WHERE name=?'
                cursor.execute(query, (name,))
                if len(cursor.fetchall()) == 0:
                    cursor.execute('INSERT INTO instruments VALUES(?)', (name,))
                    connection.commit()
                    cursor.execute(query, (name,))
                inst_id = cursor.fetchall()
                instrument_ids.append(inst_id[0][0])
            for index in instrument_ids:
                cursor.execute('INSERT INTO instruments_piece_join VALUES(?,?)', (index,result,))

        if "composer" in data:
            query = 'SELECT ROWID FROM composers WHERE name=?'
            cursor.execute(query, (data["composer"],))
            if len(cursor.fetchall()) == 0:
                cursor.execute('INSERT INTO composers VALUES(?)', (data["composer"],))
                connection.commit()
                cursor.execute(query, (data["composer"],))
            composer_id = cursor.fetchall()[0][0]
            cursor.execute('INSERT INTO composer_piece_join VALUES(?,?)', (composer_id, result))

        if "key" in data:
            fifths = data["key"]["fifths"]
            mode = data["key"]["mode"]
            cursor.execute('SELECT ROWID FROM keys WHERE fifths=? AND mode=?', (fifths, mode,))
            key = cursor.fetchone()
            if len(key) > 0:
                cursor.execute('INSERT INTO key_piece_join VALUES(?,?)',(key[0],result,))

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

    def getComposerId(self, instrument, connection, cursor):
        cursor.execute('SELECT ROWID FROM composers WHERE name=?', (instrument,))
        result = cursor.fetchall()
        return result[0][0]

    def getKeyId(self, key, connection, cursor):
        cursor.execute('SELECT ROWID FROM keys WHERE name=?', (key,))
        result = cursor.fetchall()
        return result[0][0]

    def getPiecesByInstrument(self, instrument):
        connection, cursor = self.connect()
        instrument_id = self.getInstrumentId(instrument, connection, cursor)
        cursor.execute('SELECT piece_id FROM instruments_piece_join WHERE instrument_id=?', (instrument_id,))
        result = cursor.fetchall()
        file_list = self.getPiecesByRowId(result, cursor)
        self.disconnect(connection)
        return file_list

    def getPiecesByRowId(self, rows, cursor):
        file_list = []
        for element in rows:
            cursor.execute('SELECT filename FROM pieces WHERE ROWID=?',element)
            file_list.append(cursor.fetchone()[0])
        return file_list

    def getPiecesByComposer(self, composer):
        connection, cursor = self.connect()
        composer_id = self.getComposerId(composer, connection, cursor)
        cursor.execute('SELECT piece_id FROM composer_piece_join WHERE composer_id=?', (composer_id,))
        result = cursor.fetchall()
        file_list = self.getPiecesByRowId(result, cursor)
        self.disconnect(connection)
        return file_list

    def getPieceByTitle(self, title):
        connection, cursor = self.connect()
        thing = (title,)
        cursor.execute('SELECT * FROM pieces WHERE title=?',thing)
        result = cursor.fetchall()
        self.disconnect(connection)
        return result

    def getPieceByKey(self, key):
        connection, cursor = self.connect()
        key_id = self.getKeyId(key, connection, cursor)
        cursor.execute('SELECT piece_id FROM key_piece_join WHERE key_id=?', (key_id,))
        result = cursor.fetchall()
        file_list = self.getPiecesByRowId(result, cursor)
        self.disconnect(connection)
        return file_list

    def disconnect(self, connection):
        connection.close()