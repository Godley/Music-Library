"""
This class handles very low level queries to the database file, including
creation of tables when files are first created (will do if not exists so
there are no clashes), handling connection and disconnection from the DB,
etc.

There are 17 tables (heh):
- Instruments: lists all instrument names. Hopefully we should process the
                instrument names so that there aren't too many duplicates...
                This can be a little difficult with different languages/choices
                of how to name your parts.
- instrument_piece_join: join table between pieces and instruments
- tempo: lists all tempos. Easier to process than instruments so shouldn't be
many variants/duplicates
- tempo_piece_join: ...
- time: holds meters/time signatures. format is same as the short time sig poem.
            That may need to change in the case of weird time signatures.
- time_piece_join: ...
- key: holds key signatures. These are pre filled.
- key_piece_join: ...
- clef: holds clefs. also prefilled.
- clef_piece_join: ...
- composers: composers. Even harder than instruments to avoid duplicates here.
- lyricists: as above. Each piece is currently presumed to have 1 composer, 1 lyricist.
                Maybe this is too big an assumption, but anyway, piece table contains
                composer id/lyricist id link.
- pieces: contains any meta data which is probably unique to that piece, like title
            and filename.
- sources: links a piece id with the online source it came from. This is how we check if a
            piece is local.
- licenses: links a piece id with a license type. Licenses are actually text files stored in the app,
            we just store what file name/type to use.
- secrets: we need to look at this. Links each piece ID with its unique secret for accessing it on the API.

Beyond adding and getting basic information, there are some more complex query methods.
Explained below.

Any additions to this class should have relevant tests written before working on the feature.
Any new tables should really be discussed in issues/other comms platforms before doing a big change.
These can be found in ExtractMetadata/tests/testDataLayer. Please either expand those classes or if
there's going to be a lot to group, put them in a new test file.

"""

import sqlite3
from implementation.primaries.ExtractMetadata.classes.DataLayer import TableCreator


class TempoParser(object):
    converter = {"crotchet": "quarter",
                 "quaver": "eighth",
                 "minim": "half",
                 "semibreve": "whole",
                 "quarter": "quarter",
                 "eighth": "eighth",
                 "half": "half",
                 "whole": "whole"}
    halvers = ['semi', 'hemi', 'demi']
    def splitParts(self, tempo):
        return tempo.split("=")

    def parseHalvers(self, tempo):
        seg_length = 4
        index = 0
        value = 8
        while tempo[index:index+seg_length] in self.halvers:
            value *= 2
            index += seg_length
        return value

    def parseHalversToString(self, tempo):
        halver_str = str(self.parseHalvers(tempo))
        if halver_str[-1] == "2":
            halver_str += 'nd'
        else:
            halver_str += 'th'
        return halver_str


    def convertToAmerican(self, entry):
        if entry in self.converter:
            return self.converter[entry]

    def getDots(self, entry):
        end_of_word = len(entry) - 1
        dots = ''
        while end_of_word > -1:
            if entry[end_of_word] == '.':
                dots += '.'
            else:
                break
            end_of_word -= 1
        new_word = entry[:end_of_word+1]
        return dots, new_word

    def parseWord(self, word):
        dots, remaining = self.getDots(word)
        if word[:4] in self.halvers:
            value = self.parseHalversToString(remaining)
        else:
            value = self.convertToAmerican(remaining)
        return value + dots

    def decode(self, entry):
        parts = self.splitParts(entry)
        result = {}
        minute = -1
        beat_2 = -1
        beat = self.parseWord(parts[0])
        try:
            minute = int(parts[1])
        except ValueError:
            beat_2 = self.parseWord(parts[1])
        result['beat'] = beat
        result['minute'] = minute
        result['beat_2'] = beat_2
        return result

    def encode(self, entry):
        tempo_string = str(entry[0]) + "="
        if entry[1] != -1:
            tempo_string += str(entry[1])
        elif entry[2] != -1:
            tempo_string += str(entry[2])
        return tempo_string


