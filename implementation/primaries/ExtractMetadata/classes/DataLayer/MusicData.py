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
- time: holds meters/time signatures.
        format is same as the short time sig poem.
        That may need to change in the case of weird time signatures.
- time_piece_join: ...
- key: holds key signatures. These are pre filled.
- key_piece_join: ...
- clef: holds clefs. also prefilled.
- clef_piece_join: ...
- composers: composers. Even harder than instruments to avoid duplicates here.
- lyricists: as above. Each piece is currently presumed to have 1 composer,
            1 lyricist. Maybe this is too big an assumption, but anyway,
            piece table contains composer id/lyricist id link.
- pieces: contains any meta data which is probably unique to that piece,
            like title and filename.
- sources: links a piece id with the online source it came from.
            This is how we check if a piece is local.
- licenses: links a piece id with a license type. Licenses are actually text
            files stored in the app, we just store what file name/type to use.
- secrets: we need to look at this. Links each piece ID with its unique secret
            for accessing it on the API.

Beyond adding and getting basic information, there are some more complex
query methods. Explained below.

Any additions to this class should have relevant tests written before
working on the feature. Any new tables should really be discussed in
issues/other comms platforms before doing a big change. These can be
found in ExtractMetadata/tests/testDataLayer. Please either expand
those classes or if there's going to be a lot to group, put them
in a new test file.

