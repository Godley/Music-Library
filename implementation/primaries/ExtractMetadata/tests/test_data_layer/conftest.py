import pytest
from ...classes.DataLayer.querylayer import QueryLayer

@pytest.fixture()
def db():
    return "sqlite:///:memory:"

@pytest.fixture()
def qlayer(db):
    elem = QueryLayer(db)
    elem.setup()
    return elem