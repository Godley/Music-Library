import sqlite3

class MusicData(object):
    def __init__(self, database):
        self.database = database
        self.createMusicTable()
        self.createInstrumentTable()
        self.createComposerTable()
        self.createKeyTable()

    def createKeyTable(self):
        '''
        method to create a new key table if one does not already exist
        :return: None
        '''
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS keys
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
            key[0]
            cursor.execute('SELECT * FROM KEYS WHERE name=?', (key[0],))
            result = cursor.fetchone()
            if result is None or len(result) == 0:
                cursor.execute('INSERT INTO keys VALUES(?,?,?)', key)

        cursor.execute('CREATE TABLE IF NOT EXISTS key_piece_join (key_id INTEGER, piece_id INTEGER, instrument_id INTEGER)')
        connection.commit()
        self.disconnect(connection)

    def createMusicTable(self):
        '''
        method to create piece table if one does not already exist
        :return: none
        '''
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pieces
             (filename text, title text, composer_id int)''')
        self.disconnect(connection)

    def createInstrumentTable(self):
        '''
        method to create instrument table if one does not already exist
        :return: none
        '''
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS instruments
                 (name text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS instruments_piece_join
             (instrument_id INTEGER, piece_id INTEGER)''')
        self.disconnect(connection)

    def createComposerTable(self):
        '''
        method to create composer table if one does not already exist
        :return:
        '''
        connection, cursor = self.connect()
        #cursor.execute('''CREATE TABLE composers
             #(name text,birth DATE,death DATE,country text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS composers
             (name text)''')
        self.disconnect(connection)


    def connect(self):
        '''
        method to create new sqlite connection and set up the cursor
        :return: connection object, cursor object
        '''
        conn = sqlite3.connect(self.database)
        return conn, conn.cursor()

    def addPiece(self, filename, data):
        '''
        method which takes in stuff about a piece and adds it to the relevant tables
        :param filename: filename the piece is talking about
        :param data: dictionary containing information - ids can be "composer", "title", "key" (which contains a dict of mode and fifths), "clef", "instruments"
        :return: None
        '''
        connection, cursor = self.connect()
        composer_id = -1
        title = ""
        if "title" in data:
            title = data["title"]

        if "composer" in data:
            query = 'SELECT ROWID FROM composers WHERE name=?'
            cursor.execute(query, (data["composer"],))
            if len(cursor.fetchall()) == 0:
                cursor.execute('INSERT INTO composers VALUES(?)', (data["composer"],))
                connection.commit()
                cursor.execute(query, (data["composer"],))
            composer_id = cursor.fetchone()
            if composer_id is not None:
                composer_id = composer_id[0]

        input = (filename,title,composer_id,)
        cursor.execute('INSERT INTO pieces VALUES(?,?,?)',input)
        connection.commit()
        select_input = (filename,)
        cursor.execute('SELECT ROWID FROM pieces WHERE filename=?', select_input)
        result = cursor.fetchall()[0][0]
        if "instruments" in data:
            instrument_ids = []
            for name in data["instruments"]:
                query = 'SELECT ROWID FROM instruments WHERE name=?'
                cursor.execute(query, (name,))
                inst_id = cursor.fetchall()
                if len(inst_id) == 0:
                    cursor.execute('INSERT INTO instruments VALUES(?)', (name,))
                    connection.commit()
                    cursor.execute(query, (name,))
                    inst_id = cursor.fetchall()
                if inst_id is not None and len(inst_id) > 0:
                    instrument_ids.append(inst_id[0][0])
            for index in instrument_ids:
                cursor.execute('INSERT INTO instruments_piece_join VALUES(?,?)', (index,result,))

        if "key" in data:
            for instrument in data["key"]:
                fifths = data["key"][instrument]["fifths"]
                mode = data["key"][instrument]["mode"]
                instrument_id = self.getInstrumentId(instrument, cursor)
                if instrument_id is None:
                    instrument_id = -1
                cursor.execute('SELECT ROWID FROM keys WHERE fifths=? AND mode=?', (fifths, mode,))
                key = cursor.fetchone()
                if key is not None and len(key) > 0:
                    cursor.execute('INSERT INTO key_piece_join VALUES(?,?,?)',(key[0],result,instrument_id,))

        connection.commit()
        self.disconnect(connection)

    def getPiece(self, filename):
        '''
        method to get a piece's table entry according to it's filename
        :param filename: string indicating the file name
        :return:
        '''
        connection, cursor = self.connect()
        thing = (filename,)
        cursor.execute('SELECT * FROM pieces WHERE filename=?',thing)
        result = cursor.fetchall()
        result = [r[0] for r in result]
        self.disconnect(connection)
        return result

    def getInstrumentId(self, instrument, cursor):
        '''
        method which takes in instrument name and returns the row id of that instrument
        :param instrument: name of instrument
        :param cursor: cursor object
        :return: int pertaining to row id of instrument in database
        '''
        cursor.execute('SELECT ROWID FROM instruments WHERE name=?', (instrument,))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    def getComposerId(self, composer, cursor):
        '''
        method which takes in composer name and outputs its database id
        :param composer: name of composer
        :param cursor: database cursor object
        :return: int pertaining to row id of composer in database
        '''
        cursor.execute('SELECT ROWID FROM composers WHERE name=?', (composer,))
        result = cursor.fetchall()
        return result[0][0]

    def getKeyId(self, key, cursor):
        '''
        method which takes in string of key name (e.g C major) and outputs row id
        :param key: string name of the key (e.g C major, A minor)
        :param cursor:  database cursor object
        :return: int pertaining to row id
        '''
        cursor.execute('SELECT ROWID FROM keys WHERE name=?', (key,))
        result = cursor.fetchall()
        return result[0][0]

    def getPiecesByInstruments(self, instruments):
        '''
        method to get all the pieces containing a certain instrument
        :param instrument: name of instrument
        :return: list of files containing that instrumnet
        '''
        connection, cursor = self.connect()
        instrument_ids = [self.getInstrumentId(instrument, cursor) for instrument in instruments]
        query = 'SELECT i.piece_id FROM instruments_piece_join i WHERE EXISTS (SELECT * FROM instruments_piece_join WHERE piece_id = i.piece_id AND instrument_id = ?)'
        for i in range(1,len(instrument_ids)):
            query += ' AND EXISTS (SELECT * FROM instruments_piece_join WHERE piece_id = i.piece_id AND instrument_id = ?)'
        query += ";"
        input = tuple(instrument_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor)
        self.disconnect(connection)
        return file_list

    def getPiecesByRowId(self, rows, cursor):
        '''
        method which takes in a list of rows which are ROWIDs in the piece table and returns a list of files
        :param rows: list of tuples pertaining to ROWIDs in pieces table
        :param cursor: connection cursor object
        :return: list of strings pertaining to xml files
        '''
        file_list = []
        previous = None
        for element in rows:
            if element != previous:
                cursor.execute('SELECT filename FROM pieces WHERE ROWID=?',element)
                file_list.append(cursor.fetchone()[0])
            previous = element
        return file_list

    def getPiecesByComposer(self, composer):
        '''
        method which takes in string of composer name and outputs list of files written by that guy
        :param composer: composer's name
        :return: list of strings (filenames)
        '''
        connection, cursor = self.connect()
        composer_id = self.getComposerId(composer, cursor)
        cursor.execute('SELECT filename FROM pieces WHERE composer_id=?', (composer_id,))
        result = cursor.fetchall()
        file_list = [r[0] for r in result]
        self.disconnect(connection)
        return file_list

    def getPieceByTitle(self, title):
        '''
        method which takes in title of piece and outputs list of files named that
        :param title: title of piece
        :return: list of tuples
        '''
        connection, cursor = self.connect()
        thing = (title,)
        cursor.execute('SELECT * FROM pieces WHERE title=?',thing)
        result = cursor.fetchall()
        result = [r[0] for r in result]
        self.disconnect(connection)
        return result

    def getPieceByKey(self, key):
        '''
        method which takes in a key and outputs list of files in that key
        :param key: string name of key (e.g C major)
        :return: list of strings (files)
        '''
        connection, cursor = self.connect()
        key_id = self.getKeyId(key, cursor)
        cursor.execute('SELECT piece_id FROM key_piece_join WHERE key_id=?', (key_id,))
        result = cursor.fetchall()
        file_list = self.getPiecesByRowId(result, cursor)
        self.disconnect(connection)
        return file_list

    def disconnect(self, connection):
        '''
        method which shuts down db connection
        :param connection: connection object
        :return: None
        '''
        connection.close()