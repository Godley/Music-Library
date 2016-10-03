from sqlalchemy import create_engine, update
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import exists, alias, select, or_

from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean
from .exceptions import BadTableException

class QueryLayer(object):
    tables = {}

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

    def __init__(self, db_path):
        self.engine = create_engine(db_path, echo=True)


    def get_session(self):
        Session = sessionmaker(bind=self.engine)
        return Session()

    def setup(self):
        metadata = MetaData()
        self.tables["creators"] = Table('creators', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String))

        self.tables["instruments"] = Table('instruments', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String),
                            Column('chromatic', Integer),
                            Column('diatonic', Integer))

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

        self.tables["time_signatures"] = Table('time_signatures', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('beat', Integer),
                          Column('beat_type', Integer))

        self.tables["pieces"] = Table('pieces', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', String),
                       Column('filename', String, unique=True),
                       Column('archived', Boolean),
                       Column('composer.id', None, ForeignKey('creators.id')),
                       Column('lyricist.id', None, ForeignKey('creators.id')))

        self.tables["playlists"] = Table('playlists', metadata,
                                         Column('id', Integer, primary_key=True),
                                         Column('name', String))
        self.tables["playlist_join"] = Table('playlist_join', metadata,
                                             Column('playlists.id', Integer, ForeignKey('playlists.id')),
                                             Column('pieces.id', Integer, ForeignKey('pieces.id')))

        self.tables["sources"] = Table('sources', metadata,
                                       Column('id', Integer, primary_key=True),
                                       Column('name', String))

        self.tables["sources_piece"] = Table('source_join', metadata,
                                           Column('piece.id', Integer, ForeignKey('pieces.id')),
                                           Column('source.id', Integer, ForeignKey('sources.id')))

        self.tables["keys_ins_piece"] = Table('key_ins_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('keys.id', Integer, ForeignKey('keys.id')),
                                   Column('instruments.id', Integer, ForeignKey('instruments.id')))

        self.tables["clefs_ins_piece"] = Table('clef_ins_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('clefs.id', Integer, ForeignKey('clefs.id')),
                                   Column('instruments.id', Integer, ForeignKey('instruments.id')))

        self.tables["tempos_piece"] = Table('tempo_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('tempos.id', Integer, ForeignKey('tempos.id')))

        self.tables["time_signatures_piece"] = Table('time_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('time_signatures.id', Integer, ForeignKey('time_signatures.id')))

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
        self.add({table+".id": elem['id'], "piece.id": piece_id}, table=table+"_piece")

    def add_multiple(self, data_list, table="pieces"):
        ids = []
        for elem in data_list:
            ids.append(self.add(elem, table=table))

    def add(self, data_dict, table="pieces"):
        if self.validate_table(table):
            query = self.tables[table].insert().values(**data_dict)
            return self.execute(query).inserted_primary_key
        else:
            raise BadTableException("table {} not in {}".format(table, self.tables.keys()))

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
            return [{key:value for key, value in zip(keys, entry)} for entry in query.all()]
        else:
            raise BadTableException("table {} not in {}".format(table, self.tables.keys()))

    def query_multiple(self, data, filter_col="piece.id", table="clefs_ins_piece"):
        if self.validate_table(table):
            _table = self.tables[table]
            _filter_col = getattr(_table.columns, filter_col)
            q = select([_filter_col])
            nxtalias = None
            first = True
            for elem in data:
                query = _table.select()
                nxtalias = alias(_table)
                for key in elem:
                    col = getattr(nxtalias.columns, key)

                    if type(elem[key]) is not list:
                        expr = (col == elem[key])
                    else:
                        expr = col == elem[key][0]
                        for val in elem[key][1:]:
                            expr = or_(expr, (col==val))
                    query = query.where(expr)

                alias_filter = getattr(nxtalias.columns, filter_col)
                query = query.where(alias_filter == _filter_col)
                q = q.where(exists(query))

            result_prox = self.execute(q)
            return set([elem[0] for elem in result_prox])
        else:
            raise BadTableException("table {} not in {}".format(table, self.tables.keys()))

    def get_ids_for_like(self, data, table="pieces"):
        result = self.like(data, table="instruments")
        ids = [elem['id'] for elem in result]
        return ids

    def query(self, data, table="pieces"):
        if self.validate_table(table):
            query = self.mk_query(data, table=table)
            keys = [col.name for col in self.tables[table].columns]
            return [{key:value for key, value in zip(keys, entry)} for entry in query.all()]
        else:
            raise BadTableException("table {} not in {}".format(table, self.tables.keys()))

    def mk_query(self, data, table="pieces"):
        if self.validate_table(table):
            session = self.get_session()
            query = session.query(self.tables[table]).filter_by(**data)
            return query
        else:
            raise BadTableException("table {} not in {}".format(table, self.tables.keys()))

    def mk_like_query(self, data, table="pieces"):
        pass

    def get_all(self, table="pieces"):
        if self.validate_table(table):
            query = self.tables[table].select()
            return self.execute(query)
        else:
            raise BadTableException("table {} not in {}".format(table, self.tables.keys()))

    def update(self, id, data, table="pieces"):
        if self.validate_table(table):
            query = update(self.tables[table]).where(self.tables[table].c.id == id).values(**data)
            self.execute(query)
        else:
            raise BadTableException("table {} not in {}".format(table, self.tables.keys()))

    def execute(self, query):
        conn = self.engine.connect()
        return conn.execute(query)

    def init_clefs(self):
        for clef in self.clefs:
            self.get_or_add({'name': clef[0], 'sign': clef[1], 'line': clef[2]}, table='clefs')

    def init_keys(self):
        for key in self.keys:
            self.get_or_add({'name': key[0], 'fifths': key[1], 'mode': key[2]}, table='keys')
