from ..MainWindow import MainWindow
from Application import Application
import pytest
from ..Widgets import Scorebook, PlaylistWidget
from PyQt4 import QtGui
import sys
import os


@pytest.fixture(scope="session")
def folder():
    return os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        "test_files")


@pytest.fixture(scope="session")
def app():
    app = QtGui.QApplication(sys.argv)
    return app


@pytest.fixture(scope="session")
def application(app, folder):
    appl = Application(app)
    appl.loadFolder(folder)
    return appl


@pytest.fixture()
def main_window(application):
    application.windows["main"].load()
    yield application.windows["main"]
    application.windows["main"].unloadFrame("scorebook")


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
