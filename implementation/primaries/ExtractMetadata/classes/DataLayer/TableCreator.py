import sqlite3

from implementation.primaries.ExtractMetadata.classes.DataLayer import TableConnector

class TableCreator(TableConnector.TableConnector):
    def createSourcesTable(self):
        connection, cursor = self.connect()
        query = 'CREATE TABLE IF NOT EXISTS sources (piece_id int, source text)'
        cursor.execute(query)
        connection.commit()
        self.disconnect(connection)

    def createLicenseTable(self):
        connection, cursor = self.connect()
        query = 'CREATE TABLE IF NOT EXISTS licenses (piece_id int, license text)'
        cursor.execute(query)
        connection.commit()
        self.disconnect(connection)

    def createSecretsTable(self):
        connection, cursor = self.connect()
        query = 'CREATE TABLE IF NOT EXISTS secrets (piece_id int, secret text)'
        cursor.execute(query)
        connection.commit()
        self.disconnect(connection)

    def getSecret(self, filename):
        # TODO HASH THIS STUFF
        connection, cursor = self.connect()
        query = 'SELECT secret FROM secrets s, pieces p WHERE p.filename=? AND s.piece_id = p.ROWID'
        cursor.execute(query, (filename,))
        result = cursor.fetchone()
        self.disconnect(connection)
        return result

    def createTempoTable(self):
        '''
        method to create a new key table if one does not already exist
        :return: None
        '''
        connection, cursor = self.connect()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS tempos (beat text, minute int, beat_2 text)')
        cursor.execute('''CREATE TABLE IF NOT EXISTS tempo_piece_join
             (piece_id int, tempo_id int)''')
        connection.commit()
        self.disconnect(connection)

    def createTimeTable(self):
        '''
        method to create a new key table if one does not already exist
        :return: None
        '''
        connection, cursor = self.connect()
        cursor.execute(
            'CREATE TABLE IF NOT EXISTS timesigs (beat int, b_type int)')
        cursor.execute('''CREATE TABLE IF NOT EXISTS time_piece_join
             (piece_id int, time_id int)''')
        connection.commit()
        self.disconnect(connection)

    def createKeyTable(self):
        '''
        method to create a new key table if one does not already exist
        :return: None
        '''
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS keys
             (name text, fifths int, mode text)''')
        keys = [("C flat major", -7, "major"),
                ("G flat major", -6, "major"),
                ("D flat major", -5, "major"),
                ("A flat major", -4, "major"),
                ("E flat major", -3, "major"),
                ("B flat major", -2, "major"),
                ("F major", -1, "major"),
                ("C major", 0, "major",),
                ("G major", 1, "major",),
                ("D major", 2, "major",),
                ("A major", 3, "major",),
                ("E major", 4, "major",),
                ("B major", 5, "major"),
                ("F# major", 6, "major",),
                ("C# major", 7, "major",),
                ("A flat minor", -7, "minor"),
                ("E flat minor", -6, "minor"),
                ("B flat minor", -5, "minor"),
                ("F minor", -4, "minor"),
                ("C minor", -3, "minor"),
                ("G minor", -2, "minor"),
                ("D minor", -1, "minor"),
                ("A minor", 0, "minor",),
                ("E minor", 1, "minor"),
                ("B minor", 2, "minor"),
                ("F# minor", 3, "minor"),
                ("C# minor", 4, "minor"),
                ("G# minor", 5, "minor"),
                ("D# minor", 6, "minor"),
                ("A# minor", 7, "minor")]
        for key in keys:
            cursor.execute('SELECT * FROM KEYS WHERE name=?', (key[0],))
            result = cursor.fetchone()
            if result is None or len(result) == 0:
                cursor.execute('INSERT INTO keys VALUES(?,?,?)', key)

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS key_piece_join (key_id INTEGER, piece_id INTEGER, instrument_id INTEGER)')
        connection.commit()
        self.disconnect(connection)

    def createPlaylistTable(self):
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS playlists(name text)''')
        cursor.execute(
            '''CREATE TABLE IF NOT EXISTS playlist_join(playlist_id int, piece_id int)''')
        connection.commit()
        self.disconnect(connection)

    def createClefsTable(self):
        '''
        method to create a new key table if one does not already exist
        :return: None
        '''
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS clefs
             (name text, sign text, line int)''')
        clefs = [("treble", "G", 2,),
                 ("french", "G", 1),
                 ("varbaritone", "F", 3,),
                 ("subbass", "F", 5),
                 ("bass", "F", 4),
                 ("alto", "C", 3),
                 ("percussion", "percussion", -1,),
                 ("tenor", "C", 4),
                 ("baritone", "C", 5,),
                 ("mezzosoprano", "C", 2),
                 ("soprano", "C", 1),
                 ("varC", "VARC", -1),
                 ("alto varC", "VARC", 3),
                 ("tenor varC", "VARC", 4),
                 ("baritone varC", "VARC", 5)]
        for clef in clefs:
            cursor.execute('SELECT * FROM clefs WHERE name=?', (clef[0],))
            result = cursor.fetchone()
            if result is None or len(result) == 0:
                cursor.execute('INSERT INTO clefs VALUES(?,?,?)', clef)

        cursor.execute(
            'CREATE TABLE IF NOT EXISTS clef_piece_join (clef_id INTEGER, piece_id INTEGER, instrument_id INTEGER)')
        connection.commit()
        self.disconnect(connection)

    def createMusicTable(self):
        '''
        method to create piece table if one does not already exist
        :return: none
        '''
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pieces
             (filename text, title text, composer_id int, lyricist_id int, archived BOOLEAN)''')
        self.disconnect(connection)

    def createInstrumentTable(self):
        '''
        method to create instrument table if one does not already exist
        :return: none
        '''
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS instruments
                 (name text,diatonic int,chromatic int)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS instruments_piece_join
             (instrument_id INTEGER, piece_id INTEGER)''')
        self.disconnect(connection)

    def createComposerTable(self):
        '''
        method to create composer table if one does not already exist
        :return:
        '''
        connection, cursor = self.connect()
        # cursor.execute('''CREATE TABLE composers
        #(name text,birth DATE,death DATE,country text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS composers
             (name text)''')
        self.disconnect(connection)

    def createLyricistTable(self):
        '''
        method to create composer table if one does not already exist
        :return:
        '''
        connection, cursor = self.connect()
        # cursor.execute('''CREATE TABLE composers
        #(name text,birth DATE,death DATE,country text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS lyricists
             (name text)''')
        self.disconnect(connection)