import pytest
from implementation.primaries.ExtractMetadata.classes.DataLayer.querylayer import QueryLayer
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict

@pytest.fixture()
def db():
    return "sqlite:///:memory:"

@pytest.fixture()
def qlayer(db):
    elem = QueryLayer(db)
    elem.setup()
    return elem

@pytest.fixture()
def mlayer(db):
    elem = MusicData(db)
    elem.setup()
    return elem

@pytest.fixture()
def dummy():
    data = {"instruments": [{"name": "wibble"}], "clefs":{"wibble": [{"name": "treble"}]},
            "keys": {"wibble": [{"name": "C major"}]}}
    return data

@pytest.fixture()
def dummy_res():
    return {"keys": {'wibble': ['C major']},
                 "clefs": {'wibble': ['treble']},
                 "instruments": [hashdict(chromatic=None, diatonic=None, name='wibble')]}