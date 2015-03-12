import sqlite3

class MusicData(object):
    def __init__(self, database):
        self.database = database
        self.createMusicTable()
        self.createInstrumentTable()
        self.createComposerTable()
        self.createLyricistTable()
        self.createKeyTable()
        self.createClefsTable()
        self.createTimeTable()
        self.createTempoTable()

    def createTempoTable(self):
        '''
        method to create a new key table if one does not already exist
        :return: None
        '''
        connection, cursor = self.connect()
        cursor.execute('CREATE TABLE IF NOT EXISTS tempos (beat text, minute int, beat_2 text)')
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
        cursor.execute('CREATE TABLE IF NOT EXISTS timesigs (beat int, b_type int)')
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
        keys = [("C flat major",-7, "major"),
                ("G flat major",-6, "major"),
                ("D flat major",-5, "major"),
                ("A flat major",-4, "major"),
                ("E flat major",-3, "major"),
                ("B flat major",-2, "major"),
                ("F major",-1,"major"),
                ("C major",0,"major",),
                ("G major",1,"major",),
                ("D major",2,"major",),
                ("A major",3,"major",),
                ("E major",4,"major",),
                ("B major",5,"major"),
                ("F# major",6,"major",),
                ("C# major",7,"major",),
                ("A flat minor",-7,"minor"),
                ("E flat minor",-6,"minor"),
                ("B flat minor",-5,"minor"),
                ("F minor",-4,"minor"),
                ("C minor",-3,"minor"),
                ("G minor",-2,"minor"),
                ("D minor",-1,"minor"),
                ("A minor",0,"minor",),
                ("E minor",1,"minor"),
                ("B minor",2,"minor"),
            ("F# minor",3,"minor"),
            ("C# minor",4,"minor"),
            ("G# minor",5,"minor"),
            ("D# minor",6,"minor"),
            ("A# minor",7,"minor")]
        for key in keys:
            cursor.execute('SELECT * FROM KEYS WHERE name=?', (key[0],))
            result = cursor.fetchone()
            if result is None or len(result) == 0:
                cursor.execute('INSERT INTO keys VALUES(?,?,?)', key)

        cursor.execute('CREATE TABLE IF NOT EXISTS key_piece_join (key_id INTEGER, piece_id INTEGER, instrument_id INTEGER)')
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
        clefs = [("treble","G",2,),
                 ("french","G",1),
                 ("varbaritone","F",3,),
                 ("subbass","F",5),
                ("bass","F",4),
                ("alto","C",3),
                 ("percussion","percussion",-1,),
                 ("tenor","C",4),
                 ("baritone","C",5,),
                 ("mezzosoprano","C",2),
                ("soprano","C",1),
                ("varC","VARC",-1),
                ("alto varC","VARC",3),
                ("tenor varC","VARC",4),
                 ("baritone varC","VARC",5)]
        for clef in clefs:
            cursor.execute('SELECT * FROM clefs WHERE name=?', (clef[0],))
            result = cursor.fetchone()
            if result is None or len(result) == 0:
                cursor.execute('INSERT INTO clefs VALUES(?,?,?)', clef)

        cursor.execute('CREATE TABLE IF NOT EXISTS clef_piece_join (clef_id INTEGER, piece_id INTEGER, instrument_id INTEGER)')
        connection.commit()
        self.disconnect(connection)

    def createMusicTable(self):
        '''
        method to create piece table if one does not already exist
        :return: none
        '''
        connection, cursor = self.connect()
        cursor.execute('''CREATE TABLE IF NOT EXISTS pieces
             (filename text, title text, composer_id int, lyricist_id int)''')
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
        #cursor.execute('''CREATE TABLE composers
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
        #cursor.execute('''CREATE TABLE composers
             #(name text,birth DATE,death DATE,country text)''')
        cursor.execute('''CREATE TABLE IF NOT EXISTS lyricists
             (name text)''')
        self.disconnect(connection)

    def addInstruments(self, data):
        connection, cursor = self.connect()
        elements = []
        for item in data:
            octave = 0
            diatonic = 0
            chromatic = 0
            if "transposition" in item:
                trans = item["transposition"]
                if "diatonic" in trans:
                    diatonic = trans["diatonic"]
                if "chromatic" in trans:
                    chromatic = trans["chromatic"]
            item_data = (item["name"],diatonic,chromatic)
            elements.append(item_data)
        cursor.executemany('INSERT INTO instruments VALUES(?,?,?)', elements)
        connection.commit()
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
        :param data: dictionary containing information - ids can be "composer", "title", "key" (which contains a dict of mode and fifths attached to instruments), "clef"
        (same as keys), "tempo", "instruments"
        :return: None
        '''
        connection, cursor = self.connect()
        composer_id = -1
        lyricist_id = -1
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

        if "lyricist" in data:
            query = 'SELECT ROWID FROM lyricists WHERE name=?'
            cursor.execute(query, (data["lyricist"],))
            if len(cursor.fetchall()) == 0:
                cursor.execute('INSERT INTO lyricists VALUES(?)', (data["lyricist"],))
                connection.commit()
                cursor.execute(query, (data["lyricist"],))
            lyricist_id = cursor.fetchone()
            if lyricist_id is not None:
                lyricist_id = lyricist_id[0]

        input = (filename,title,composer_id,lyricist_id,)
        cursor.execute('INSERT INTO pieces VALUES(?,?,?,?)',input)
        connection.commit()
        select_input = (filename,)
        cursor.execute('SELECT ROWID FROM pieces WHERE filename=?', select_input)
        result = cursor.fetchall()[0][0]
        if "instruments" in data:
            instrument_ids = []
            for item in data["instruments"]:
                octave = 0
                diatonic = 0
                chromatic = 0
                if "transposition" in item:
                    transposition = item["transposition"]
                    if "diatonic" in transposition:
                        diatonic = transposition["diatonic"]
                    if "chromatic" in transposition:
                        chromatic = transposition["chromatic"]
                query = 'SELECT ROWID FROM instruments WHERE name=? AND diatonic=? AND chromatic=?'
                cursor.execute(query, (item["name"],diatonic,chromatic,))
                inst_id = cursor.fetchall()
                if len(inst_id) == 0:
                    cursor.execute('INSERT INTO instruments VALUES(?,?,?)', (item["name"],diatonic,chromatic,))
                    connection.commit()
                    cursor.execute(query, (item["name"],diatonic,chromatic,))
                    inst_id = cursor.fetchall()
                if inst_id is not None and len(inst_id) > 0:
                    instrument_ids.append(inst_id[0][0])
            for index in instrument_ids:
                cursor.execute('INSERT INTO instruments_piece_join VALUES(?,?)', (index,result,))

        if "key" in data:
            for instrument in data["key"]:
                for key in data["key"][instrument]:
                    fifths = key["fifths"]
                    mode = key["mode"]
                    instrument_id = self.getInstrumentId(instrument, cursor)
                    if instrument_id is None:
                        instrument_id = -1
                    cursor.execute('SELECT ROWID FROM keys WHERE fifths=? AND mode=?', (fifths, mode,))
                    key = cursor.fetchone()
                    if key is not None and len(key) > 0:
                        cursor.execute('INSERT INTO key_piece_join VALUES(?,?,?)',(key[0],result,instrument_id,))

        if "clef" in data:
            for instrument in data["clef"]:
                for clef in data["clef"][instrument]:
                    sign = clef["sign"]
                    line = clef["line"]
                    instrument_id = self.getInstrumentId(instrument, cursor)
                    if instrument_id is None:
                        instrument_id = -1
                    cursor.execute('SELECT ROWID FROM clefs WHERE sign=? AND line=?', (sign, line,))
                    clef_id = cursor.fetchone()
                    if clef_id is not None and len(clef_id) > 0:
                        cursor.execute('INSERT INTO clef_piece_join VALUES(?,?,?)',(clef_id[0],result,instrument_id,))

        if "time" in data:
            for meter in data["time"]:
                beat = meter["beat"]
                b_type = meter["type"]
                cursor.execute('SELECT ROWID FROM timesigs WHERE beat=? AND b_type=?',(beat,b_type))
                res = cursor.fetchone()
                if res is None or len(res) == 0:
                    cursor.execute('INSERT INTO timesigs VALUES(?,?)',(beat,b_type))
                    connection.commit()
                    cursor.execute('SELECT ROWID FROM timesigs WHERE beat=? AND b_type=?',(beat,b_type))
                    res = cursor.fetchone()
                cursor.execute('INSERT INTO time_piece_join VALUES(?,?)',(result,res[0]))

        if "tempo" in data:
            for tempo in data["tempo"]:
                beat = tempo["beat"]
                beat_2 = -1
                minute = -1
                if "beat_2" in tempo:
                    beat_2 = tempo["beat_2"]
                if "minute" in tempo:
                    minute = tempo["minute"]
                cursor.execute('SELECT ROWID FROM tempos WHERE beat=? AND beat_2=? AND minute=?',(beat,beat_2,minute))
                res = cursor.fetchone()
                if res is None or len(res) == 0:
                    cursor.execute('INSERT INTO tempos VALUES(?,?,?)',(beat,minute,beat_2))
                    connection.commit()
                    cursor.execute('SELECT ROWID FROM tempos WHERE beat=? AND beat_2=? AND minute=?',(beat,beat_2,minute))
                    res = cursor.fetchone()
                cursor.execute('INSERT INTO tempo_piece_join VALUES(?,?)',(result,res[0]))


        connection.commit()
        self.disconnect(connection)

    def getFileList(self):
        connection, cursor = self.connect()
        query = 'SELECT filename FROM pieces'
        cursor.execute(query, ())
        results = cursor.fetchall()
        self.disconnect(connection)
        filelist = [result[0] for result in results]
        return filelist

    def getPiece(self, filename):
        '''
        method to get a piece's table entry according to it's filename
        :param filename: string indicating the file name
        :return:
        '''
        connection, cursor = self.connect()
        thing = (filename,)
        cursor.execute('SELECT ROWID, filename, title, composer_id FROM pieces WHERE filename=?',thing)
        result = cursor.fetchall()
        self.disconnect(connection)
        return result

    def getTimeId(self, beats, type, cursor):
        '''
        method which takes in instrument name and returns the row id of that instrument
        :param instrument: name of instrument
        :param cursor: cursor object
        :return: int pertaining to row id of instrument in database
        '''
        cursor.execute('SELECT ROWID FROM timesigs WHERE beat=? AND b_type=? ', (beats, type))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    def getTempoId(self, beat, minute, beat_2, cursor):
        '''
        method which takes in instrument name and returns the row id of that instrument
        :param instrument: name of instrument
        :param cursor: cursor object
        :return: int pertaining to row id of instrument in database
        '''
        cursor.execute('SELECT ROWID FROM tempos WHERE beat=? AND minute=? AND beat_2=? ', (beat, minute, beat_2))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

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
        if len(result) > 0:
            return result[0][0]

    def getLyricistId(self, lyricist, cursor):
        '''
        method which takes in composer name and outputs its database id
        :param composer: name of composer
        :param cursor: database cursor object
        :return: int pertaining to row id of composer in database
        '''
        cursor.execute('SELECT ROWID FROM lyricists WHERE name=?', (lyricist,))
        result = cursor.fetchall()
        if len(result) > 0:
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
        if len(result) > 0:
            return result[0][0]

    def getClefId(self, clef, cursor):
        '''
        method which takes in string of clef name (e.g treble) and outputs row id
        :param key: string name of the clef (e.g treble, bass)
        :param cursor:  database cursor object
        :return: int pertaining to row id
        '''
        cursor.execute('SELECT ROWID FROM clefs WHERE name=?', (clef,))
        result = cursor.fetchall()
        if len(result) > 0:
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

    def getPiecesByLyricist(self, lyricist):
        '''
        method which takes in string of lyricist name and outputs list of files written by that guy/woman
        :param composer: lyricist's name
        :return: list of strings (filenames)
        '''
        connection, cursor = self.connect()
        lyricist_id = self.getLyricistId(lyricist, cursor)
        cursor.execute('SELECT filename FROM pieces WHERE lyricist_id=?', (lyricist_id,))
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

    def getPieceByKeys(self, keys):
        '''
        method which takes in a key and outputs list of files in that key
        :param key: string name of key (e.g C major)
        :return: list of strings (files)
        '''
        connection, cursor = self.connect()
        key_ids = [self.getKeyId(key, cursor) for key in keys]
        query = 'SELECT i.piece_id FROM key_piece_join i WHERE EXISTS (SELECT * FROM key_piece_join WHERE piece_id = i.piece_id AND key_id = ?)'
        for i in range(1,len(key_ids)):
            query += ' AND EXISTS (SELECT * FROM key_piece_join WHERE piece_id = i.piece_id AND key_id = ?)'
        query += ";"
        input = tuple(key_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor)
        self.disconnect(connection)
        return file_list

    def getPieceByClefs(self, clefs):
        '''
        method which takes in a key and outputs list of files in that key
        :param key: string name of key (e.g C major)
        :return: list of strings (files)
        '''
        connection, cursor = self.connect()
        clef_ids = [self.getClefId(clef, cursor) for clef in clefs]
        query = 'SELECT i.piece_id FROM clef_piece_join i WHERE EXISTS (SELECT * FROM clef_piece_join WHERE piece_id = i.piece_id AND clef_id = ?)'
        for i in range(1,len(clef_ids)):
            query += ' AND EXISTS (SELECT * FROM clef_piece_join WHERE piece_id = i.piece_id AND clef_id = ?)'
        query += ";"
        input = tuple(clef_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor)
        self.disconnect(connection)
        return file_list

    def getPieceByInstrumentInKey(self, data):
        connection, cursor = self.connect()
        search_ids = []
        tuple_data = [instrument for instrument in data]
        for instrument in data:
            search_ids.append(self.getInstrumentId(instrument, cursor))
            search_ids.append(self.getKeyId(data[instrument], cursor))
        query = 'SELECT key.piece_id FROM key_piece_join key WHERE EXISTS (SELECT * FROM key_piece_join WHERE piece_id = key.piece_id AND instrument_id = ? AND key_id = ?)'
        for i in range(1,len(tuple_data)):
            query += ' AND EXISTS (SELECT * FROM key_piece_join WHERE piece_id = key.piece_id AND instrument_id = ? AND key_id = ?)'
        query += ";"
        cursor.execute(query, tuple(search_ids))
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor)
        return file_list

    def getPieceByInstrumentInClef(self, data):
        connection, cursor = self.connect()
        search_ids = []
        tuple_data = [instrument for instrument in data]
        for instrument in data:
            search_ids.append(self.getInstrumentId(instrument, cursor))
            search_ids.append(self.getClefId(data[instrument], cursor))
        query = 'SELECT key.piece_id FROM clef_piece_join key WHERE EXISTS (SELECT * FROM clef_piece_join WHERE piece_id = key.piece_id AND instrument_id = ? AND clef_id = ?)'
        for i in range(1,len(tuple_data)):
            query += ' AND EXISTS (SELECT * FROM clef_piece_join WHERE piece_id = key.piece_id AND instrument_id = ? AND clef_id = ?)'
        query += ";"
        cursor.execute(query, tuple(search_ids))
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor)
        return file_list

    def getPieceByMeter(self, meters):
        meter_list = []
        for meter in meters:
            if "/" in meter:
                values = meter.split("/")
                beat = int(values[0])
                b_type = int(values[1])
                meter_list.append((beat,b_type))
        connection, cursor = self.connect()
        time_ids = [self.getTimeId(meter[0],meter[1], cursor) for meter in meter_list]
        query = 'SELECT i.piece_id FROM time_piece_join i WHERE EXISTS (SELECT * FROM time_piece_join WHERE piece_id = i.piece_id AND time_id = ?)'
        for i in range(1,len(time_ids)):
            query += ' AND EXISTS (SELECT * FROM time_piece_join WHERE piece_id = i.piece_id AND time_id = ?)'
        query += ";"
        input = tuple(time_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor)
        self.disconnect(connection)
        return file_list

    def getPieceByTempo(self, tempos):
        tempo_list = []
        tempo_tuple_list = []
        dot_count = 0
        converter = {"crotchet":"quarter","quaver":"eighth","minim":"half","semibreve":"whole"}
        for tempo in tempos:
            parts = tempo.split("=")
            beat_one = parts[0]
            beat = -1
            if parts[0][:4] == "semi" or parts[0][:4] == "hemi" or parts[0][:4] == "demi":
                    index = 4
                    last_index = 0
                    number = 8
                    while index < len(parts[0]):
                        section = parts[0][last_index:index]
                        if section == "semi" or section == "hemi" or section == "demi":
                            number *= 2
                        else:
                            break
                        last_index = index
                        index += 4
                    beat_2_str_digit = str(number)
                    if beat_2_str_digit == "2":
                        beat_2_str_digit += "nd"
                    else:
                        beat_2_str_digit += "th"
                    beat = beat_2_str_digit

            if parts[0][-1] == ".":
                index = len(parts[0])-1
                while index > -1:
                    if parts[0][index] == ".":
                        beat_one = beat_one[:-1]
                        dot_count += 1
                    else:
                        break
                    index -= 1
            if beat_one in converter and beat == -1:
                beat = converter[parts[0]]

            elif beat == -1:
                beat = parts[0]

            beat+= "".join(["." for dot in range(dot_count)])
            beat_2 = -1
            minute = -1
            try:
                minute = int(parts[1])
            except:
                if parts[1][:5] == "semi" or parts[1][:5] == "hemi" or parts[1][:5] == "demi":
                    index = 0
                    last_index = 0
                    number = 8
                    while index < len(parts[1]):
                        section = parts[1][last_index:index]
                        if section == "semi" or section == "hemi" or section == "demi":
                            number *= 2
                        else:
                            break
                        last_index = index
                        index += 4
                    beat_2_str_digit = str(number)
                    if number[-1] == "2":
                        beat_2_str_digit += "nd"
                    else:
                        beat_2_str_digit += "th"
                    beat_2 = beat_2_str_digit

                if parts[1] in converter:
                    beat_2 = converter[parts[1]]
                elif beat_2 == -1:
                    beat_2 = parts[1]
            tempo_list.append((beat,minute,beat_2))
            tempo_tuple_list.append(beat)
            tempo_tuple_list.append(minute)
            tempo_tuple_list.append(beat_2)

        connection, cursor = self.connect()
        tempo_ids = [self.getTempoId(tempo[0],tempo[1],tempo[2], cursor) for tempo in tempo_list]
        query = 'SELECT i.piece_id FROM tempo_piece_join i WHERE EXISTS (SELECT * FROM tempo_piece_join WHERE piece_id = i.piece_id AND tempo_id = ?)'
        for i in range(1,len(tempo_ids)):
            query += ' AND EXISTS (SELECT * FROM tempo_piece_join WHERE piece_id = i.piece_id AND tempo_id = ?)'
        query += ";"
        input = tuple(tempo_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor)
        self.disconnect(connection)
        return file_list

    def getInstrumentsByPieceId(self, piece_id, cursor):
        instrument_query = 'SELECT instrument_id FROM instruments_piece_join WHERE piece_id=?'
        cursor.execute(instrument_query,(piece_id,))
        instrument_ids = cursor.fetchall()
        instruments = []
        for id in instrument_ids:
            data = {}
            q = 'SELECT * FROM instruments WHERE ROWID=?'
            cursor.execute(q, id)
            record = cursor.fetchone()
            if record is not None and len(record) > 0:
                data["name"] = record[0]
                if record[1] != 0 or record[2] != 0:
                    data["transposition"] = {"diatonic":record[1],"chromatic":record[2]}
                instruments.append(data)

        return instruments

    def getInstrumentByTransposition(self, transposition):
        connection, cursor = self.connect()
        data = []
        instrument_query = 'SELECT ROWID, name FROM instruments WHERE'
        keys = list(transposition.keys())
        for index in range(len(keys)):
            instrument_query += ' '+keys[index]+"=?"
            if index != len(keys) -1:
                instrument_query += ' AND'
            data.append(transposition[keys[index]])

        cursor.execute(instrument_query,tuple(data))
        instruments = cursor.fetchall()
        self.disconnect(connection)
        return instruments

    def getInstrumentsBySameTranspositionAs(self, instrument):
        connection, cursor = self.connect()
        instrument_query = '''SELECT i2.ROWID, i2.name FROM instruments i1, instruments i2
                              WHERE i1.name = ? AND i2.diatonic = i1.diatonic
                              AND i2.chromatic = i1.chromatic
                              AND i2.name != i1.name'''
        cursor.execute(instrument_query, (instrument,))
        instruments = cursor.fetchall()
        self.disconnect(connection)
        return instruments

    def getPieceByInstrumentsOrSimilar(self, instruments):
        '''
        method which searches first for any pieces containing the exact instrument, then by the name in dict,
        then by the transposition of the name if it isn't in the instruments table.
        :param instruments: list of instruments to search by
        :return: list of files + their instruments
        '''
        connection, cursor = self.connect()
        instrument_names = [entry["name"] for entry in instruments]
        instrument_keys = []
        for name in instrument_names:
            key = self.getInstrumentId(name, cursor)
            if key is not None:
                instrument_keys.append((name, key))
            else:
                self.addInstruments([entry for entry in instruments if entry["name"] == name])
                key = self.getInstrumentId(name, cursor)
                instrument_keys.append((name, key))
        results = self.getPiecesByInstruments(instrument_names)
        if len(results) == 0:
            alternates = [(item, self.getInstrumentsBySameTranspositionAs(item[0])) for item in instrument_keys]
            query = '''SELECT piece_id FROM instruments_piece_join i WHERE EXISTS'''
            query_input = []
            for instrument in alternates:
                query_input.append(instrument[0][1])
                query += ''' (SELECT * FROM instruments_piece_join WHERE piece_id = i.piece_id AND instrument_id = ?'''
                for value in instrument[1]:
                    query_input.append(value[0])
                    query += ''' OR instrument_id =?'''
                query += ''')'''
                if instrument != alternates[-1]:
                    query += " AND EXISTS"
            query += ";"
            cursor.execute(query,tuple(query_input))
            results = cursor.fetchall()
            file_list = self.getPiecesByRowId(results, cursor)
        self.disconnect(connection)
        return file_list


    def getClefsByPieceId(self, piece_id, cursor):
        clef_query = 'SELECT clef_id, instrument_id FROM clef_piece_join WHERE piece_id=?'
        cursor.execute(clef_query,(piece_id,))
        clef_ids = cursor.fetchall()
        clefs = {}
        for id in clef_ids:
            q = 'SELECT clefs.name, instruments.name FROM clefs, instruments WHERE clefs.ROWID=? AND instruments.ROWID=?'
            cursor.execute(q, id)
            name = cursor.fetchone()
            if name is not None and len(name) > 0:
                if name[1] not in clefs:
                    clefs[name[1]] = []
                clefs[name[1]].append(name[0])
        return clefs

    def getKeysByPieceId(self, piece_id, cursor):
        key_query = 'SELECT key_id, instrument_id FROM key_piece_join WHERE piece_id=?'
        cursor.execute(key_query,(piece_id,))
        key_ids = cursor.fetchall()
        keys = {}
        for id in key_ids:
            q = 'SELECT keys.name, instruments.name FROM keys, instruments WHERE keys.ROWID=? AND instruments.ROWID=?'
            cursor.execute(q, id)
            name = cursor.fetchone()
            if len(name) > 0:
                if name[1] not in keys:
                    keys[name[1]] = []
                keys[name[1]].append(name[0])
        return keys

    def getTimeSigsByPieceId(self, piece_id, cursor):
        time_query = 'SELECT time_id FROM time_piece_join WHERE piece_id=?'
        cursor.execute(time_query,(piece_id,))
        time_ids = cursor.fetchall()
        meters = []
        for id in time_ids:
            q = 'SELECT * FROM timesigs WHERE ROWID=?'
            cursor.execute(q, id)
            timesig = cursor.fetchone()
            if timesig is not None and len(timesig) > 0:
                meters.append(str(timesig[0])+"/"+str(timesig[1]))
        return meters

    def getTemposByPieceId(self, piece_id, cursor):
        tempo_query = 'SELECT tempo_id FROM tempo_piece_join WHERE piece_id=?'
        cursor.execute(tempo_query,(piece_id,))
        tempo_ids = cursor.fetchall()
        tempos = []
        for id in tempo_ids:
            q = 'SELECT * FROM tempos WHERE ROWID=?'
            cursor.execute(q, id)
            tempo = cursor.fetchone()
            if tempo is not None and len(tempo) > 0:
                tempo_string = str(tempo[0])+"="
                if tempo[1] != -1:
                    tempo_string += str(tempo[1])
                elif tempo[2] != -1:
                    tempo_string += str(tempo[2])
                tempos.append(tempo_string)
        return tempos

    def getAllPieceInfo(self, filenames):
        file_data = []
        for filename in filenames:
            piece_tuple = self.getPiece(filename)
            if len(piece_tuple) > 0:
                piece_tuple = piece_tuple[0]
            else:
                break
            data = {"id":piece_tuple[0],"filename":piece_tuple[1],"title":piece_tuple[2],"composer_id":piece_tuple[3]}
            file_data.append(data)

        connection, cursor = self.connect()
        for file in file_data:
            index = file["id"]
            composer = file["composer_id"]
            if composer != -1:
                query = 'SELECT name FROM composers WHERE ROWID=?'
                cursor.execute(query,(composer,))
                fetched = cursor.fetchone()
                if len(fetched) > 0:
                    file["composer"] = fetched[0]
            else:
                file["composer"] = -1

            file["instruments"] = self.getInstrumentsByPieceId(index, cursor)
            file["clefs"] = self.getClefsByPieceId(index, cursor)
            file["keys"] = self.getKeysByPieceId(index, cursor)
            file["time_signatures"] = self.getTimeSigsByPieceId(index, cursor)
            file["tempos"] = self.getTemposByPieceId(index, cursor)
            file.pop("id")
            file.pop("composer_id")
        self.disconnect(connection)
        return file_data

    def removePieces(self, filenames):
        connection, cursor = self.connect()
        for file in filenames:
            id_query = '''SELECT ROWID from pieces WHERE filename=?'''
            cursor.execute(id_query, (file,))
            result = cursor.fetchone()
            instrument_query = '''DELETE FROM instruments_piece_join WHERE piece_id =?'''
            cursor.execute(instrument_query,result)
            tempo_query = '''DELETE FROM tempo_piece_join WHERE piece_id =?'''
            cursor.execute(tempo_query,result)
            key_query = '''DELETE FROM key_piece_join WHERE piece_id =?'''
            cursor.execute(key_query,result)
            clef_query = '''DELETE FROM clef_piece_join WHERE piece_id =?'''
            cursor.execute(clef_query,result)
            time_query = '''DELETE FROM time_piece_join WHERE piece_id =?'''
            cursor.execute(time_query,result)
            piece_query = '''DELETE FROM pieces WHERE ROWID=?'''
            cursor.execute(piece_query,result)
        connection.commit()
        self.disconnect(connection)


    def archivePieces(self, filenames):
        connection, cursor = self.connect()
        for file in filenames:
            id_query = '''UPDATE pieces SET archived = 1 WHERE filename=?'''
            cursor.execute(id_query,(file,))
        connection.commit()
        self.disconnect(connection)

    def getArchivedPieces(self):
        file_list = []
        connection, cursor = self.connect()
        query = '''SELECT filename FROM pieces WHERE archived = 1'''
        cursor.execute(query)
        results = cursor.fetchall()
        file_list = [result[0] for result in results]
        self.disconnect(connection)
        return file_list

    def disconnect(self, connection):
        '''
        method which shuts down db connection
        :param connection: connection object
        :return: None
        '''
        connection.close()