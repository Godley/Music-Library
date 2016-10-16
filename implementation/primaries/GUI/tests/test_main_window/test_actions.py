from ..helpers.qt_utils import click, action_click
from PyQt4.QtGui import QMenu
from unittest.mock import MagicMock


class TestSuiteActions(object):
    def test_import_collection(self, main_window, import_window):
        widget = main_window.my_menu
        menu = widget.findChildren(QMenu)[0]
        click(menu)
        action = action_click(0, menu)
        assert action is not None
        assert not import_window.isHidden()

    def test_new_collection(self, main_window, startup_window):
        widget = main_window.my_menu
        menu = widget.findChildren(QMenu)[0]
        click(menu)
        action = action_click(1, menu)
        assert action is not None
        assert main_window.isHidden()
        assert not startup_window.isHidden()

    def test_refresh_collection(self, main_window, startup_window):
        widget = main_window.my_menu
        menu = widget.findChildren(QMenu)[0]
        self.update = main_window.qApp.updateDb
        main_window.qApp.updateDb = MagicMock()
        click(menu)
        action = action_click(2, menu)
        assert action is not None
        assert main_window.qApp.updateDb.assert_called_once_with()
        main_window.qApp.updateDb = self.update