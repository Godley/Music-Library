from PyQt4.QtTest import QTest
from PyQt4.QtCore import Qt


class TestSuiteSidebar(object):
    def assert_widget_loaded(self, widget, main_window, value=None):
        QTest.mouseClick(widget, Qt.LeftButton)
        assert main_window.loaded == value
        if value is not None:
            layout = main_window.contentFrame.layout()
            widget = layout.itemAt(0).widget()
            assert widget.title_str.lower() == value.lower()

    def test_btn1(self, main_window, scorebook):
        widget = main_window.scorebookBtn
        self.assert_widget_loaded(widget, main_window, value=scorebook)


    def test_btn2(self, main_window, playlist):
        widget = main_window.myPlaylistBtn
        self.assert_widget_loaded(widget, main_window, value=playlist)

    def test_btn3(self, main_window, auto_playlist):
        widget = main_window.autoPlaylistBtn
        self.assert_widget_loaded(widget, main_window, value=auto_playlist)

    def test_btn4(self, main_window, info):
        widget = main_window.infoBtn
        self.assert_widget_loaded(widget, main_window, value=info)

    def test_btn5(self, main_window, featured):
        widget = main_window.featuredBtn
        self.assert_widget_loaded(widget, main_window, value=featured)

    def test_btn6(self, main_window, browser):
        widget = main_window.browserBtn
        self.assert_widget_loaded(widget, main_window, value=browser)

    def test_btn1_doubleclick_unload(self, main_window, scorebook):
        widget = main_window.scorebookBtn
        self.assert_widget_loaded(widget, main_window, value=scorebook)
        self.assert_widget_loaded(widget, main_window)

    def test_btn2_doubleclick_unload(self, main_window, playlist):
        widget = main_window.myPlaylistBtn
        self.assert_widget_loaded(widget, main_window, value=playlist)
        self.assert_widget_loaded(widget, main_window)

    def test_btn3_doubleclick_unload(self, main_window, auto_playlist):
        widget = main_window.autoPlaylistBtn
        self.assert_widget_loaded(widget, main_window, value=auto_playlist)
        self.assert_widget_loaded(widget, main_window)

    def test_btn4_doubleclick_unload(self, main_window, info):
        widget = main_window.infoBtn
        self.assert_widget_loaded(widget, main_window, value=info)
        self.assert_widget_loaded(widget, main_window)

    def test_btn5_doubleclick_unload(self, main_window, featured):
        widget = main_window.featuredBtn
        self.assert_widget_loaded(widget, main_window, value=featured)
        self.assert_widget_loaded(widget, main_window)

    def test_btn6_doubleclick_unload(self, main_window, browser):
        widget = main_window.browserBtn
        self.assert_widget_loaded(widget, main_window, value=browser)
        self.assert_widget_loaded(widget, main_window)