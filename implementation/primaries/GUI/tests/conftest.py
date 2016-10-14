from ..MainWindow import MainWindow
from Application import Application
import pytest
from ..Widgets import Scorebook, PlaylistWidget
from PyQt4 import QtGui
import sys


@pytest.fixture(scope="session")
def app():
    app = QtGui.QApplication(sys.argv)
    return app

@pytest.fixture(scope="session")
def application(app):
    return Application(app)

@pytest.fixture(scope="session")
def main_window(application):
    application.windows["main"].load()
    return application.windows["main"]

@pytest.fixture()
def scorebook():
    return "scorebook"

@pytest.fixture()
def playlist():
    return "myplaylist"

@pytest.fixture()
def auto_playlist():
    return "autoplaylist"

@pytest.fixture()
def info():
    return "info"

@pytest.fixture()
def featured():
    return "featured"

@pytest.fixture()
def browser():
    return "browser"