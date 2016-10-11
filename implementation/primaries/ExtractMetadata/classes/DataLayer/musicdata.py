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

from . import querylayer
from .helpers import extendJoinQuery, do_online_offline_query, get_if_exists, \
    filter_dict
from ..hashdict import hashdict
import copy
from .exceptions import BadPieceException, InvalidQueryException
from .parsers import TempoParser, MeterParser, InstrumentParser


class MusicData(querylayer.QueryLayer):
    parsers = {"tempos": TempoParser(),
               "time_signatures": MeterParser(),
               "instruments": InstrumentParser()}

    def __init__(self, database):
        super(MusicData, self).__init__(database)
        self.setup()
        self.add_fixtures()

    def get_instrument_names(self):
        results = self.get_all(table="instruments")
        instruments = set([result['name'].lower() for result in results])
        return list(instruments)

    def link_creator_to_piece(self, name, piece_id, creator='composer'):
        row = self.get_or_add({"name": name}, table="creators")[0]

        if row is not None:
            self.update(piece_id,
                        {"{}.id".format(creator): row['id']},
                        table="pieces")

    def archive(self, filenames):
        for filename in filenames:
            id = self.get_ids_for_like({"filename": filename})[0]
            self.update(id, {"archived": True}, table="pieces")

    def delete(self, filenames):
        for filename in filenames:
            id = self.get_ids_for_like({"filename": filename})[0]
            self.remove(id, table="pieces")

    def add_piece(self, filename, data):
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
        source = "local"
        secret = None

        if "title" in data:
            title = data["title"]
            data.pop("title")

        if "source" in data:
            source = data["source"]
            data.pop("source")

        if "secret" in data:
            secret = data["secret"]
            data.pop("secret")

        query_input = {"filename": filename,
                       "name": title,
                       "composer.id": composer_id,
                       "lyricist.id": lyricist_id,
                       "archived": False,
                       "source": source,
                       "secret": secret}

        piece_id = self.add(query_input)[0]

        if "instruments" in data:
            data = self.add_instruments_to_piece(data, piece_id)

        else:
            raise BadPieceException(
                "All pieces must have at least one instrument")

        if "id" in data:
            data.pop("id")

        for key in data:
            if key in ['lyricist', 'composer']:
                self.link_creator_to_piece(data[key], piece_id, creator=key)
            else:
                for value in data[key]:
                    self.add_and_link(value, piece_id, table=key)

    def add_instruments_to_piece(self, data, piece_id):
        result_data = copy.deepcopy(data)
        for instrument in result_data["instruments"]:
            name = instrument['name']
            kwargs = {}
            if "clefs" in data:
                if name in data["clefs"]:
                    clef_data = result_data["clefs"][name]
                    kwargs['clefs'] = clef_data
                else:
                    raise BadPieceException(
                        "each instrument should have atleast one key")
            else:
                raise BadPieceException(
                    "each instrument should have atleast one clef")

            if "keys" in data:
                if name in data["keys"]:
                    key_data = result_data["keys"][name]
                    kwargs['keys'] = key_data

                else:
                    raise BadPieceException(
                        "each instrument should have atleast one key")

            else:
                raise BadPieceException(
                    "each instrument should have atleast one key")

            self.add_instrument_to_piece(instrument, piece_id, **kwargs)
        result_data["clefs"] = {}
        result_data["keys"] = {}
        result_data.pop("instruments")
        return result_data

    def add_instrument_to_piece(self, data, piece_id, clefs={}, keys={}):
        ins = self.get_or_add(data, table='instruments')[0]
        for clef_data in clefs:
            clef = self.get_or_add(clef_data, table='clefs')[0]
            self.add({'instruments.id': ins['id'], 'clefs.id': clef[
                     'id'], 'piece.id': piece_id}, table='clefs_ins_piece')

        for key_data in keys:
            key = self.get_or_add(key_data, table='keys')[0]
            self.add({'instruments.id': ins['id'], 'keys.id': key[
                     'id'], 'piece.id': piece_id}, table='keys_ins_piece')

    def query_pieces_archived_online(
            self,
            online=False,
            archived=False,
            data=None):
        source = {'source': 'local'}
        not_data = {}
        if data is None:
            data = {}
        if online:
            not_data = source
        else:
            data.update(source)
        data['archived'] = archived
        results = self.query(data, not_data, table="pieces")
        return results

    def get_file_list(self, online=False, archived=False):
        results = self.query_pieces_archived_online(
            online=online, archived=archived)
        filelist = set([result['filename'] for result in results])
        return list(filelist)

    # methods used in querying by user
    def get_pieces_by_instruments(
            self,
            instruments,
            archived=False,
            online=False):
        """
        method to get all the pieces containing a certain instrument
        :param instrument: name of instrument
        :return: list of files containing that instrumnet
        """
        instrument_ids = [self.get_ids_for_like({"name": "%{}%".format(
            instrument)}, table="instruments") for instrument in instruments]
        res = list(filter(None, instrument_ids))
        if len(res) != len(instrument_ids):
            return []

        tuple_ids = []
        [tuple_ids.extend(inst_id) for inst_id in instrument_ids]
        query = []

        for i in range(len(instrument_ids)):
            data = {"instruments.id": instrument_ids[i]}
            query.append(data)
        results = self.query_multiple(query)
        file_list = self.get_pieces_by_row_id(
            results, archived=archived, online=online)
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
        all_pieces = self.get_pieces_by_instruments(instruments,
                                                    archived=archived,
                                                    online=online)
        any = {"Instrument: " + instrument:
               self.get_pieces_by_instruments([instrument],
                                              archived=archived,
                                              online=online)
               for instrument in instruments}
        result = {}
        if len(all_pieces) > 0:
            result['All Instruments'] = all_pieces
        result.update({key: any[key] for key in any if len(any[key]) > 0})
        return result

    def get_pieces_by_row_id(self, rows, archived=False, online=False):
        """
        method which takes in a list of rows which are ROWIDs in the
        piece table and returns a list of files
        :param rows: list of tuples pertaining to ROWIDs in pieces table
        :return: list of strings pertaining to xml files
        """
        file_list = []
        previous = None
        for element in rows:
            if element != previous:
                result = querylayer.col_or_none(
                    self.query_pieces_archived_online(
                        data={
                            'id': element},
                        online=online,
                        archived=archived),
                    'filename')
                if result is not None:
                    file_list.append(result)
            previous = element
        return file_list

    def get_pieces_by_creator(
            self,
            creator,
            creator_type='composer',
            archived=False,
            online=False):
        file_list = []
        creator_id = self.query(
            likedata={
                "name": "%{}%".format(creator)},
            table="creators")
        if len(creator_id) > 0:
            creator_id = creator_id[0]
            piece_ids = self.query(
                {creator_type + ".id": creator_id['id']}, table="pieces")
            piece_ids = [elem['id'] for elem in piece_ids]
            file_list = self.get_pieces_by_row_id(
                piece_ids, archived=archived, online=online)
        return file_list

    def getPieceByTitle(self, title, *args,
                        archived=False, online=False, creator_type=None):
        """
        method which takes in title of piece and outputs list of
        files named that
        :param title: title of piece
        :return: list of tuples
        """
        notdata = {}
        data = {}
        if online:
            notdata['source'] = 'local'
        else:
            data['source'] = 'local'
        data['archived'] = archived
        pieces = self.query(notdata=notdata,
                            data=data,
                            likedata={"name": "%{}%".format(title)},
                            table='pieces')
        files = [piece['filename'] for piece in pieces]
        return files

    def get_piece_by_join(self, data, table, archived=False, online=False):
        results = []
        for value in data:
            key = self.query(value, table=table)[0]
            piece_ids = self.query(
                {table + '.id': key['id']}, table=table + "_ins_piece")
            piece_ids = [elem['piece.id'] for elem in piece_ids]
            results.extend(piece_ids)
        results = set(results)
        file_list = self.get_pieces_by_row_id(
            results, archived=archived, online=online)
        return file_list

    def getPiecesByModularity(self, modularity, archived=False, online=False):
        """

        :param modularity:
        :param archived:
        :param online:
        :return:
        """
        keys = self.query({"mode": modularity}, table="keys")
        pieces = []
        for key in keys:
            piece_ids = self.query(
                {"keys.id": key['id']}, table="keys_ins_piece")
            piece_ids = [elem['piece.id'] for elem in piece_ids]
            pieces.extend(piece_ids)
        pieces = set(pieces)
        file_list = self.get_pieces_by_row_id(
            pieces, archived=archived, online=online)
        return file_list

    def getPieceByInstrumentIn_(
            self,
            data,
            table="clefs",
            archived=False,
            online=False):
        query = []
        for instrument in data:
            ins_id = self.query({"name": instrument}, table="instruments")
            ins_id = [elem['id'] for elem in ins_id]
            for e in data[instrument]:
                elem_id = self.query(e, table=table)
                if len(elem_id) > 0:
                    elem_id = [elem_id[0]['id']]
                else:
                    raise InvalidQueryException(
                        "{} query invalid, no results found".format(table))
                new_q = {
                    "instruments.id": ins_id,
                    "{}.id".format(table): elem_id}
                query.append(new_q)

        results = self.query_multiple(
            query, table="{}_ins_piece".format(table))
        file_list = self.get_pieces_by_row_id(
            results, archived=archived, online=online)
        return file_list

    def getPieceByMeter(self, meters, archived=False, online=False):
        results = set()
        for meter in meters:
            if "/" in meter:
                values = meter.split("/")
                beat = int(values[0])
                b_type = int(values[1])
                result = self.query(
                    {"beat": beat, "beat_type": b_type}, table="time_signatures")[0]['id']
                # TODO bounds check
                join = self.query({"time_signatures.id": result},
                                  table="time_signatures_piece")
                data = {elem['piece.id'] for elem in join}
                if len(results) > 0:
                    results = set.intersection(results, data)
                else:
                    results = set(data)
        file_list = self.get_pieces_by_row_id(
            results, archived=archived, online=online)
        return file_list

    def get_piece_by_tempo(self, tempos, archived=False, online=False):
        pieces = []
        tempo_list = []
        parser = TempoParser()
        for tempo in tempos:
            result = parser.decode(tempo)
            tempo_list.append(result)
        tempo_ids = [self.query(tempo, table="tempos")[0]
                     for tempo in tempo_list]
        for elem in tempo_ids:
            res = self.query({'tempos.id': elem['id']}, table='tempos_piece')
            res = [elem['piece.id'] for elem in res]
            pieces.append(res)
        pieces = set(*pieces)
        pieces = set.intersection(pieces)
        file_list = self.get_pieces_by_row_id(
            pieces, archived=archived, online=online)
        return file_list

    def get_instruments_by_piece_id(self, piece_id):
        results = self.query({'piece.id': piece_id},
                             table=self.get_join("instruments"))
        instruments = []
        for elem in results:
            results = self.query(
                {"id": elem['instruments.id']}, table="instruments")[0]
            results.pop("id")
            hashed = hashdict(results)
            instruments.append(hashed)

        return instruments

    def getInstrumentsByTransposition(self, transposition, online=False):
        result = self.query(transposition, table="instruments")
        return result

    def getInstrumentsBySameTranspositionAs(self, instrument):
        result = self.query_similar_rows({"name": instrument},
                                         match_cols=["chromatic",
                                                     "diatonic"],
                                         excl_cols=["name", "id"],
                                         table="instruments")
        return result

    def getPieceByAlternateInstruments(
            self,
            alternates,
            archived=False,
            online=False):
        query = []
        for instrument in alternates:
            ids = [instrument[0][1]]
            ids.extend([elem['id'] for elem in instrument[1]])
            data = {"instruments.id": ids}
            query.append(data)

        results = self.query_multiple(query, table="clefs_ins_piece")
        file_list = self.get_pieces_by_row_id(
            results, archived=archived, online=online)
        return file_list

    def getPieceByInstrumentsOrSimilar(
            self,
            instruments,
            archived=False,
            online=False):
        """
        method which searches first for any pieces containing the exact instrument,
        then by the name in dict, then by the transposition of the name if it
        isn't in the instruments table.
        :param instruments: list of instruments to search by
        :return: list of files + their instruments
        """
        file_list = []
        instrument_keys = []
        alternates = []
        for elem in instruments:
            key = self.get_row_id({"name": elem["name"]}, table="instruments")
            if key is not -1:
                instrument_keys.append((elem, key))
                if key is not None:
                    alternates.append(
                        ((elem, key), self.getInstrumentsBySameTranspositionAs(
                            elem['name'])))
                else:
                    transpos = copy.deepcopy(elem)
                    transpos.pop("name")
                    alternates.append(((elem, key),
                                       self.getInstrumentsByTransposition(transpos)))
        results = self.get_pieces_by_instruments(
            [instrument["name"] for instrument in instruments])
        if len(results) == 0:
            file_list = self.getPieceByAlternateInstruments(
                alternates, archived, online)
        return file_list

    # again, helper methods for other methods which just go off and find the
    # joins for specific pieces
    def get_clefs_or_keys_by_piece_id(self, piece_id, elem='keys'):
        elem_ids = self.query({'piece.id': piece_id},
                              table=elem + "_ins_piece")
        data = {}
        for value in elem_ids:
            ins = self.query(
                {'id': value['instruments.id']}, table='instruments')[0]
            res = self.query({'id': value[elem + '.id']}, table=elem)[0]
            if ins is not None:
                data.setdefault(ins['name'], []).append(res['name'])
        return data

    def getFileData(self, filenames, archived=False, online=False):
        file_data = []
        for filename in filenames:
            piece_tuple = self.query_pieces_archived_online(
                archived=archived, online=online, data={"filename": filename})
            if len(piece_tuple) > 0:
                file_data.append(piece_tuple[0])
        return file_data

    def get_all_piece_info(self, filenames, archived=False, online=False):
        file_data = self.getFileData(
            filenames, archived=archived, online=online)
        files = []

        for file in file_data:
            lyricist = ''
            composer = ''
            index = file["id"]
            composer_id = file["composer.id"]
            if composer_id != -1:
                composer = self.query(
                    {'id': composer_id}, table='creators')
                composer = querylayer.col_or_none(composer, 'name')

            lyricist_id = file["lyricist.id"]
            if lyricist_id != -1:
                lyricist = self.query(
                    {'id': lyricist_id}, table='creators')
                lyricist = querylayer.col_or_none(lyricist, 'name')

            elem_data = hashdict(
                {
                    "instruments": self.get_instruments_by_piece_id(index),
                    "clefs": self.get_clefs_or_keys_by_piece_id(
                        index,
                        elem='clefs'),
                    "keys": self.get_clefs_or_keys_by_piece_id(index),
                    "timesigs": self.get_elem_by_piece_id(
                        index,
                        elem='time_signatures'),
                    "tempos": self.get_elem_by_piece_id(
                        index,
                        elem='tempos'),
                    "filename": file["filename"],
                    "title": file["name"],
                    'composer': composer,
                    'lyricist': lyricist})
            files.append(filter_dict(elem_data))

        return files

    def get_elem_by_piece_id(self, piece_id, elem='tempos'):
        join_query = self.query({'piece.id': piece_id}, table=elem + '_piece')
        results = []
        if elem in self.parsers:
            parser = self.parsers[elem]
        else:
            parser = None
        for vals in join_query:
            data = self.query(
                {'id': vals['{}.id'.format(elem)]}, table=elem)[0]
            result = parser.encode(data)
            results.append(result)
        return results

    def get_piece_by_all_(self, elem='keys', online=False, archived=False):
        table = self.get_join(elem)
        elems = self.to_dict(table, self.get_all(table=table))
        sorted = self.order_by(
            elems,
            store_val="piece.id",
            column="{}.id".format(elem))
        result = {}
        for key in sorted:
            query = self.query({"id": key}, table=elem)[0]
            if len(query) > 0:
                files = self.get_pieces_by_row_id(
                    sorted[key], online=online, archived=archived)
                if elem in self.parsers:
                    entry = self.parsers[elem].encode(query)
                else:
                    entry = query["name"]

                if len(files) > 0:
                    result[entry] = files

        return result

    def get_piece_by_all_creators(
            self,
            elem="composer",
            online=False,
            archived=False):
        elems = self.to_dict(
            "creators",
            self.get_all(
                table="creators"))
        result = {}
        for e in elems:
            data = {"{}.id".format(elem): e["id"]}
            data['archived'] = archived
            notdata = {}
            if online:
                notdata['source'] = 'local'
            else:
                data['source'] = 'local'
            query = self.query(data=data, notdata=notdata, table="pieces")
            if len(query) > 0:
                result[e["name"]] = [q["filename"] for q in query]
        return result

    def get_value_for_filename(self, filename, column):
        res = self.query(data={'filename': filename})
        return_val = None
        if len(res) > 0:
            res = res[0]
            if column in res:
                return_val = res[column]
        return return_val

    def update_piece(self, filename, data):
        piece_id = self.get_value_for_filename(filename, 'id')
        self.update(piece_id, data)

    def add_playlist(self, name, files):
        id = self.add({"name": name}, table='playlists')
        if len(id) > 0:
            id = id[0]
            for file in files:
                q = self.query({'filename': file})
                p_id = querylayer.col_or_none(q, 'id')
                if p_id is not None:
                    self.add({'piece.id': p_id, 'playlist.id': id},
                             table=self.get_join('playlists'))

    def get_all_user_playlists(self):
        playlists = self.get_all('playlists')
        data = {}
        for elem in playlists:
            file_join = self.query(
                {'playlist.id': elem['id']}, table=self.get_join('playlists'))
            file_join = [f['piece.id'] for f in file_join]
            filenames = self.get_pieces_by_row_id(file_join)
            if len(filenames) > 0:
                data[elem['name']] = filenames
        return data

    def get_user_playlists_by_filename(self, filename):
        data = self.query({'filename': filename})
        result = {}
        if len(data) > 0:
            data = data[0]
            playlists = self.query(
                {'piece.id': data['id']}, table=self.get_join('playlists'))
            for elem in playlists:
                play_data = self.query(
                    {'id': elem['playlist.id']}, table='playlists')
                if len(play_data) > 0:
                    play_data = play_data[0]
                    joins = self.query(
                        {'playlist.id': play_data['id']},
                        table=self.get_join('playlists'))
                    joins = [f['piece.id'] for f in joins]
                    filenames = self.get_pieces_by_row_id(joins)
                    if len(filenames) > 0:
                        result[play_data['name']] = filenames
        return result

    def delete_playlist(self, name):
        p_id = self.query({'name': name}, table='playlists')
        p_id = querylayer.col_or_none(p_id, 'id')
        if p_id is not None:
            self.remove(p_id, 'playlists')
            self.remove(p_id, self.get_join('playlists'), column='playlist.id')

    def get_playlist(self, name):
        elem = self.query({'name': name}, table='playlists')
        return elem
