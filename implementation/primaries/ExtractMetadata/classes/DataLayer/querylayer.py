from sqlalchemy import create_engine, update
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey, Boolean

class QueryLayer(object):
    tables = {}
    def __init__(self, db_path):
        self.engine = create_engine(db_path, echo=True)

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

        self.tables["sources"] = Table('sources', metadata,
                                       Column('id', Integer, primary_key=True),
                                       Column('name', String))

        self.tables["source_join"] = Table('source_join', metadata,
                                           Column('piece.id', Integer, ForeignKey('pieces.id')),
                                           Column('source.id', Integer, ForeignKey('sources.id')))

        self.tables["key_ins_piece"] = Table('key_ins_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('keys.id', Integer, ForeignKey('keys.id')),
                                   Column('instruments.id', Integer, ForeignKey('instruments.id')))

        self.tables["clef_ins_piece"] = Table('clef_ins_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('clefs.id', Integer, ForeignKey('clefs.id')),
                                   Column('instruments.id', Integer, ForeignKey('instruments.id')))

        self.tables["tempo_piece"] = Table('tempo_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('tempos.id', Integer, ForeignKey('tempos.id')))

        self.tables["time_piece"] = Table('time_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('time_signatures.id', Integer, ForeignKey('time_signatures.id')))

        metadata.create_all(self.engine)

    def add(self, data_dict, table="pieces"):
        query = self.tables[table].insert().values(**data_dict)
        self.execute(query)

    def get(self, table="pieces"):
        query = self.tables[table].select()
        return self.execute(query)

    def update(self, id, data, table="pieces"):
        query = update(self.tables[table]).where(self.tables[table].c.id == id).values(**data)
        self.execute(query)

    def execute(self, query):
        conn = self.engine.connect()
        return conn.execute(query)
