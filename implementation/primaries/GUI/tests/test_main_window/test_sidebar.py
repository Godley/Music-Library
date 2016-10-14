from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt


class TestSuiteSidebar(object):
    def test_btn1(self, main_window, scorebook):
        widget = main_window.scorebookBtn
        QTest.mouseClick(widget, Qt.LeftButton)
        assert main_window.loaded == scorebook
        layout = main_window.contentFrame.layout()
        widget = layout.itemAt(0).widget()
        assert widget.title_str.lower() == scorebook.lower()

    def test_btn2(self, main_window, playlist):
        widget = main_window.myPlaylistBtn
        QTest.mouseClick(widget, Qt.LeftButton)
        assert main_window.loaded == playlist
        layout = main_window.contentFrame.layout()
        widget = layout.itemAt(0).widget()
        title = widget.title_str.lower()
        assert title == playlist

    def test_btn3(self, main_window, auto_playlist):
        widget = main_window.autoPlaylistBtn
        QTest.mouseClick(widget, Qt.LeftButton)
        assert main_window.loaded == auto_playlist
        layout = main_window.contentFrame.layout()
        widget = layout.itemAt(0).widget()
        assert widget.title_str.lower() == auto_playlist

    def test_btn4(self, main_window, info):
        widget = main_window.infoBtn
        QTest.mouseClick(widget, Qt.LeftButton)
        assert main_window.loaded == info
        layout = main_window.contentFrame.layout()
        widget = layout.itemAt(0).widget()
        assert widget.title_str.lower() == info

    def test_btn5(self, main_window, featured):
        widget = main_window.featuredBtn
        QTest.mouseClick(widget, Qt.LeftButton)
        assert main_window.loaded == featured
        layout = main_window.contentFrame.layout()
        widget = layout.itemAt(0).widget()
        assert widget.title_str.lower() == featured

    def test_btn6(self, main_window, browser):
        widget = main_window.browserBtn
        QTest.mouseClick(widget, Qt.LeftButton)
        assert main_window.loaded == browser
        layout = main_window.contentFrame.layout()
        widget = layout.itemAt(0).widget()
        assert widget.title_str.lower() == browser