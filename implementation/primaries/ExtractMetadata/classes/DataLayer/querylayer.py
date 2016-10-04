from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import exists, alias, select, or_

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from .exceptions import BadTableException


class QueryLayer(object):
    tables = {}
    fixtures = {
        "clefs": [{"name": "treble", "sign": "G", "line": 2},
                  {"name": "french", "sign": "G", "line": 1},
                  {"name": "varbaritone", "sign": "F", "line": 1},
                  {"name": "subbass", "sign": "F", "line": 5},
                  {"name": "bass", "sign": "F", "line": 4},
                  {"name": "alto", "sign": "C", "line": 3},
                  {"name": "percussion", "sign": "percussion", "line": -1},
                  {"name": "tenor", "sign": "C", "line": 4},
                  {"name": "baritone", "sign": "C", "line": 5},
                  {"name": "mezzosoprano", "sign": "C", "line": 2},
                  {"name": "soprano", "sign": "C", "line": 1},
                  {"name": "varC", "sign": "VARC", "line": -1},
                  {"name": "alto varC", "sign": "VARC", "line": 3},
                  {"name": "tenor varC", "sign": "VARC", "line": 4},
                  {"name": "baritone varC", "sign": "VARC", "line": 5}],

        "keys": [{"name": "C flat major", "fifths": -7, "mode": "major"},
                 {"name": "G flat major", "fifths": -6, "mode": "major"},
                 {"name": "D flat major", "fifths": -5, "mode": "major"},
                 {"name": "A flat major", "fifths": -4, "mode": "major"},
                 {"name": "E flat major", "fifths": -3, "mode": "major"},
                 {"name": "B flat major", "fifths": -2, "mode": "major"},
                 {"name": "F major", "fifths": -1, "mode": "major"},
                 {"name": "C major", "fifths": 0, "mode": "major"},
                 {"name": "G major", "fifths": 1, "mode": "major"},
                 {"name": "D major", "fifhts": 2, "mode": "major"},
                 {"name": "A major", "fifths": 3, "mode": "major"},
                 {"name": "E major", "fifths": 4, "mode": "major"},
                 {"name": "B major", "fifths": 5, "mode": "major"},
                 {"name": "F# major", "fifths": 6, "mode": "major"},
                 {"name": "C# major", "fifths": 7, "mode": "major"},
                 {"name": "A flat minor", "fifths": -7, "mode": "minor"},
                 {"name": "E flat minor", "fifths": -6, "mode": "minor"},
                 {"name": "B flat minor", "fifths": -5, "mode": "minor"},
                 {"name": "F minor", "fifths": -4, "mode": "minor"},
                 {"name": "C minor", "fifths": -3, "mode": "minor"},
                 {"name": "G minor", "fifths": -2, "mode": "minor"},
                 {"name": "D minor", "fifths": -1, "mode": "minor"},
                 {"name": "A minor", "fifths": 0, "mode": "minor"},
                 {"name": "E minor", "fifths": 1, "mode": "minor"},
                 {"name": "B minor", "fifths": 2, "mode": "minor"},
                 {"name": "F# minor", "fifths": 3, "mode": "minor"},
                 {"name": "C# minor", "fifths": 4, "mode": "minor"},
                 {"name": "G# minor", "fifths": 5, "mode": "minor"},
                 {"name": "D# minor", "fifths": 6, "mode": "minor"},
                 {"name": "A# minor", "fifths": 7, "mode": "minor"}]
    }

    def __init__(self, db_path):
        self.engine = create_engine(db_path, echo=True)

    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def setup(self):
        metadata = MetaData()
        self.tables["creators"] = Table(
            'creators', metadata, Column(
                'id', Integer, primary_key=True), Column(
                'name', String))

        self.tables["instruments"] = Table(
            'instruments', metadata, Column(
                'id', Integer, primary_key=True), Column(
                'name', String), Column(
                'chromatic', Integer), Column(
                    'diatonic', Integer))

        self.tables["keys"] = Table('keys', metadata,
                                    Column('id', Integer, primary_key=True),
                                    Column('name', String, unique=True),
                                    Column('mode', String),
                                    Column('fifths', Integer))

        self.tables["clefs"] = Table('clefs', metadata,
                                     Column('id', Integer, primary_key=True),
                                     Column('name', String, unique=True),
                                     Column('sign', String),
                                     Column('line', Integer))

        self.tables["tempos"] = Table('tempos', metadata,
                                      Column('id', Integer, primary_key=True),
                                      Column('beat', String),
                                      Column('minute', Integer),
                                      Column('beat_2', String))

        self.tables["time_signatures"] = Table(
            'time_signatures', metadata, Column(
                'id', Integer, primary_key=True), Column(
                'beat', Integer), Column(
                'beat_type', Integer))

        self.tables["pieces"] = Table(
            'pieces', metadata, Column(
                'id', Integer, primary_key=True), Column(
                'name', String), Column(
                'filename', String, unique=True), Column(
                    'archived', Boolean), Column(
                        'composer.id', None, ForeignKey('creators.id')), Column(
                            'lyricist.id', None, ForeignKey('creators.id')))

        self.tables["playlists"] = Table(
            'playlists', metadata, Column(
                'id', Integer, primary_key=True), Column(
                'name', String))
        self.tables["playlist_join"] = Table(
            'playlist_join', metadata, Column(
                'playlists.id', Integer, ForeignKey('playlists.id')), Column(
                'pieces.id', Integer, ForeignKey('pieces.id')))

        self.tables["sources"] = Table('sources', metadata,
                                       Column('id', Integer, primary_key=True),
                                       Column('name', String))

        self.tables["sources_piece"] = Table(
            'source_join', metadata, Column(
                'piece.id', Integer, ForeignKey('pieces.id')), Column(
                'source.id', Integer, ForeignKey('sources.id')))

        self.tables["keys_ins_piece"] = Table(
            'key_ins_piece_join', metadata, Column(
                'piece.id', Integer, ForeignKey('pieces.id')), Column(
                'keys.id', Integer, ForeignKey('keys.id')), Column(
                'instruments.id', Integer, ForeignKey('instruments.id')))

        self.tables["clefs_ins_piece"] = Table(
            'clef_ins_piece_join', metadata, Column(
                'piece.id', Integer, ForeignKey('pieces.id')), Column(
                'clefs.id', Integer, ForeignKey('clefs.id')), Column(
                'instruments.id', Integer, ForeignKey('instruments.id')))

        self.tables["tempos_piece"] = Table(
            'tempo_piece_join', metadata, Column(
                'piece.id', Integer, ForeignKey('pieces.id')), Column(
                'tempos.id', Integer, ForeignKey('tempos.id')))

        self.tables["time_signatures_piece"] = Table(
            'time_piece_join', metadata, Column(
                'piece.id', Integer, ForeignKey('pieces.id')), Column(
                'time_signatures.id', Integer, ForeignKey('time_signatures.id')))

        metadata.create_all(self.engine)

    def validate_table(self, table):
        return table in self.tables

    def get_or_add(self, data, table="instruments"):
        elem = self.query(data, table=table)
        if elem is None or len(elem) == 0:
            self.add(data, table=table)
            elem = self.query(data, table=table)
        return elem

    def add_and_link(self, data, piece_id, table="tempos"):
        elem = self.get_or_add(data, table=table)[0]
        self.add({table + ".id": elem['id'],
                  "piece.id": piece_id},
                 table=table + "_piece")

    def add_multiple(self, data_list, table="pieces"):
        ids = []
        for elem in data_list:
            ids.append(self.add(elem, table=table))

    def add(self, data_dict, table="pieces"):
        if self.validate_table(table):
            query = self.tables[table].insert().values(**data_dict)
            return self.execute(query).inserted_primary_key
        else:
            raise BadTableException(
                "table {} not in {}".format(
                    table, self.tables.keys()))

    def like(self, data, table="pieces"):
        if self.validate_table(table):
            _table = self.tables[table]
            session = self.get_session()
            query = session.query(_table)
            keys = [col.name for col in _table.columns]
            for key in data:
                attr = getattr(_table.columns, key)
                print(attr)
                query = query.filter(attr.like(data[key]))
            return [{key: value for key, value in zip(
                keys, entry)} for entry in query.all()]
        else:
            raise BadTableException(
                "table {} not in {}".format(
                    table, self.tables.keys()))

    def mk_or_expr(self, elems, column):
        expr = column == elems[0]
        for e in elems:
            expr = or_(expr, (column == e))
        return expr

    def query_multiple(
            self,
            data,
            filter_col="piece.id",
            table="clefs_ins_piece"):
        if self.validate_table(table):
            _table = self.tables[table]
            _filter_col = getattr(_table.columns, filter_col)
            q = select([_filter_col])
            for elem in data:
                query = _table.select()
                nxtalias = alias(_table)
                for key in elem:
                    col = getattr(nxtalias.columns, key)
                    expr = self.mk_or_expr(elem[key], col)
                    query = query.where(expr)

                alias_filter = getattr(nxtalias.columns, filter_col)
                query = query.where(alias_filter == _filter_col)
                q = q.where(exists(query))

            result_prox = self.execute(q)
            return set([elem[0] for elem in result_prox])
        else:
            raise BadTableException(
                "table {} not in {}".format(
                    table, self.tables.keys()))

    def get_ids_for_like(self, data, table="pieces"):
        result = self.like(data, table="instruments")
        ids = [elem['id'] for elem in result]
        return ids

    def query(self, data, table="pieces"):
        if self.validate_table(table):
            query = self.mk_query(data, table=table)
            keys = [col.name for col in self.tables[table].columns]
            return [{key: value for key, value in zip(
                keys, entry)} for entry in query.all()]
        else:
            raise BadTableException(
                "table {} not in {}".format(
                    table, self.tables.keys()))

    def mk_query(self, data, table="pieces"):
        if self.validate_table(table):
            session = self.get_session()
            query = session.query(self.tables[table]).filter_by(**data)
            return query
        else:
            raise BadTableException(
                "table {} not in {}".format(
                    table, self.tables.keys()))

    def mk_like_query(self, data, table="pieces"):
        pass

    def get_all(self, table="pieces"):
        if self.validate_table(table):
            query = self.tables[table].select()
            return self.execute(query)
        else:
            raise BadTableException(
                "table {} not in {}".format(
                    table, self.tables.keys()))

    def update(self, id, data, table="pieces"):
        if self.validate_table(table):
            query = update(
                self.tables[table]).where(
                self.tables[table].c.id == id).values(
                **data)
            self.execute(query)
        else:
            raise BadTableException(
                "table {} not in {}".format(
                    table, self.tables.keys()))

    def execute(self, query):
        conn = self.engine.connect()
        return conn.execute(query)

    def add_fixtures(self):
        for table in self.fixtures:
            for elem in self.fixtures[table]:
                self.get_or_add(elem, table=table)