"""

from . import TableManager
from .helpers import extendJoinQuery, do_online_offline_query, get_if_exists, \
    filter_dict
from ..hashdict import hashdict
from ..helpers import init_kv


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
        tempo_string = str(entry['beat']) + "="
        if entry['beat_2'] != '-1':
            tempo_string += str(entry['beat_2'])
        elif entry['minute'] != -1:
            tempo_string += str(entry['minute'])
        return tempo_string


class MusicData(TableManager.TableManager):

    def __init__(self, database):
        super(MusicData, self).__init__(database)

    def addInstruments(self, data):
        connection, cursor = self.connect()
        elements = []
        for item in data:
            octave = 0
            diatonic = 0
            chromatic = 0
            if "diatonic" in item:
                diatonic = item["diatonic"]
            if "chromatic" in item:
                chromatic = item["chromatic"]
            item_data = (item["name"], diatonic, chromatic)
            elements.append(item_data)
        cursor.executemany('INSERT INTO instruments VALUES(?,?,?)', elements)
        connection.commit()
        self.disconnect(connection)

    def getInstrumentNames(self):
        query = 'SELECT name FROM instruments'
        results = self.read_all(query)
        instruments = set([result['name'].lower() for result in results])
        return list(instruments)

    def get_elem_id(self, name, elem='composer'):
        query = 'SELECT ROWID FROM {}s WHERE name=?'.format(elem)
        elem_id = self.read_one(query, (name,))
        if elem_id is not None:
            elem_id = elem_id['rowid']
        return elem_id

    def link_creator_to_piece(self, name, piece_id, creator='composer'):
        s_query = 'SELECT ROWID FROM {}s WHERE name=?'.format(creator)
        w_query = 'INSERT INTO {}s VALUES(?)'.format(creator)
        rowid = self.get_or_create_one(s_query, w_query, (name,))
        if rowid is not None:
            rowid = rowid['rowid']
            self.write('UPDATE pieces SET {}_id = ? WHERE ROWID = ?'.
                       format(creator),
                       (rowid, piece_id))

    def get_or_create_instrument(self, instrument):
        diatonic = get_if_exists(instrument, 'diatonic', default=0)
        chromatic = get_if_exists(instrument, 'chromatic', default=0)
        s_query = 'SELECT ROWID FROM instruments WHERE name=? ' \
                  'AND diatonic=? AND chromatic=?'
        w_query = 'INSERT INTO instruments VALUES(?,?,?)'
        name = instrument['name']
        rowid = self.get_or_create_one(s_query,
                                       w_query,
                                       (name, diatonic, chromatic))
        return rowid

    def getInstrumentId(self, name):
        data = self.read_one(
                            'SELECT ROWID FROM instruments '
                            'WHERE name=?',
                            (name,))
        if data is not None:
            data = data['rowid']
        return data

    def getInstrumentIdByNameAndTrans(self, instrument):
        diatonic = get_if_exists(instrument, 'diatonic', default=0)
        chromatic = get_if_exists(instrument, 'chromatic', default=0)
        query = 'SELECT ROWID FROM instruments WHERE name=? ' \
                'AND diatonic=? AND chromatic=?'
        return self.read_one(query, (instrument['name'], diatonic, chromatic))

    def get_or_create_instruments(self, instrument_list, piece_id):
        for item in instrument_list:
            rowid = self.get_or_create_instrument(item)
            if rowid is not None:
                self.write('INSERT INTO instruments_piece_join VALUES(?,?)',
                           (rowid['rowid'], piece_id))

    def create_key_links(self, keysig_dict, piece_id):
        for instrument in keysig_dict:
            for key in keysig_dict[instrument]:
                if type(key) is str:
                    query = 'SELECT ROWID FROM keys WHERE name = ?'
                    values = (key,)
                else:
                    query = 'SELECT ROWID FROM keys WHERE fifths=? AND mode=?'
                    fifths = get_if_exists(key, "fifths")
                    mode = get_if_exists(key, "mode")
                    values = (fifths, mode,)

                instrument_id = self.getInstrumentId(instrument)
                key = self.read_one(query, values)
                if key is not None:
                    query = 'INSERT INTO key_piece_join VALUES(?,?,?)'
                    self.write(query, (key['rowid'],
                               piece_id,
                               instrument_id))

    def create_clef_links(self, clef_dict, piece_id):
        for instrument in clef_dict:
            for clef in clef_dict[instrument]:
                sign = get_if_exists(clef, "sign", default="G")
                line = get_if_exists(clef, "line", default=2)
                instrument_id = self.getInstrumentId(instrument)
                clef_id = self.read_one(
                                        'SELECT ROWID FROM clefs '
                                        'WHERE sign=? AND line=?',
                                        (sign, line,))
                if clef_id is not None:
                    self.write(
                        'INSERT INTO clef_piece_join VALUES(?,?,?)',
                        (clef_id['rowid'],
                         piece_id,
                         instrument_id,
                         ))

    def get_or_create_tempo_or_timesig(self, data, elem='timesig'):
        queries = {"timesig": ('SELECT ROWID FROM timesigs WHERE '
                               'beat=? AND b_type=?',
                               'INSERT INTO timesigs VALUES(?,?)'),
                   "tempo": ('SELECT ROWID FROM tempos WHERE beat=? '
                             'AND minute=? AND beat_2=?',
                             'INSERT INTO tempos VALUES(?,?,?)')}
        return self.get_or_create_one(queries[elem][0], queries[elem][1], data)

    def create_timesig_links(self, timesig_list, piece_id):
        for meter in timesig_list:
            beat = meter["beat"]
            b_type = meter["type"]
            rowid = self.get_or_create_tempo_or_timesig((beat, b_type))
            if rowid is not None:
                self.write('INSERT INTO time_piece_join VALUES(?,?)',
                           (piece_id, rowid['rowid']))

    def create_tempo_links(self, tempo_list, piece_id):
        for tempo in tempo_list:
            beat = tempo["beat"]
            beat_2 = get_if_exists(tempo, "beat_2", -1)
            minute = get_if_exists(tempo, "minute", -1)
            rowid = self.get_or_create_tempo_or_timesig((beat, minute, beat_2),
                                                        elem='tempo')
            if rowid is not None:
                self.write('INSERT INTO tempo_piece_join '
                           'VALUES(?,?)',
                           (piece_id,
                            rowid['rowid']))

    def set_source(self, source, piece_id):
        query = 'INSERT INTO sources VALUES(?,?)'
        self.write(query, (piece_id, source,))

    def set_secret(self, secret, piece_id):
        query = 'INSERT INTO secrets VALUES(?,?)'
        self.write(query, (piece_id, secret,))

    def setLicense(self, license, piece_id):
        query = 'INSERT INTO licenses VALUES(?,?)'
        self.write(query, (piece_id, license,))

    def addPiece(self, filename, data):
        '''
        method which takes in stuff about a piece and adds it
         to the relevant tables
        :param filename: filename the piece is talking about
        :param data: dictionary containing information -
        ids can be "composer", "title", "key"
        (which contains a dict of mode and fifths attached to instruments),
        "clef" (same as keys), "tempo", "instruments"
        :return: None
        '''
        composer_id = -1
        lyricist_id = -1
        title = ""
        method_table = {"key": self.create_key_links,
                        "clef": self.create_clef_links,
                        "time": self.create_timesig_links,
                        "tempo": self.create_tempo_links,
                        "source": self.set_source,
                        "secret": self.set_secret,
                        "license": self.setLicense}

        if "title" in data:
            title = data["title"]
            data.pop("title")

        query_input = (filename, title, composer_id, lyricist_id, False)
        self.write('INSERT INTO pieces VALUES(?,?,?,?,?)', query_input)
        select_input = (filename,)
        rowid = self.read_one('SELECT ROWID FROM pieces WHERE filename=?',
                              select_input)
        piece_id = rowid["rowid"]

        if "instruments" in data:
            self.get_or_create_instruments(data["instruments"], piece_id)
            data.pop("instruments")

        if "id" in data:
            data.pop("id")

        table_info = {}
        for key in data:
            if key in ['lyricist', 'composer']:
                self.link_creator_to_piece(data[key], piece_id, creator=key)
            else:
                table_info[key] = method_table[key](data[key], piece_id)

    def getFileList(self, online=False):
        connection, cursor = self.connect()
        query = 'SELECT filename FROM pieces p WHERE p.archived=0'
        query = do_online_offline_query(query, 'p.ROWID', online=online)
        cursor.execute(query)
        results = cursor.fetchall()
        self.disconnect(connection)
        filelist = set([result['filename'] for result in results])
        return list(filelist)

    def getRoughPiece(self, filename, archived=0, online=False):
        """
        method to get a piece's table entry according to it's filename.
        This is used in cases where the user has started to type a filename
        but may not have entered the whole filename yet.

        Returns all results found for this string.
        """

        connection, cursor = self.connect()
        thing = (filename, "%" + filename + "%", archived,)
        query = 'SELECT ROWID, filename, title, composer_id, ' \
                'lyricist_id FROM pieces p WHERE (p.filename=?' \
                ' OR p.filename LIKE ?) AND p.archived=?'
        query = do_online_offline_query(query, 'p.ROWID', online=online)
        cursor.execute(query, thing)

        result = cursor.fetchall()
        self.disconnect(connection)
        return [r['filename'] for r in result]

    def getExactPiece(self, filename, archived=0, online=False):
        """
        Method to get piece by exactly the string entered with no wildcards.
        This is used in cases where user has entered "*.xml" or filename:<this>
        or for getting a file having found its filename elsewhere.

        Returns 1 metadata collection assuming file names are unique.
        """
        connection, cursor = self.connect()
        thing = (filename, archived,)
        query = 'SELECT ROWID, filename, title, composer_id, lyricist_id ' \
                'FROM pieces p WHERE (p.filename=?) AND p.archived=?'
        query = do_online_offline_query(query, 'p.ROWID', online=online)
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
        result = cursor.fetchone()
        if result is not None:
            return result['rowid']

    def getTempoId(self, beat, minute, beat_2):
        """
        fetch a tempo ID by its beats.
        """
        result = self.read_one(
            'SELECT ROWID FROM tempos WHERE beat=? AND minute=? AND beat_2=? ',
            (beat,
             minute,
             beat_2))
        if result is not None:
            return result['rowid']

    def getInstrumentIdWhereTextInName(self, instrument):
        """
        similar to get rough piece. Try and figure out an instrument ID by
        a partial instrument name

        Returns a list of all IDs matching the string
        """
        result = self.read_all('SELECT ROWID FROM instruments '
                               'WHERE name=? OR name LIKE ?',
                               (instrument, "%{}%".format(instrument)))
        instrument_ids = [id['rowid'] for id in result]
        return instrument_ids

    def get_creator_id_where_text_in_name(self, name, creator_type='composer'):
        """
        method which takes in composer name and outputs its database id
        :param composer: name of composer
        :param cursor: database cursor object
        :return: int pertaining to row id of composer in database
        """
        query = 'SELECT ROWID FROM {}s WHERE name=? OR name LIKE ? ' \
                'OR name LIKE ? OR name LIKE ?'.format(creator_type)
        input_vars = (name, "%{}%".format(name), "%{}".format(name),
                      "{}%".format(name))
        results = self.read_all(query, input_vars)
        composer_ids = [res['rowid'] for res in results]
        return composer_ids

    def get_creator_name(self, creator_id, creator_type='composer'):
        query = 'SELECT name FROM {}s WHERE ROWID = ?'.format(creator_type)
        result = self.read_one(query, (creator_id,))
        if result is not None:
            return result['name']

    # methods used in querying by user
    def getPiecesByInstruments(self, instruments, archived=0, online=False):
        """
        method to get all the pieces containing a certain instrument
        :param instrument: name of instrument
        :return: list of files containing that instrumnet
        """
        instrument_ids = [
            self.getInstrumentIdWhereTextInName(
                instrument) for instrument in instruments]
        tuple_ids = []
        [tuple_ids.extend(inst_id) for inst_id in instrument_ids]
        file_list = []
        query = 'SELECT i.piece_id FROM instruments_piece_join i WHERE EXISTS '

        for i in range(len(instrument_ids)):
            query += '(SELECT * FROM instruments_piece_join ' \
                     'WHERE piece_id = i.piece_id'
            # for every new instrument update the query
            query += extendJoinQuery(len(instrument_ids[i]),
                                     'instrument_id = ?',
                                     ' OR ',
                                     init_string=' AND (')
            query += ')'
            if i != len(instrument_ids) - 1:
                query += ' AND EXISTS '
        query = do_online_offline_query(query, 'i.piece_id', online=online)
        query += ";"

        input = tuple(tuple_ids)
        results = self.read_all(query, input)

        file_list = self.getPiecesByRowId(results)
        return file_list

    def get_pieces_by_any_all_instruments(self,
                                          instruments,
                                          archived=0,
                                          online=False):
        """
        Runs 2 queries:
        1. Fetch a piece that contains all of the instruments
        listed in instruments.
        2. Iterate through the list asking for the individual
        pieces containing that instrument,
        but possibly not all of them.

        Returns a dictionary containing "Instrument: "<each instrument>
        as keys to which each value is a list of the pieces containing
        that instrument, and, if there are any, a key "All Instruments"
         which is matched to a list of all pieces containing every instrument
        requested.
        """
        all_pieces = self.getPiecesByInstruments(instruments,
                                                 archived=archived,
                                                 online=online)
        any = {"Instrument: "+instrument:
               self.getPiecesByInstruments([instrument],
                                           archived=archived,
                                           online=online)
               for instrument in instruments}
        result = {}
        if len(all_pieces) > 0:
            result['All Instruments'] = all_pieces
        result.update({key: any[key] for key in any if len(any[key]) > 0})
        return result



    def getPiecesByRowId(self, rows, archived=0):
        """
        method which takes in a list of rows which are ROWIDs in the piece table and returns a list of files
        :param rows: list of tuples pertaining to ROWIDs in pieces table
        :return: list of strings pertaining to xml files
        """
        file_list = []
        previous = None
        for element in rows:
            if element != previous:
                result = self.read_one('SELECT filename FROM pieces WHERE ROWID=? AND archived=?',
                                       (element['piece_id'], archived))
                if result is not None:
                    file_list.append(result['filename'])
            previous = element
        return file_list

    def get_pieces_by_creator(self, creator, archived=0, online=False, creator_type='composer'):
        creator_ids = self.get_creator_id_where_text_in_name(creator, creator_type)
        file_list = []
        if len(creator_ids) > 0:
            query = 'SELECT filename FROM pieces p WHERE p.archived=? AND '
            query += extendJoinQuery(len(creator_ids), 'p.{}_id LIKE ?'.format(creator_type), ' OR ', init_string='(')
            query = do_online_offline_query(query, 'p.ROWID', online=online)
            input_list = [archived]
            input_list.extend(creator_ids)
            input = tuple(input_list)
            results = self.read_all(query, input)
            file_list = [r['filename'] for r in results]
        return file_list

    def getPieceByTitle(self, title, *args, archived=0, online=False, creator_type=None):
        """
        method which takes in title of piece and outputs list of files named that
        :param title: title of piece
        :return: list of tuples
        """
        connection, cursor = self.connect()
        thing = (title, "%" + title + "%", title + "%", "%" + title, archived,)
        query = 'SELECT * FROM pieces p WHERE (p.title=? OR p.title LIKE ?' \
                ' OR p.title LIKE ? OR p.title LIKE ?) AND p.archived=?'
        query = do_online_offline_query(query, 'p.ROWID', online=online)
        cursor.execute(query, thing)
        result = cursor.fetchall()
        result = [r['filename'] for r in result]
        self.disconnect(connection)
        return result

    def get_piece_by_join(self, data, query_type, p_id='i.piece_id', archived=0, online=False):
        options = {"key": {"init_query":'SELECT i.piece_id FROM key_piece_join i WHERE EXISTS ' \
                '(SELECT * FROM key_piece_join WHERE piece_id = i.piece_id AND key_id = ?)',
                           "extender": ' AND EXISTS (SELECT * FROM key_piece_join WHERE piece_id = i.piece_id AND key_id = ?)'
                        , "p_id": 'i.piece_id',
                           "method":self.get_elem_id},
                   "clef": {"init_query": 'SELECT i.piece_id FROM clef_piece_join i WHERE EXISTS (SELECT * FROM clef_piece_join WHERE piece_id = i.piece_id AND clef_id = ?)',
                            "extender": ' AND EXISTS (SELECT * FROM clef_piece_join WHERE piece_id = i.piece_id AND clef_id = ?)',
                            "p_id": "i.piece_id",
                            "method":self.get_elem_id}}
        connection, cursor = self.connect()
        data = [options[query_type]["method"](elem, query_type) for elem in data]
        query = options[query_type]["init_query"]
        for i in range(1, len(data)):
            query += options[query_type]["extender"]
        query = do_online_offline_query(query, options[query_type]["p_id"], online=online)
        query += ";"
        input = tuple(data)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results)
        self.disconnect(connection)
        return file_list

    def getPiecesByModularity(self, modularity, archived=0, online=False):
        """

        :param modularity:
        :param archived:
        :param online:
        :return:
        """
        query = 'SELECT key_piece.piece_id FROM keys k, key_piece_join ' \
                'key_piece WHERE k.mode = ? AND key_piece.key_id = k.ROWID'

        query = do_online_offline_query(query, 'key_piece.piece_id', online=online)
        key_set = self.read_all(query, (modularity,))
        file_list = self.getPiecesByRowId(key_set)
        return file_list

    # playlist queries
    def get_piece_by_all_elem(self, archived=0, online=False, elem='key'):
        query_table = {
            'keys': '''SELECT k.name, piece.filename FROM keys k, pieces piece, key_piece_join key_piece, instruments i
                    WHERE key_piece.key_id = k.ROWID AND i.ROWID = key_piece.instrument_id
                    AND i.diatonic = 0 AND i.chromatic = 0 AND piece.ROWID = key_piece.piece_id
                    AND piece.archived = ? AND EXISTS (SELECT NULL FROM key_piece_join WHERE key_id = k.ROWID AND piece_id != key_piece.piece_id)
        ''',
            'clefs': '''SELECT clef.name, piece.filename FROM clefs clef, pieces piece, clef_piece_join clef_piece
                    WHERE clef_piece.clef_id = clef.ROWID AND piece.ROWID = clef_piece.piece_id
                    AND piece.archived = ? AND EXISTS (SELECT NULL FROM clef_piece_join WHERE clef_id = clef_piece.clef_id AND piece_id != clef_piece.piece_id)
        ''',
            'composers': '''SELECT comp.name, piece.filename FROM composers comp, pieces piece
                    WHERE piece.composer_id = comp.ROWID
                    AND EXISTS (SELECT * FROM pieces WHERE composer_id = comp.ROWID AND ROWID != piece.ROWID)
                    AND piece.archived = ?
        ''',
            'lyricists': '''SELECT lyric.name, piece.filename FROM lyricists lyric, pieces piece
                    WHERE lyric.ROWID = piece.lyricist_id
                    AND EXISTS (SELECT * FROM pieces WHERE lyricist_id = piece.lyricist_id AND ROWID != piece.ROWID)
                    AND piece.archived = ?
        '''
        }
        query = do_online_offline_query(query_table[elem], 'piece.ROWID', online=online)
        return self.get_by_all_elems(query, (archived,))

    def getPiecesByAllTimeSigs(self, archived=0, online=False):
        query = '''SELECT time_sig.beat, time_sig.b_type, piece.filename FROM timesigs time_sig, pieces piece, time_piece_join time_piece
                    WHERE time_piece.time_id = time_sig.ROWID AND piece.ROWID = time_piece.piece_id
                    AND piece.archived = ? AND EXISTS(SELECT null FROM time_piece_join WHERE time_id=time_sig.ROWID AND time_piece_join.piece_id != time_piece.piece_id)
        '''
        query = do_online_offline_query(query, 'piece.ROWID', online=online)
        results = self.read_all(query, (archived,))
        sig_dict = {}
        for pair in results:
            sig_input = "{}/{}".format(pair['beat'], pair['b_type'])
            if sig_input not in sig_dict:
                sig_dict[sig_input] = []
            sig_dict[sig_input].append(pair['filename'])
        return sig_dict

    def getPiecesByAllTempos(self, archived=0, online=False):
        query = '''SELECT tempo.beat, tempo.beat_2, tempo.minute, piece.filename
                  FROM tempos tempo, pieces piece, tempo_piece_join tempo_piece
                    WHERE tempo_piece.tempo_id = tempo.ROWID AND piece.ROWID = tempo_piece.piece_id
                    AND EXISTS (SELECT * FROM tempo_piece_join WHERE tempo_id = tempo_piece.tempo_id AND piece_id != tempo_piece.piece_id)
                    AND piece.archived = ?
        '''
        query = do_online_offline_query(query, 'piece.ROWID', online=online)
        results = self.read_all(query, (archived,))
        tempo_dict = {}
        for pair in results:
            parser = TempoParser()
            key_input = parser.encode(pair)
            if key_input not in tempo_dict:
                tempo_dict[key_input] = []
            tempo_dict[key_input].append(pair['filename'])
        return tempo_dict

    def getPiecesByAllInstruments(self, archived=0, online=False):
        connection, cursor = self.connect()
        query = '''SELECT instrument.name, instrument.diatonic, instrument.chromatic, piece.filename
                  FROM instruments instrument, pieces piece, instruments_piece_join instrument_piece
                    WHERE instrument_piece.instrument_id = instrument.ROWID AND piece.ROWID = instrument_piece.piece_id
                    AND EXISTS (SELECT * FROM instruments_piece_join WHERE instrument_id = instrument_piece.instrument_id AND piece_id != instrument_piece.piece_id)
                    AND piece.archived = ?
        '''
        query = do_online_offline_query(query, 'piece.ROWID', online=online)
        cursor.execute(query, (archived,))
        results = cursor.fetchall()
        self.disconnect(connection)
        instrument_dict = {}


        for pair in results:
            if pair['diatonic'] != 0 or pair['chromatic'] != 0:
                key_val = "{} transposed {} diatonic {} chromatic".format(pair['name'], pair['diatonic'],
                                                                   pair['chromatic'])
            else:
                key_val = pair['name']
            if key_val not in instrument_dict:
                instrument_dict[key_val] = []
            instrument_dict[key_val].append(pair['filename'])
        return instrument_dict

    def createInstrumentDictionaryAndList(self, instruments, action, elem_type='clef'):
        inst_list = []
        inst_dict = {}
        for instrument in instruments:
            inst_list.append(self.getInstrumentId(instrument))
            inst_dict[instrument] = []
            for key in instruments[instrument]:
                id = action(key, elem_type)
                if id is not None:
                    inst_list.append(id)
                    inst_dict[instrument].append(id)
        return inst_list, inst_dict

    def getPieceByInstrumentInKeys(self, data, archived=0, online=False):
        connection, cursor = self.connect()
        file_list = []
        tuple_data = list(data.keys())
        search_ids, key_ids = self.createInstrumentDictionaryAndList(data, self.get_elem_id, elem_type='key')
        if len(tuple_data) > 0 and len(key_ids) > 0:
            query = 'SELECT key_piece.piece_id FROM key_piece_join key_piece WHERE EXISTS '
            for i in range(len(data)):
                query += '(SELECT * FROM key_piece_join WHERE piece_id = key_piece.piece_id AND instrument_id = ?'
                query += extendJoinQuery(len(key_ids[tuple_data[i]]), 'key_id = ?', ' AND ', init_string=' AND ')
                if i != len(data) - 1:
                    query += ' AND EXISTS '
            query = do_online_offline_query(query, 'key_piece.piece_id', online)

            cursor.execute(query, tuple(search_ids))
            results = cursor.fetchall()

            file_list = self.getPiecesByRowId(results, archived)
        return file_list

    def getPieceByInstrumentInClefs(self, data, archived=0, online=False):
        connection, cursor = self.connect()
        tuple_data = list(data.keys())
        file_list = []
        search_ids, clef_ids = self.createInstrumentDictionaryAndList(data, self.get_elem_id, elem_type='clef')

        if len(tuple_data) > 0 and len(clef_ids) > 0:
            query = 'SELECT clef_piece.piece_id FROM clef_piece_join clef_piece WHERE EXISTS '
            for i in range(len(tuple_data)):
                query += '(SELECT * FROM clef_piece_join WHERE piece_id = clef_piece.piece_id AND instrument_id = ?'
                query += extendJoinQuery(len(clef_ids[tuple_data[i]]), 'clef_id = ?', ' AND ', init_string=' AND ')
                if i != len(tuple_data) - 1:
                    query += ' AND EXISTS '
            query = do_online_offline_query(query, 'clef_piece.piece_id', online=online)
            cursor.execute(query, tuple(search_ids))
            results = cursor.fetchall()
            file_list = self.getPiecesByRowId(results, archived)
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
        query = do_online_offline_query(query, 'i.piece_id', online=online)

        for i in range(1, len(time_ids)):
            query += ' AND EXISTS (SELECT * FROM time_piece_join WHERE piece_id = i.piece_id AND time_id = ?)'

        query += ";"
        input = tuple(time_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, archived)
        self.disconnect(connection)
        return file_list



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
                tempo[2]) for tempo in tempo_list]
        query = 'SELECT i.piece_id FROM tempo_piece_join i WHERE EXISTS (SELECT * FROM tempo_piece_join WHERE piece_id = i.piece_id AND tempo_id = ?)'
        for i in range(1, len(tempo_ids)):
            query += ' AND EXISTS (SELECT * FROM tempo_piece_join WHERE piece_id = i.piece_id AND tempo_id = ?)'
        query = do_online_offline_query(query, 'i.piece_id', online=online)
        query += ";"
        input = tuple(tempo_ids)
        cursor.execute(query, input)
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results)
        self.disconnect(connection)
        return file_list

    def getInstrumentsByPieceId(self, piece_id, cursor):
        instrument_query = '''SELECT name, diatonic, chromatic FROM instruments AS i JOIN instruments_piece_join
                              AS ins ON ins.instrument_id = i.rowid WHERE ins.piece_id = ?'''
        cursor.execute(instrument_query, (piece_id,))
        data = set(cursor.fetchall())
        return data

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

    def getPieceByAlternateInstruments(self, cursor, alternates, archived=0, online=False):
        query = '''SELECT piece_id FROM instruments_piece_join i WHERE EXISTS'''
        query_input = []
        for instrument in alternates:
            query_input.append(instrument[0][1])
            query += ''' (SELECT * FROM instruments_piece_join WHERE piece_id = i.piece_id AND instrument_id = ?'''
            for value in instrument[1]:
                query_input.append(value['rowid'])
                query += ''' OR instrument_id =?'''
            query += ''')'''
            if instrument != alternates[-1]:
                query += " AND EXISTS"

        query = do_online_offline_query(query, 'i.piece_id', online=online)
        query += ";"
        cursor.execute(query, tuple(query_input))
        results = cursor.fetchall()
        file_list = self.getPiecesByRowId(results, archived=archived)
        return file_list

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
        file_list = []
        instrument_keys = []
        alternates = []
        for elem in instruments:
            key = self.getInstrumentId(elem["name"])
            if key is not -1:
                instrument_keys.append((elem, key))
                alternates.append(((elem, key), self.getInstrumentsBySameTranspositionAs(elem['name'])))
        results = self.getPiecesByInstruments(
            [instrument["name"] for instrument in instruments])
        if len(results) == 0:
            file_list = self.getPieceByAlternateInstruments(cursor, alternates, archived, online)

        self.disconnect(connection)
        return file_list

    # again, helper methods for other methods which just go off and find the
    # joins for specific pieces
    def get_clefs_or_keys_by_piece_id(self, piece_id, elem='key'):
        table = {"key": ('SELECT key_id, instrument_id FROM key_piece_join WHERE piece_id=?',
                        'SELECT keys.name, instruments.name as instrument FROM keys, ' \
                'instruments WHERE keys.ROWID=? AND instruments.ROWID=?'),
                 "clef": ('SELECT clef_id, instrument_id FROM clef_piece_join WHERE piece_id=?',
                            'SELECT clefs.name, instruments.name as instrument FROM clefs, ' \
                'instruments WHERE clefs.ROWID=? AND instruments.ROWID=?')}
        elem_ids = set(self.read_all(table[elem][0], (piece_id,)))
        data = {}
        for id in elem_ids:
            name = self.read_one(table[elem][1], (id['{}_id'.format(elem)], id['instrument_id']))
            if name is not None:
                init_kv(data, name['instrument'], init_value=[])
                data[name['instrument']].append(name['name'])
        return data

    def getTimeSigsByPieceId(self, piece_id, cursor):
        time_query = 'SELECT time_id FROM time_piece_join WHERE piece_id=?'
        cursor.execute(time_query, (piece_id,))
        time_ids = set(cursor.fetchall())
        meters = []
        for id in time_ids:
            q = 'SELECT * FROM timesigs WHERE ROWID=?'
            cursor.execute(q, (id['time_id'],))
            timesig = cursor.fetchone()
            if timesig is not None and len(timesig) > 0:
                meters.append(str(timesig['beat']) + "/" + str(timesig['b_type']))
        return meters

    def getTemposByPieceId(self, piece_id, cursor):
        tempo_query = 'SELECT tempo_id FROM tempo_piece_join WHERE piece_id=?'
        cursor.execute(tempo_query, (piece_id,))
        tempo_ids = set(cursor.fetchall())
        tempos = []
        for id in tempo_ids:
            q = 'SELECT * FROM tempos WHERE ROWID=?'
            cursor.execute(q, (id['tempo_id'],))
            tempo = cursor.fetchone()
            parser = TempoParser()
            if tempo is not None and len(tempo) > 0:
                tempos.append(parser.encode(tempo))
        return tempos

    def getFileData(self, filenames, archived=0, online=False):
        file_data = []
        for filename in filenames:
            piece_tuple = self.getExactPiece(filename, archived, online=online)
            if piece_tuple is not None:
                file_data.append(piece_tuple)
        return file_data

    def getAllPieceInfo(self, filenames, archived=0, online=False):
        file_data = self.getFileData(filenames, archived=archived, online=online)
        files = []
        connection, cursor = self.connect()

        for file in file_data:
            lyricist = ''
            composer = ''
            index = file["rowid"]
            composer_id = file["composer_id"]
            if composer_id != -1:
                composer = self.get_creator_name(composer_id)

            lyricist_id = file["lyricist_id"]
            if lyricist_id != -1:
                lyricist = self.get_creator_name(lyricist_id, creator_type='lyricist')
            elem_data = hashdict({"instruments": self.getInstrumentsByPieceId(index, cursor),
            "clefs" : self.get_clefs_or_keys_by_piece_id(index, elem='clef'),
            "keys": self.get_clefs_or_keys_by_piece_id(index),
            "timesigs": self.getTimeSigsByPieceId(index, cursor),
            "tempos": self.getTemposByPieceId(index, cursor),
            "filename": file["filename"], "title": file["title"],
            'composer': composer, 'lyricist': lyricist})
            files.append(filter_dict(elem_data))

        self.disconnect(connection)
        return files

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
                (val['rowid'],
                 file_id['rowid']))
        connection.commit()
        self.disconnect(connection)

    def getAllUserPlaylists(self):
        query = '''SELECT piece.filename, play.name, play.ROWID FROM playlists play, playlist_join playjoin, pieces piece
                          WHERE playjoin.playlist_id = play.ROWID and piece.ROWID = playjoin.piece_id'''
        data = self.get_by_all_elems(query, ())
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
            cursor.execute(query_2, (results[i]['name'],))
            files = cursor.fetchall()
            if results[i]['name'] not in data:
                data[results[i]['name']] = [file['filename'] for file in files]
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
        cursor.execute(join_query, (res['rowid'],))
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
            cursor.execute(instrument_query, (result['rowid'],))
            tempo_query = '''DELETE FROM tempo_piece_join WHERE piece_id =?'''
            cursor.execute(tempo_query, (result['rowid'],))
            key_query = '''DELETE FROM key_piece_join WHERE piece_id =?'''
            cursor.execute(key_query, (result['rowid'],))
            clef_query = '''DELETE FROM clef_piece_join WHERE piece_id =?'''
            cursor.execute(clef_query, (result['rowid'],))
            time_query = '''DELETE FROM time_piece_join WHERE piece_id =?'''
            cursor.execute(time_query, (result['rowid'],))
            piece_query = '''DELETE FROM pieces WHERE ROWID=?'''
            cursor.execute(piece_query, (result['rowid'],))
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
        file_list = [result['filename'] for result in results]
        self.disconnect(connection)
        return file_list

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
        cursor.execute(query, (result['rowid'],))
        connection.commit()
        self.disconnect(connection)



