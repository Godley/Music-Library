import sqlite3

from implementation.primaries.ExtractMetadata.classes.DataLayer import TableConnector

class TableCreator(TableConnector.TableConnector):
    tables = ["sources (piece_id int, source text)",
              "licenses (piece_id int, license text)",
              "secrets (piece_id int, secret text)",
              "tempos (beat text, minute int, beat_2 text)",
              "tempo_piece_join(piece_id int, tempo_id int)",
              "timesigs (beat int, b_type int)",
              "time_piece_join(piece_id int, time_id int)",
              "keys(name text, fifths int, mode text)",
              "key_piece_join (key_id INTEGER, piece_id INTEGER, instrument_id INTEGER)",
              "playlists (name text)",
              "playlist_join(playlist_id int, piece_id int)",
              "clefs(name text, sign text, line int)",
              "clef_piece_join (clef_id INTEGER, piece_id INTEGER, instrument_id INTEGER)",
              "instruments(name text,diatonic int,chromatic int)",
              "instruments_piece_join(instrument_id INTEGER, piece_id INTEGER)",
              "lyricists(name text)",
              "composers(name text)",
              "pieces(filename text, title text, composer_id int, lyricist_id int, archived BOOLEAN)"]
    def __init__(self, db):
        super(TableCreator, self).__init__(db)
        for table in self.tables:
            self.create_if_not_exists(table)
        self.createKeyData()
        self.createClefsData()


    def create_if_not_exists(self, table_and_columns):
        connection, cursor = self.connect()
        query = 'CREATE TABLE IF NOT EXISTS '+table_and_columns
        cursor.execute(query)
        connection.commit()
        self.disconnect(connection)

    def get_value_for_filename(self, filename, value):
        """
        Method for doing a simple search where the table contains x value linked
        to x piece id. Used for license, source, or secret
        :param filename:
        :param value:
        :return:
        """
        connection, cursor = self.connect()
        query = 'SELECT {} FROM {}s {}, pieces p WHERE p.filename=? AND {}.piece_id = p.ROWID'.format(value, value, value[0],
                                                                                                      value[0])
        cursor.execute(query, (filename,))
        result = cursor.fetchone()
        self.disconnect(connection)
        return result

    def createKeyData(self):
        '''
        method to create a new key table if one does not already exist
        :return: None
        '''
        connection, cursor = self.connect()
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
        connection.commit()
        self.disconnect(connection)

    def createClefsData(self):
        '''
        method to create a new key table if one does not already exist
        :return: None
        '''
        connection, cursor = self.connect()
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

        connection.commit()
        self.disconnect(connection)