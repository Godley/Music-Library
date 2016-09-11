from sqlalchemy import create_engine
from sqlalchemy import Table, Column, Integer, String, MetaData, ForeignKey

class QueryLayer(object):
    def __init__(self, db_path):
        self.engine = create_engine(db_path, echo=True)

    def setup(self):
        metadata = MetaData()
        self.creators = Table('creators', metadata,
                         Column('id', Integer, primary_key=True),
                         Column('name', String))

        self.instruments = Table('instruments', metadata,
                            Column('id', Integer, primary_key=True),
                            Column('name', String),
                            Column('chromatic', Integer),
                            Column('diatonic', Integer))

        self.keys = Table('keys', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String, unique=True),
                     Column('mode', String),
                     Column('fifths', Integer))

        self.clefs = Table('clefs', metadata,
                     Column('id', Integer, primary_key=True),
                     Column('name', String, unique=True),
                     Column('sign', String),
                     Column('line', Integer))

        self.tempos = Table('tempos', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('beat', String),
                       Column('minute', Integer),
                       Column('beat_2', String))

        self.time_sigs = Table('time_signatures', metadata,
                          Column('id', Integer, primary_key=True),
                          Column('beat', Integer),
                          Column('beat_type', Integer))

        self.pieces = Table('pieces', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('name', String),
                       Column('filename', String, unique=True),
                       Column('composer.id', None, ForeignKey('creators.id')),
                       Column('lyricist.id', None, ForeignKey('creators.id')))

        self.key_ins_piece_join = Table('key_ins_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('keys.id', Integer, ForeignKey('keys.id')),
                                   Column('instruments.id', Integer, ForeignKey('instruments.id')))

        self.clef_ins_piece_join = Table('clef_ins_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('clefs.id', Integer, ForeignKey('clefs.id')),
                                   Column('instruments.id', Integer, ForeignKey('instruments.id')))

        self.tempo_piece_join = Table('tempo_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('tempos.id', Integer, ForeignKey('tempos.id')))

        self.time_piece_join = Table('time_piece_join', metadata,
                                   Column('piece.id', Integer, ForeignKey('pieces.id')),
                                   Column('time_signatures.id', Integer, ForeignKey('time_signatures.id')))

        metadata.create_all(self.engine)

    def add_piece(self, data_dict):
        query = self.pieces.insert().values(**data_dict)
        self.execute(query)

    def get_pieces(self):
        query = self.pieces.select()
        return self.execute(query)

    def execute(self, query):
        conn = self.engine.connect()
        return conn.execute(query)