class MusicData(TableCreator.TableCreator):

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
        self.createPlaylistTable()
        self.createSourcesTable()
        self.createLicenseTable()
        self.createSecretsTable()



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
            item_data = (item["name"], diatonic, chromatic)
            elements.append(item_data)
        cursor.executemany('INSERT INTO instruments VALUES(?,?,?)', elements)
        connection.commit()
        self.disconnect(connection)

    def getInstrumentNames(self):
        connection, cursor = self.connect()
        query = 'SELECT name FROM instruments'
        cursor.execute(query)
        results = cursor.fetchall()
        self.disconnect(connection)
        instruments = set([result[0].lower() for result in results])
        return list(instruments)



    def getComposer(self, composer, cursor):
        query = 'SELECT ROWID FROM composers WHERE name=?'
        cursor.execute(query, (composer,))
        composer_id = cursor.fetchone()
        return composer_id

    def getLyricist(self, lyricist, cursor):
        query = 'SELECT ROWID FROM lyricists WHERE name=?'
        cursor.execute(query, (lyricist,))
        return cursor.fetchone()

    def createOrGetComposer(self, composer, connection, cursor, piece_id):
        query = 'SELECT ROWID FROM composers WHERE name=?'
        composer_id = self.getComposer(composer, cursor)
        if composer_id is None:
            cursor.execute(
                    'INSERT INTO composers VALUES(?)', (composer,))
            connection.commit()
            cursor.execute(query, (composer,))
            composer_id = cursor.fetchone()
        if composer_id is not None:
            composer_id = composer_id[0]
            query = 'UPDATE pieces SET composer_id = ? WHERE ROWID = ?'
            cursor.execute(query, (composer_id, piece_id))
            connection.commit()

    def createOrGetLyricist(self, lyricist, connection, cursor, piece_id):
        query = 'SELECT ROWID FROM lyricists WHERE name=?'
        lyricist_id = None
        lyric_id = self.getLyricist(lyricist, cursor)
        if lyric_id is None or len(lyric_id) == 0:
            cursor.execute(
                'INSERT INTO lyricists VALUES(?)', (lyricist,))
            connection.commit()
            cursor.execute(query, (lyricist,))
            lyric_id = cursor.fetchone()
        if lyric_id is not None:
            lyricist_id = lyric_id[0]
            query = 'UPDATE pieces SET lyricist_id = ? WHERE ROWID = ?'
            cursor.execute(query, (lyricist_id, piece_id))
            connection.commit()

    def getInstrumentId(self, instrument, cursor):
        diatonic = 0
        chromatic = 0
        if "transposition" in instrument:
                transposition = instrument["transposition"]
                if "diatonic" in transposition:
                    diatonic = transposition["diatonic"]
                if "chromatic" in transposition:
                    chromatic = transposition["chromatic"]
        query = 'SELECT ROWID FROM instruments WHERE name=? AND diatonic=? AND chromatic=?'
        cursor.execute(query, (instrument["name"], diatonic, chromatic,))
        inst_id = cursor.fetchall()
        return inst_id

    def createOrGetInstruments(self, instrument_list, connection, cursor, piece_id):
        for item in instrument_list:
            diatonic = 0
            chromatic = 0

            if len(inst_id) == 0:
                cursor.execute(
                    'INSERT INTO instruments VALUES(?,?,?)',
                    (item["name"],
                     diatonic,
                     chromatic,
                     ))
                connection.commit()
                inst_id = self.getInstrumentId(item, cursor)
            if inst_id is not None and len(inst_id) > 0:
                cursor.execute(
                    'INSERT INTO instruments_piece_join VALUES(?,?)',
                    (inst_id[0][0],
                     piece_id,
                     ))

    def createKeyLinks(self, keysig_dict, connection, cursor, piece_id):
        for instrument in keysig_dict:
            for key in keysig_dict[instrument]:
                fifths = 0
                mode = "major"
                if "fifths" in key:
                    fifths = key["fifths"]
                if "mode" in key:
                    mode = key["mode"]
                instrument_id = self.getInstrumentId(instrument, cursor)
                if instrument_id is None:
                    instrument_id = -1
                cursor.execute(
                    'SELECT ROWID FROM keys WHERE fifths=? AND mode=?', (fifths, mode,))
                key = cursor.fetchone()
                if key is not None and len(key) > 0:
                    cursor.execute(
                        'INSERT INTO key_piece_join VALUES(?,?,?)',
                        (key[0],
                         piece_id,
                         instrument_id,
                         ))

    def createClefLinks(self, clef_dict, connection, cursor, piece_id):
        for instrument in clef_dict:
            for clef in clef_dict[instrument]:
                sign = "G"
                line = 2
                if "sign" in clef:
                    sign = clef["sign"]
                if "line" in clef:
                    line = clef["line"]
                instrument_id = self.getInstrumentId(instrument, cursor)
                if instrument_id is None:
                    instrument_id = -1
                cursor.execute(
                    'SELECT ROWID FROM clefs WHERE sign=? AND line=?', (sign, line,))
                clef_id = cursor.fetchone()
                if clef_id is not None and len(clef_id) > 0:
                    cursor.execute(
                        'INSERT INTO clef_piece_join VALUES(?,?,?)',
                        (clef_id[0],
                         piece_id,
                         instrument_id,
                         ))

    def createTimeSigsAndLinks(self, timesig_list, connection, cursor, piece_id):
        for meter in timesig_list:
            beat = meter["beat"]
            b_type = meter["type"]
            cursor.execute(
                'SELECT ROWID FROM timesigs WHERE beat=? AND b_type=?', (beat, b_type))
            res = cursor.fetchone()
            if res is None or len(res) == 0:
                cursor.execute(
                    'INSERT INTO timesigs VALUES(?,?)', (beat, b_type))
                connection.commit()
                cursor.execute(
                    'SELECT ROWID FROM timesigs WHERE beat=? AND b_type=?', (beat, b_type))
                res = cursor.fetchone()
            cursor.execute(
                'INSERT INTO time_piece_join VALUES(?,?)', (piece_id, res[0]))

    def createTempoAndLinks(self, tempo_list, connection, cursor, piece_id):
        for tempo in tempo_list:
            beat = tempo["beat"]
            beat_2 = -1
            minute = -1
            if "beat_2" in tempo:
                beat_2 = tempo["beat_2"]
            if "minute" in tempo:
                minute = tempo["minute"]
            cursor.execute(
                'SELECT ROWID FROM tempos WHERE beat=? AND beat_2=? AND minute=?',
                (beat,
                 beat_2,
                 minute))
            res = cursor.fetchone()
            if res is None or len(res) == 0:
                cursor.execute(
                    'INSERT INTO tempos VALUES(?,?,?)',
                    (beat,
                     minute,
                     beat_2))
                connection.commit()
                cursor.execute(
                    'SELECT ROWID FROM tempos WHERE beat=? AND beat_2=? AND minute=?',
                    (beat,
                     beat_2,
                     minute))
                res = cursor.fetchone()
            cursor.execute(
                'INSERT INTO tempo_piece_join VALUES(?,?)', (piece_id, res[0]))

    def setSource(self, source, connection, cursor, piece_id):
        query = 'INSERT INTO sources VALUES(?,?)'
        cursor.execute(query, (piece_id, source,))

    def setSecret(self, secret, connection, cursor, piece_id):
        query = 'INSERT INTO secrets VALUES(?,?)'
        cursor.execute(query, (piece_id, secret,))

    def setLicense(self, license, connection, cursor, piece_id):
        query = 'INSERT INTO licenses VALUES(?,?)'
        cursor.execute(query, (piece_id, license,))

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
        method_table = {"composer": self.createOrGetComposer, "lyricist": self.createOrGetLyricist,
                        "instruments": self.createOrGetInstruments, "key": self.createKeyLinks,
                        "clef": self.createClefLinks, "time": self.createTimeSigsAndLinks,
                        "tempo": self.createTempoAndLinks, "source": self.setSource,
                        "secret": self.setSecret, "license": self.setLicense}

        if "title" in data:
            title = data["title"]
            data.pop("title")

        query_input = (filename, title, composer_id, lyricist_id, False)
        cursor.execute('INSERT INTO pieces VALUES(?,?,?,?,?)', query_input)
        connection.commit()
        select_input = (filename,)
        cursor.execute(
            'SELECT ROWID FROM pieces WHERE filename=?',
            select_input)
        piece_id = cursor.fetchone()[0]

        if "instruments" in data:
            self.createOrGetInstruments(data["instruments"], connection, cursor, piece_id)
            data.pop("instruments")

        if "id" in data:
            data.pop("id")

        table_info = {}
        for key in data:
            table_info[key] = method_table[key](data[key], connection, cursor, piece_id)

        connection.commit()
        self.disconnect(connection)

    def getFileList(self, online=False):
        connection, cursor = self.connect()
        query = 'SELECT filename FROM pieces p WHERE p.archived=0'
        if not online:
            query += ' AND NOT EXISTS(SELECT * FROM sources WHERE piece_id = p.ROWID)'
        else:
            query += ' AND EXISTS(SELECT * FROM sources WHERE piece_id = p.ROWID)'
        cursor.execute(query)
        results = cursor.fetchall()
        self.disconnect(connection)
        filelist = set([result[0] for result in results])
        return list(filelist)

    def getLicense(self, filename):
        connection, cursor = self.connect()
        query = 'SELECT license FROM licenses l, pieces p WHERE p.filename = ? AND l.piece_id = p.ROWID'
        cursor.execute(query, (filename,))
        result = cursor.fetchone()
        self.disconnect(connection)
        return result

    def getRoughPiece(self, filename, archived=0, online=False):
        """
        method to get a piece's table entry according to it's filename.
        This is used in cases where the user has started to type a filename
        but may not have entered the whole filename yet.

        Returns all results found for this string.
        """

        connection, cursor = self.connect()
        thing = (filename, "%" + filename + "%", archived,)
        query = 'SELECT ROWID, filename, title, composer_id, lyricist_id FROM pieces p WHERE (p.filename=? OR p.filename LIKE ?) AND p.archived=?'
        query = self.do_online_offline_query(query, 'p.ROWID', online=online)
        cursor.execute(query, thing)

        result = cursor.fetchall()
        self.disconnect(connection)
        return result

    def getExactPiece(self, filename, archived=0, online=False):
        """
        Method to get piece by exactly the string entered with no wildcards.
        This is used in cases where user has entered "*.xml" or filename:<this>
        or for getting a file having found its filename elsewhere.

        Returns 1 metadata collection assuming file names are unique.
        """
        connection, cursor = self.connect()
        thing = (filename, archived,)
        query = 'SELECT ROWID, filename, title, composer_id, lyricist_id FROM pieces p WHERE (p.filename=?) AND p.archived=?'
        query = self.do_online_offline_query(query, 'p.ROWID', online=online)
        cursor.execute(query, thing)

        result = cursor.fetchone()
        self.disconnect(connection)
        return result

    # helper methods which go to specific tables looking for a ROWID
    def getTimeId(self, beats, type, cursor):
        """fetch a time signature ID by its beats and type of beats"""
        cursor.execute(
            'SELECT ROWID FROM timesigs WHERE beat=? AND b_type=? ',
            (beats,
             type))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    def getTempoId(self, beat, minute, beat_2, cursor):
        """
        fetch a tempo ID by its beats.
        """
        cursor.execute(
            'SELECT ROWID FROM tempos WHERE beat=? AND minute=? AND beat_2=? ',
            (beat,
             minute,
             beat_2))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    def getInstrumentIdWhereTextInName(self, instrument, cursor):
        """
        similar to get rough piece. Try and figure out an instrument ID by
        a partial instrument name

        Returns a list of all IDs matching the string
        """
        cursor.execute(
            'SELECT ROWID FROM instruments WHERE name=? OR name LIKE ?',
            (instrument,
             "%" +
             instrument +
             "%"))
        result = cursor.fetchall()
        instrument_ids = [id[0] for id in result]
        return instrument_ids

    def getInstrumentId(self, instrument, cursor):
        """
        gets exact instrument ID based only on its name with no wildcards
        """
        cursor.execute(
            'SELECT ROWID FROM instruments WHERE name=?', (instrument,))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    def getComposerIdWhereTextInName(self, composer, cursor):
        """
        method which takes in composer name and outputs its database id
        :param composer: name of composer
        :param cursor: database cursor object
        :return: int pertaining to row id of composer in database
        """
        cursor.execute(
            'SELECT ROWID FROM composers WHERE name=? OR name LIKE ? OR name LIKE ? OR name LIKE ?',
            (composer,
             "%" +
             composer +
             "%",
             "%" + composer,
             composer + "%",))
        result = cursor.fetchall()
        composer_ids = [res[0] for res in result]
        return composer_ids

    def getComposerId(self, composer, cursor):
        """
        method which takes in composer name and outputs its database id
        :param composer: name of composer
        :param cursor: database cursor object
        :return: int pertaining to row id of composer in database
        """
        cursor.execute('SELECT ROWID FROM composers WHERE name=?', (composer,))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    def getLyricistIdWhereTextInName(self, lyricist, cursor):
        """
        get a list of lyricist IDs containing the lyricist string
        returns all matching ids
        """
        cursor.execute(
            'SELECT ROWID FROM lyricists WHERE name=? OR name LIKE ? OR name LIKE ? OR name LIKE ?',
            (lyricist,
             "%" +
             lyricist +
             "%",
             lyricist + "%",
             "%" + lyricist,))
        result = cursor.fetchall()
        lyricist_ids = [res[0] for res in result]
        return lyricist_ids

    def getLyricistId(self, lyricist, cursor):
        """
        get an exact lyricist id by its name.
        Returns 1 id
        """
        cursor.execute('SELECT ROWID FROM lyricists WHERE name=?', (lyricist,))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    def getKeyId(self, key, cursor):
        """
        method which takes in string of key name (e.g C major) and outputs row id
        :param key: string name of the key (e.g C major, A minor)
        :param cursor:  database cursor object
        :return: int pertaining to row id
        """

        cursor.execute('SELECT ROWID FROM keys WHERE name=?', (key,))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    def getClefId(self, clef, cursor):
        """
        method which takes in string of clef name (e.g treble) and outputs row id
        :param key: string name of the clef (e.g treble, bass)
        :param cursor:  database cursor object
        :return: int pertaining to row id
        """

        cursor.execute('SELECT ROWID FROM clefs WHERE name=?', (clef,))
        result = cursor.fetchall()
        if len(result) > 0:
            return result[0][0]

    # methods used in querying by user
    def getPiecesByInstruments(self, instruments, archived=0, online=False):
        """
        method to get all the pieces containing a certain instrument
        :param instrument: name of instrument
        :return: list of files containing that instrumnet
        """
        connection, cursor = self.connect()
        instrument_ids = [
            self.getInstrumentIdWhereTextInName(
                instrument,
                cursor) for instrument in instruments]
        tuple_ids = []
        [tuple_ids.extend(inst_id) for inst_id in instrument_ids]
        file_list = []
        if len(tuple_ids) > 0:
            query = 'SELECT i.piece_id FROM instruments_piece_join i WHERE EXISTS '
            for i in range(len(instrument_ids)):
                query += '(SELECT * FROM instruments_piece_join WHERE piece_id = i.piece_id'
                # for every new instrument update the query
                for result in instrument_ids[i]:
                    if result == instrument_ids[i][0]:
                        query += ' AND '
                        query += '('
                    query += 'instrument_id = ?'
                    if result != instrument_ids[i][-1]:
                        query += ' OR '
                    else:
                        query += ')'
                query += ')'
                if i != len(instrument_ids) - 1:
                    query += ' AND EXISTS '
            if online:
                query += ' AND EXISTS(SELECT * FROM sources WHERE piece_id = i.piece_id)'
            else:
                query += ' AND NOT EXISTS(SELECT * FROM sources WHERE piece_id = i.piece_id)'
            query += ";"

            input = tuple(tuple_ids)
            cursor.execute(query, input)
            results = cursor.fetchall()

            file_list = self.getPiecesByRowId(results, cursor, archived)
            self.disconnect(connection)
        return file_list

    def getPiecesByAnyAndAllInstruments(self, instruments, archived=0, online=False):
        """
        Runs 2 queries:
        1. Fetch a piece that contains all of the instruments listed in instruments.
        2. Iterate through the list asking for the individual pieces containing that instrument,
        but possibly not all of them.

        Returns a dictionary containing "Instrument: "<each instrument> as keys to which each
        value is a list of the pieces containing that instrument, and, if there are any,
        a key "All Instruments" which is matched to a list of all pieces containing every instrument
        requested.
        """
        all_pieces = self.getPiecesByInstruments(instruments, archived=archived, online=online)
        any = {"Instrument: "+instrument: self.getPiecesByInstruments([instrument], archived=archived, online=online) for instrument in instruments}
        result = {}
        if len(all_pieces) > 0:
            result['All Instruments'] = all_pieces
        result.update({key: any[key] for key in any if len(any[key]) > 0})
        return result



    def getPiecesByRowId(self, rows, cursor, archived=0):
        """
        method which takes in a list of rows which are ROWIDs in the piece table and returns a list of files
        :param rows: list of tuples pertaining to ROWIDs in pieces table
        :param cursor: connection cursor object
        :return: list of strings pertaining to xml files
        """
        file_list = []
        previous = None
        for element in rows:
            if element != previous:
                cursor.execute(
                    'SELECT filename FROM pieces WHERE ROWID=? AND archived=?',
                    (element[0],
                     archived))
                result = cursor.fetchone()
                if result is not None:
                    file_list.append(result[0])
            previous = element
        return file_list

    def getPiecesByComposer(self, composer, archived=0, online=False):
        """
        method which takes in string of composer name and outputs list of files written by that composer
        :param composer: composer's name
        :return: list of strings (filenames)
        """
        file_list = []
        connection, cursor = self.connect()
        composer_ids = self.getComposerIdWhereTextInName(composer, cursor)
        if len(composer_ids) > 0:
            query = 'SELECT filename FROM pieces p WHERE p.archived=? AND (p.composer_id=?'
            for id in composer_ids:
                if id != composer_ids[-1]:
                    query += "OR p.composer_id LIKE ?"
                if id == composer_ids[-1]:
                    query += ")"
            if online:
                query += ' AND EXISTS(SELECT * FROM sources WHERE piece_id = p.ROWID)'
            else:
                query += ' AND NOT EXISTS(SELECT * FROM sources WHERE piece_id = p.ROWID)'
            input_list = [archived]
            input_list.extend(composer_ids)
            input = tuple(input_list)
            cursor.execute(query, input)
            result = cursor.fetchall()
            file_list = [r[0] for r in result]
            self.disconnect(connection)
        return file_list

    def getPiecesByLyricist(self, lyricist, archived=0, online=False):
        """
        method which takes in string of lyricist name and outputs list of files written by that lyricist
        :param composer: lyricist's name
        :return: list of strings (filenames)
        """
        connection, cursor = self.connect()
        lyricist_ids = self.getLyricistIdWhereTextInName(lyricist, cursor)
        file_list = []
        if len(lyricist_ids) > 0:
            query = 'SELECT filename FROM pieces p WHERE p.archived=? AND (p.lyricist_id=?'
            for id in lyricist_ids:
                if id != lyricist_ids[-1]:
                    query += "OR p.lyricist_id LIKE ?"
                if id == lyricist_ids[-1]:
                    query += ")"
            if online:
                query += ' AND EXISTS(SELECT * FROM sources WHERE piece_id = p.ROWID)'
            else:
                query += ' AND NOT EXISTS(SELECT * FROM sources WHERE piece_id = p.ROWID)'
            input_list = [archived]
            input_list.extend(lyricist_ids)
            input = tuple(input_list)
            cursor.execute(query, input)
            result = cursor.fetchall()
            file_list = [r[0] for r in result]
            self.disconnect(connection)
        return file_list

    def getPieceByTitle(self, title, archived=0, online=False):
        """
        method which takes in title of piece and outputs list of files named that
        :param title: title of piece
        :return: list of tuples
        """
        connection, cursor = self.connect()
        thing = (title, "%" + title + "%", title + "%", "%" + title, archived,)
        query = 'SELECT * FROM pieces p WHERE (p.title=? OR p.title LIKE ? OR p.title LIKE ? OR p.title LIKE ?) AND p.archived=?'
        if online:
            query += ' AND EXISTS(SELECT * FROM sources WHERE piece_id = p.ROWID)'
        else:
            query += ' AND NOT EXISTS(SELECT * FROM sources WHERE piece_id = p.ROWID)'
        cursor.execute(query, thing)
        result = cursor.fetchall()
        result = [r[0] for r in result]
        self.disconnect(connection)
        return result

    def getPieceByKeys(self, keys, archived=0, online=False):
        """
        method which takes in a key and outputs list of files in that key
        :param key: string name of key (e.g C major)
        :return: list of strings (files)
        """
        connection, cursor = self.connect()
        key_ids = [self.getKeyId(key, cursor) for key in keys]
        query = 'SELECT i.piece_id FROM key_piece_join i WHERE EXISTS (SELECT * FROM key_piece_join WHERE piece_id = i.piece_id AND key_id = ?)'
        for i in range(1, len(key_ids)):
            query += ' AND EXISTS (SELECT * FROM key_piece_join WHERE piece_id = i.piece_id AND key_id = ?)'
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = i.piece_id)'
        query += ";"
        input = tuple(key_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor, archived)
        self.disconnect(connection)
        return file_list

    def getPiecesByModularity(self, modularity, archived=0, online=False):
        """

        :param modularity:
        :param archived:
        :param online:
        :return:
        """
        connection, cursor = self.connect()
        query = 'SELECT key_piece.piece_id FROM keys k, key_piece_join key_piece WHERE k.mode = ? AND key_piece.key_id = k.ROWID'
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = key_piece.piece_id)'
        cursor.execute(query, (modularity,))
        key_set = cursor.fetchall()
        file_list = self.getPiecesByRowId(key_set, cursor, archived)
        self.disconnect(connection)
        return file_list

    # playlist queries
    def getPiecesByAllKeys(self, archived=0, online=False):
        connection, cursor = self.connect()
        query = '''SELECT k.name, piece.filename FROM keys k, pieces piece, key_piece_join key_piece, instruments i
                    WHERE key_piece.key_id = k.ROWID AND i.ROWID = key_piece.instrument_id
                    AND i.diatonic = 0 AND i.chromatic = 0 AND piece.ROWID = key_piece.piece_id
                    AND piece.archived = ? AND EXISTS (SELECT NULL FROM key_piece_join WHERE key_id = k.ROWID AND piece_id != key_piece.piece_id)
        '''
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = piece.ROWID)'
        cursor.execute(query, (archived,))
        results = cursor.fetchall()
        self.disconnect(connection)
        key_dict = {}
        for pair in results:
            if pair[0] not in key_dict:
                key_dict[pair[0]] = []
            key_dict[pair[0]].append(pair[1])
        return key_dict

    def getPiecesByAllClefs(self, archived=0, online=False):
        connection, cursor = self.connect()
        query = '''SELECT clef.name, piece.filename FROM clefs clef, pieces piece, clef_piece_join clef_piece
                    WHERE clef_piece.clef_id = clef.ROWID AND piece.ROWID = clef_piece.piece_id
                    AND piece.archived = ? AND EXISTS (SELECT NULL FROM clef_piece_join WHERE clef_id = clef_piece.clef_id AND piece_id != clef_piece.piece_id)
        '''
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = piece.ROWID)'
        cursor.execute(query, (archived,))
        results = cursor.fetchall()
        self.disconnect(connection)
        clef_dict = {}
        for pair in results:
            if pair[0] not in clef_dict:
                clef_dict[pair[0]] = []
            clef_dict[pair[0]].append(pair[1])
        return clef_dict

    def getPiecesByAllTimeSigs(self, archived=0, online=False):
        connection, cursor = self.connect()
        query = '''SELECT time_sig.beat, time_sig.b_type, piece.filename FROM timesigs time_sig, pieces piece, time_piece_join time_piece
                    WHERE time_piece.time_id = time_sig.ROWID AND piece.ROWID = time_piece.piece_id
                    AND piece.archived = ? AND EXISTS(SELECT null FROM time_piece_join WHERE time_id=time_sig.ROWID AND time_piece_join.piece_id != time_piece.piece_id)
        '''
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = piece.ROWID)'
        cursor.execute(query, (archived,))
        results = cursor.fetchall()
        self.disconnect(connection)
        timesig_dict = {}
        for pair in results:
            result_key = str(pair[0]) + "/" + str(pair[1])
            if result_key not in timesig_dict:
                timesig_dict[result_key] = []
            timesig_dict[result_key].append(pair[2])
        return timesig_dict

    def getPiecesByAllTempos(self, archived=0, online=False):
        connection, cursor = self.connect()
        query = '''SELECT tempo.beat, tempo.beat_2, tempo.minute, piece.filename
                  FROM tempos tempo, pieces piece, tempo_piece_join tempo_piece
                    WHERE tempo_piece.tempo_id = tempo.ROWID AND piece.ROWID = tempo_piece.piece_id
                    AND EXISTS (SELECT * FROM tempo_piece_join WHERE tempo_id = tempo_piece.tempo_id AND piece_id != tempo_piece.piece_id)
                    AND piece.archived = ?
        '''
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = piece.ROWID)'
        cursor.execute(query, (archived,))
        results = cursor.fetchall()
        self.disconnect(connection)
        tempo_dict = {}
        for pair in results:
            key_input = pair[0] + "="
            if pair[1] != "-1":
                key_input += pair[1]
            elif pair[2] != -1:
                key_input += str(pair[2])
            if key_input not in tempo_dict:
                tempo_dict[key_input] = []
            tempo_dict[key_input].append(pair[3])
        return tempo_dict

    def getPiecesByAllInstruments(self, archived=0, online=False):
        connection, cursor = self.connect()
        query = '''SELECT instrument.name, instrument.diatonic, instrument.chromatic, piece.filename
                  FROM instruments instrument, pieces piece, instruments_piece_join instrument_piece
                    WHERE instrument_piece.instrument_id = instrument.ROWID AND piece.ROWID = instrument_piece.piece_id
                    AND EXISTS (SELECT * FROM instruments_piece_join WHERE instrument_id = instrument_piece.instrument_id AND piece_id != instrument_piece.piece_id)
                    AND piece.archived = ?
        '''
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = piece.ROWID)'
        cursor.execute(query, (archived,))
        results = cursor.fetchall()
        self.disconnect(connection)
        instrument_dict = {}
        for pair in results:
            key_input = pair[0]
            if pair[1] != 0 or pair[2] != 0:
                key_input += "\n("
                key_input += "Transposed By "
            if pair[1] != 0:
                key_input += str(pair[1]) + " Diatonic \n"
            if pair[2] != 0:
                key_input += str(pair[2]) + " Chromatic"
            if pair[1] != 0 or pair[2] != 0:
                key_input += ")"
            if key_input not in instrument_dict:
                instrument_dict[key_input] = []
            instrument_dict[key_input].append(pair[3])
        return instrument_dict

    def getPiecesByAllComposers(self, archived=0, online=False):
        connection, cursor = self.connect()
        query = '''SELECT comp.name, piece.filename FROM composers comp, pieces piece
                    WHERE piece.composer_id = comp.ROWID
                    AND EXISTS (SELECT * FROM pieces WHERE composer_id = comp.ROWID AND ROWID != piece.ROWID)
                    AND piece.archived = ?
        '''
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = piece.ROWID)'
        cursor.execute(query, (archived,))
        results = cursor.fetchall()
        self.disconnect(connection)
        composer_dict = {}
        for pair in results:
            if pair[0] not in composer_dict:
                composer_dict[pair[0]] = []
            composer_dict[pair[0]].append(pair[1])
        return composer_dict

    def getPiecesByAllLyricists(self, archived=0, online=False):
        connection, cursor = self.connect()
        query = '''SELECT lyric.name, piece.filename FROM lyricists lyric, pieces piece
                    WHERE lyric.ROWID = piece.lyricist_id
                    AND EXISTS (SELECT * FROM pieces WHERE lyricist_id = piece.lyricist_id AND ROWID != piece.ROWID)
                    AND piece.archived = ?
        '''
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = piece.ROWID)'
        cursor.execute(query, (archived,))
        results = cursor.fetchall()
        self.disconnect(connection)
        lyricist_dict = {}
        for pair in results:
            if pair[0] not in lyricist_dict:
                lyricist_dict[pair[0]] = []
            lyricist_dict[pair[0]].append(pair[1])
        return lyricist_dict

    def getPieceByClefs(self, clefs, archived=0, online=False):
        '''
        method which takes in a key and outputs list of files in that key
        :param key: string name of key (e.g C major)
        :return: list of strings (files)
        '''
        connection, cursor = self.connect()
        clef_ids = [self.getClefId(clef, cursor) for clef in clefs]
        query = 'SELECT i.piece_id FROM clef_piece_join i WHERE EXISTS (SELECT * FROM clef_piece_join WHERE piece_id = i.piece_id AND clef_id = ?)'
        for i in range(1, len(clef_ids)):
            query += ' AND EXISTS (SELECT * FROM clef_piece_join WHERE piece_id = i.piece_id AND clef_id = ?)'
        if online:
            query += ' AND EXISTS '
        else:
            query += ' AND NOT EXISTS '
        query += '(SELECT * FROM sources WHERE piece_id = i.piece_id)'
        query += ";"
        input = tuple(clef_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor, archived)
        self.disconnect(connection)
        return file_list

    def getPieceByInstrumentInKeys(self, data, archived=0, online=False):
        connection, cursor = self.connect()
        search_ids = []
        tuple_data = [instrument for instrument in data]
        key_ids = {}
        file_list = []
        for instrument in data:
            search_ids.append(self.getInstrumentId(instrument, cursor))
            key_ids[instrument] = []
            for key in data[instrument]:
                id = self.getKeyId(key, cursor)
                if id is not None:
                    search_ids.append(id)
                    key_ids[instrument].append(id)
        if len(tuple_data) > 0 and len(key_ids) > 0:
            query = 'SELECT key_piece.piece_id FROM key_piece_join key_piece WHERE EXISTS '
            for i in range(len(tuple_data)):
                query += '(SELECT * FROM key_piece_join WHERE piece_id = key_piece.piece_id AND instrument_id = ? AND '
                for j in range(len(key_ids[tuple_data[i]])):
                    query += 'key_id = ?'
                    if j != len(key_ids[tuple_data[i]]) - 1:
                        query += ' AND '
                query += ")"
                if i != len(tuple_data) - 1:
                    query += ' AND EXISTS '
            if online:
                query += ' AND EXISTS '
            else:
                query += ' AND NOT EXISTS '
            query += '(SELECT * FROM sources WHERE piece_id = key_piece.piece_id)'
            cursor.execute(query, tuple(search_ids))
            results = cursor.fetchall()

            file_list = self.getPiecesByRowId(results, cursor, archived)
        return file_list

    def getPieceByInstrumentInClefs(self, data, archived=0, online=False):
        connection, cursor = self.connect()
        search_ids = []
        tuple_data = [instrument for instrument in data]
        clef_ids = {}
        file_list = []
        for instrument in data:
            search_ids.append(self.getInstrumentId(instrument, cursor))
            clef_ids[instrument] = []
            for key in data[instrument]:
                id = self.getClefId(key, cursor)
                if id is not None:
                    search_ids.append(id)
                    clef_ids[instrument].append(id)
        if len(tuple_data) > 0 and len(clef_ids) > 0:
            query = 'SELECT clef_piece.piece_id FROM clef_piece_join clef_piece WHERE EXISTS '
            for i in range(len(tuple_data)):
                query += '(SELECT * FROM clef_piece_join WHERE piece_id = clef_piece.piece_id AND instrument_id = ? AND '
                for j in range(len(clef_ids[tuple_data[i]])):
                    query += 'clef_id = ?'
                    if j != len(clef_ids[tuple_data[i]]) - 1:
                        query += ' AND '
                query += ")"
                if i != len(tuple_data) - 1:
                    query += ' AND EXISTS '
            if online:
                query += ' AND EXISTS '
            else:
                query += ' AND NOT EXISTS '
            query += '(SELECT * FROM sources WHERE piece_id = clef_piece.piece_id)'
            cursor.execute(query, tuple(search_ids))
            results = cursor.fetchall()
            file_list = self.getPiecesByRowId(results, cursor, archived)
        return file_list

    def getPieceByMeter(self, meters, archived=0, online=False):
        meter_list = []
        for meter in meters:
            if "/" in meter:
                values = meter.split("/")
                beat = int(values[0])
                b_type = int(values[1])
                meter_list.append((beat, b_type))
        connection, cursor = self.connect()
        time_ids = [
            self.getTimeId(
                meter[0],
                meter[1],
                cursor) for meter in meter_list]
        query = 'SELECT i.piece_id FROM time_piece_join i WHERE EXISTS (SELECT * FROM time_piece_join WHERE piece_id = i.piece_id AND time_id = ?)'
        query = self.do_online_offline_query(query, 'i.piece_id', online=online)

        for i in range(1, len(time_ids)):
            query += ' AND EXISTS (SELECT * FROM time_piece_join WHERE piece_id = i.piece_id AND time_id = ?)'

        query += ";"
        input = tuple(time_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor, archived)
        self.disconnect(connection)
        return file_list

    def do_online_offline_query(self, query, piece_id_field, online=False):
        new_query = query
        if online:
            new_query += ' AND EXISTS '
        else:
            new_query += ' AND NOT EXISTS '
        new_query += '(SELECT * FROM sources WHERE piece_id = '+piece_id_field+')'
        return new_query

    def getPieceByTempo(self, tempos, archived=0, online=False):
        tempo_list = []
        tempo_tuple_list = []
        dot_count = 0
        converter = {
            "crotchet": "quarter",
            "quaver": "eighth",
            "minim": "half",
            "semibreve": "whole"}
        parser = TempoParser()
        for tempo in tempos:
            result = parser.decode(tempo)
            tempo_list.append((result['beat'], result['minute'], result['beat_2']))
        connection, cursor = self.connect()
        tempo_ids = [
            self.getTempoId(
                tempo[0],
                tempo[1],
                tempo[2],
                cursor) for tempo in tempo_list]
        query = 'SELECT i.piece_id FROM tempo_piece_join i WHERE EXISTS (SELECT * FROM tempo_piece_join WHERE piece_id = i.piece_id AND tempo_id = ?)'
        for i in range(1, len(tempo_ids)):
            query += ' AND EXISTS (SELECT * FROM tempo_piece_join WHERE piece_id = i.piece_id AND tempo_id = ?)'
        query = self.do_online_offline_query(query, 'i.piece_id', online=online)
        query += ";"
        input = tuple(tempo_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, cursor, archived)
        self.disconnect(connection)
        return file_list

    def getInstrumentsByPieceId(self, piece_id, cursor):
        instrument_query = 'SELECT instrument_id FROM instruments_piece_join WHERE piece_id=?'
        cursor.execute(instrument_query, (piece_id,))
        instrument_ids = set(cursor.fetchall())
        instruments = []
        for id in instrument_ids:
            data = {}
            q = 'SELECT * FROM instruments WHERE ROWID=?'
            cursor.execute(q, id)
            record = cursor.fetchone()
            if record is not None and len(record) > 0:
                data["name"] = record[0]
                if record[1] != 0 or record[2] != 0:
                    data["transposition"] = {
                        "diatonic": record[1],
                        "chromatic": record[2]}
                instruments.append(data)

        return instruments

    def getInstrumentByTransposition(self, transposition, online=False):
        connection, cursor = self.connect()
        data = []
        instrument_query = 'SELECT ROWID, name FROM instruments WHERE'
        keys = list(transposition.keys())
        for index in range(len(keys)):
            instrument_query += ' ' + keys[index] + "=?"
            if index != len(keys) - 1:
                instrument_query += ' AND'
            data.append(transposition[keys[index]])

        cursor.execute(instrument_query, tuple(data))
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

    def getPieceByInstrumentsOrSimilar(
            self,
            instruments,
            archived=0,
            online=False):
        """
        method which searches first for any pieces containing the exact instrument, then by the name in dict,
        then by the transposition of the name if it isn't in the instruments table.
        :param instruments: list of instruments to search by
        :return: list of files + their instruments
        """
        connection, cursor = self.connect()

        instrument_keys = []
        for name in instruments:
            if type(name) == str:
                key = self.getInstrumentId(name, cursor)
            else:
                key = self.getInstrumentId(name["name"], cursor)
            if key is not None:
                instrument_keys.append((name, key))
        results = self.getPiecesByInstruments(
            [instrument["name"] for instrument in instruments])
        if len(results) == 0:
            alternates = [
                (item,
                 self.getInstrumentsBySameTranspositionAs(
                     item[0]["name"])) for item in instrument_keys]
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

            query = self.do_online_offline_query(query, 'i.piece_id', online=online)
            query += ";"
            cursor.execute(query, tuple(query_input))
            results = cursor.fetchall()
            file_list = self.getPiecesByRowId(
                results,
                cursor,
                archived=archived)
        self.disconnect(connection)
        return file_list

    # again, helper methods for other methods which just go off and find the
    # joins for specific pieces
    def getClefsByPieceId(self, piece_id, cursor):
        clef_query = 'SELECT clef_id, instrument_id FROM clef_piece_join WHERE piece_id=?'
        cursor.execute(clef_query, (piece_id,))
        clef_ids = set(cursor.fetchall())
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
        cursor.execute(key_query, (piece_id,))
        key_ids = set(cursor.fetchall())
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
        cursor.execute(time_query, (piece_id,))
        time_ids = set(cursor.fetchall())
        meters = []
        for id in time_ids:
            q = 'SELECT * FROM timesigs WHERE ROWID=?'
            cursor.execute(q, id)
            timesig = cursor.fetchone()
            if timesig is not None and len(timesig) > 0:
                meters.append(str(timesig[0]) + "/" + str(timesig[1]))
        return meters

    def getTemposByPieceId(self, piece_id, cursor):
        tempo_query = 'SELECT tempo_id FROM tempo_piece_join WHERE piece_id=?'
        cursor.execute(tempo_query, (piece_id,))
        tempo_ids = set(cursor.fetchall())
        tempos = []
        for id in tempo_ids:
            q = 'SELECT * FROM tempos WHERE ROWID=?'
            cursor.execute(q, id)
            tempo = cursor.fetchone()
            parser = TempoParser()
            if tempo is not None and len(tempo) > 0:
                tempos.append(parser.encode(tempo))
        return tempos

    def getAllPieceInfo(self, filenames, archived=0, online=False):
        file_data = []
        for filename in filenames:
            piece_tuple = self.getExactPiece(filename, archived, online=online)
            if piece_tuple is not None:
                data = {
                    "id": piece_tuple[0],
                    "filename": piece_tuple[1],
                    "title": piece_tuple[2],
                    "composer_id": piece_tuple[3],
                    "lyricist_id": piece_tuple[4]}
                file_data.append(data)

        connection, cursor = self.connect()
        for file in file_data:
            index = file["id"]
            composer = file["composer_id"]
            if composer != -1:
                query = 'SELECT name FROM composers WHERE ROWID=?'
                cursor.execute(query, (composer,))
                fetched = cursor.fetchone()
                if fetched is not None and len(fetched) > 0:
                    file["composer"] = fetched[0]
                else:
                    file["composer"] = -1
            else:
                file["composer"] = -1

            lyricist = file["lyricist_id"]
            if lyricist != -1:
                query = 'SELECT name FROM lyricists WHERE ROWID=?'
                cursor.execute(query, (lyricist,))
                fetched = cursor.fetchone()
                if fetched is not None and len(fetched) > 0:
                    file["lyricist"] = fetched[0]
                else:
                    file["lyricist"] = -1
            else:
                file["lyricist"] = -1
            instruments = self.getInstrumentsByPieceId(index, cursor)
            if len(instruments) > 0:
                file["instruments"] = instruments
            clefs = self.getClefsByPieceId(index, cursor)
            if len(clefs) > 0:
                file["clefs"] = clefs
            keys = self.getKeysByPieceId(index, cursor)
            if len(keys) > 0:
                file["keys"] = keys
            timesigs = self.getTimeSigsByPieceId(index, cursor)
            if len(timesigs) > 0:
                file["time_signatures"] = timesigs
            tempos = self.getTemposByPieceId(index, cursor)
            if len(tempos) > 0:
                file["tempos"] = tempos
            file.pop("id")
            file.pop("composer_id")
            file.pop("lyricist_id")
        self.disconnect(connection)
        return file_data

    def addPlaylist(self, pname, files):
        connection, cursor = self.connect()
        cursor.execute('''INSERT INTO playlists VALUES(?)''', (pname,))
        cursor.execute(
            '''SELECT ROWID from playlists WHERE name = ?''', (pname,))
        val = cursor.fetchone()
        for name in files:
            cursor.execute(
                '''SELECT ROWID FROM pieces WHERE filename = ?''', (name,))
            file_id = cursor.fetchone()
            cursor.execute(
                '''INSERT INTO playlist_join VALUES(?,?)''',
                (val[0],
                 file_id[0]))
        connection.commit()
        self.disconnect(connection)

    def getAllUserPlaylists(self):
        connection, cursor = self.connect()
        cursor.execute(
            '''SELECT piece.filename, play.name, play.ROWID FROM playlists play, playlist_join playjoin, pieces piece
                          WHERE playjoin.playlist_id = play.ROWID and piece.ROWID = playjoin.piece_id''')
        results = cursor.fetchall()
        self.disconnect(connection)
        data = {}
        for item in results:
            if item[1] not in data:
                data[item[1]] = []
            data[item[1]].append(item[0])
        return data

    def getUserPlaylist(self, title):
        connection, cursor = self.connect()
        cursor.execute(
            '''SELECT ROWID from playlists WHERE name=?''', (title,))
        result = cursor.fetchone()
        self.disconnect(connection)
        return result[0]

    def updateUserPlaylist(self, rowid, data):
        connection, cursor = self.connect()
        if "title" in data:
            query = '''UPDATE playlists SET name = ? WHERE ROWID = ?'''
            cursor.execute(query, (data["title"], rowid,))

        if "pieces" in data:
            pass
        connection.commit()
        self.disconnect(connection)

    def getUserPlaylistsForFile(self, filename):
        data = {}
        connection, cursor = self.connect()
        query = '''SELECT playlist.name from playlists playlist, playlist_join play, pieces piece
                    WHERE piece.filename = ? AND piece.ROWID = play.piece_id'''
        cursor.execute(query, (filename,))
        results = cursor.fetchall()
        query_2 = '''SELECT piece.filename FROM pieces piece, playlist_join play, playlists playlist
                  WHERE playlist.name = ? AND play.playlist_id = playlist.ROWID AND piece.ROWID = play.piece_id'''
        for i in range(len(results)):
            cursor.execute(query_2, results[i])
            files = cursor.fetchall()
            if results[i][0] not in data:
                data[results[i][0]] = [file[0] for file in files]
        self.disconnect(connection)
        return data

    def deletePlaylist(self, playlist_name):
        connection, cursor = self.connect()
        id_query = '''SELECT ROWID FROM playlists WHERE name = ?'''
        cursor.execute(id_query, (playlist_name,))
        res = cursor.fetchone()
        query = '''DELETE FROM playlists WHERE name = ?'''
        cursor.execute(query, (playlist_name,))
        join_query = '''DELETE FROM playlist_join WHERE playlist_id = ?'''
        cursor.execute(join_query, res)
        connection.commit()
        self.disconnect(connection)

    # methods to clear out old records. In general we just archive them on the off chance the piece comes back -
    # if it does give the user the option to un-archive or else remove all old
    # data
    def removePieces(self, filenames):
        connection, cursor = self.connect()
        for file in filenames:
            id_query = '''SELECT ROWID from pieces WHERE filename=?'''
            cursor.execute(id_query, (file,))
            result = cursor.fetchone()
            instrument_query = '''DELETE FROM instruments_piece_join WHERE piece_id =?'''
            cursor.execute(instrument_query, result)
            tempo_query = '''DELETE FROM tempo_piece_join WHERE piece_id =?'''
            cursor.execute(tempo_query, result)
            key_query = '''DELETE FROM key_piece_join WHERE piece_id =?'''
            cursor.execute(key_query, result)
            clef_query = '''DELETE FROM clef_piece_join WHERE piece_id =?'''
            cursor.execute(clef_query, result)
            time_query = '''DELETE FROM time_piece_join WHERE piece_id =?'''
            cursor.execute(time_query, result)
            piece_query = '''DELETE FROM pieces WHERE ROWID=?'''
            cursor.execute(piece_query, result)
        connection.commit()
        self.disconnect(connection)

    def archivePieces(self, filenames):
        connection, cursor = self.connect()
        for file in filenames:
            id_query = '''UPDATE pieces SET archived = 1 WHERE filename=?'''
            cursor.execute(id_query, (file,))
        connection.commit()
        self.disconnect(connection)

    def unarchivePieces(self, filenames):
        connection, cursor = self.connect()
        for file in filenames:
            query = '''UPDATE pieces SET archived=0 WHERE filename=?'''
            cursor.execute(query, (file))
        connection.commit()
        self.disconnect(connection)

    def getArchivedPieces(self):
        connection, cursor = self.connect()
        query = '''SELECT filename FROM pieces WHERE archived = 1'''
        cursor.execute(query)
        results = cursor.fetchall()
        file_list = [result[0] for result in results]
        self.disconnect(connection)
        return file_list

    def getPieceSource(self, filename):
        connection, cursor = self.connect()
        query = 'SELECT source FROM sources, pieces p WHERE p.filename =? AND p.ROWID = sources.piece_id'
        cursor.execute(query, (filename,))
        result = cursor.fetchone()
        self.disconnect(connection)
        return result

    def downloadPiece(self, filename):
        """
        method to get rid of the source entry for a given filename
        :param filename:
        :return:
        """
        connection, cursor = self.connect()
        query = 'SELECT ROWID FROM pieces WHERE filename =?'
        cursor.execute(query, (filename,))
        result = cursor.fetchone()
        query = 'DELETE FROM sources WHERE piece_id = ?'
        cursor.execute(query, result)
        connection.commit()
        self.disconnect(connection)


