from PyQt4 import QtGui, QtCore, uic
from PyQt4.QtCore import SIGNAL
import sip
import os
import difflib
import time
from sys import platform
if platform != 'win32':
    from popplerqt4 import Poppler
from implementation.primaries.GUI.helpers import get_base_dir, parseStyle, postProcessLines, merge_instruments, merge_clefs_and_keys, fit_columns_to_widget
from implementation.primaries.GUI import themedWindow, Widgets, qt_threading, MultistandWidget, pdfViewer


class MainWindow(QtGui.QMainWindow, themedWindow.ThemedWindow):
    widgets = {}
    frames = {}
    colors = {}

    def __init__(self, app, theme, theme_folder, design_folder):
        QtGui.QMainWindow.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, theme_folder)
        self.qApp = app
        self.theme = theme
        self.theme_folder = theme_folder
        self.design_folder = design_folder
        self.loaded = ""
        self.current_piece = ""
        self.playlist = None
        self.index = None
        self.themeSet = False

    def resizeEvent(self, QResizeEvent):
        if hasattr(self, "scoreWindow"):
            self.resizeScoreWindow()
        if hasattr(self, "playlistTable"):
            self.resizePlaylistTable()
        if hasattr(self, "searchBar"):
            self.resizeSearchbar()
        QResizeEvent.accept()

    def resizeScoreWindow(self):
        if not self.scoreWindow.isHidden():
            widgetSize = (
                self.scoreWindow.width(), self.scoreWindow.height())
            self.resizeCenterWidget(self.scoreWindow)
            self.resizePages(widgetSize)

    def resizePlaylistTable(self):
        if not self.playlistTable.isHidden():
            self.resizeCenterWidget(self.playlistTable)
            fit_columns_to_widget(self.playlistTable, 10)
            for i in range(10):
                self.playlistTable.setColumnWidth(
                    i, self.playlistTable.width() / 9)

    def resizeCenterWidget(self, item):
        """
        method which resizes either center widget
        (should be score viewer or playlist table)
        according to changes in window size
        :param item: the item to modify
        :return:
        """
        position = item.pos()
        width = self.width() - self.buttonFrame.width()
        height = self.height() - self.searchBar.height()
        item.setGeometry(position.x(), position.y(), width, height)

    def resizePages(self, size):
        percentWidth = self.scoreWindow.width() / size[0]
        percentHeight = self.scoreWindow.height() / size[1]
        self.scoreWindow.scale(percentWidth, percentHeight)

    def resizeSearchbar(self):
        """
        method which resizes the search bar at the top
        of the screen according to window width
        :return:
        """
        search_position = self.searchBar.pos()
        search_width = self.width()
        search_height = self.searchBar.height()
        self.searchBar.setGeometry(
            search_position.x(),
            search_position.y(),
            search_width,
            search_height)

    def closeEvent(self, QCloseEvent):
        self.hide()
        self.qApp.setup_startup()
        QCloseEvent.accept()

    def load(self):
        file = os.path.join(self.design_folder, "MainWindow.ui")
        uic.loadUi(file, self)
        self.setGeometry(0, 0, self.width(), self.height())
        self.widgets["scorebook"] = Widgets.Scorebook(self, self.design_folder)
        self.colors["scorebook"] = "rgba(170, 255, 8, 255)"
        self.colors["myplaylist"] = "rgba(248, 213, 17, 255)"
        self.colors["autoplaylist"] = "rgba(235, 25, 39, 255)"
        self.colors["info"] = "rgba(253, 127, 60, 255)"
        self.widgets["myplaylist"] = Widgets.MyPlaylists(
            self, self.design_folder)
        self.widgets["autoplaylist"] = Widgets.AutoPlaylists(
            self, self.design_folder)
        self.widgets["info"] = Widgets.PieceInfo(self, self.design_folder)
        self.widgets["featured"] = Widgets.FeaturedIn(self, self.design_folder)
        self.widgets["browser"] = Widgets.PlaylistBrowser(
            self, self.design_folder)
        self.widgets["search"] = Widgets.SearchTree(self, self.design_folder)
        layout = self.searchFrame.layout()
        layout.addWidget(self.widgets["search"])
        self.searchFrame.setGeometry(
            self.searchFrame.pos().x(),
            self.searchFrame.pos().y(),
            self.widgets["search"].width(),
            self.widgets["search"].height())
        self.scorebookBtn.clicked.connect(self.sidemenu_callback)
        self.myPlaylistBtn.clicked.connect(self.sidemenu_callback)
        self.autoPlaylistBtn.clicked.connect(self.sidemenu_callback)
        self.browserBtn.clicked.connect(self.sidemenu_callback)
        self.featuredBtn.clicked.connect(self.sidemenu_callback)
        self.infoBtn.clicked.connect(self.sidemenu_callback)
        self.searchInput.setCursorPosition(10)
        self.searchInput.textChanged.connect(self.updateOptions)
        self.searchInput.editingFinished.connect(self.finished)
        self.contentFrame.setGeometry(0, 0, 10, 10)
        self.contentFrame.hide()
        self.searchBar.setGeometry(self.searchBar.pos().x(
        ), self.searchBar.pos().y(), self.width(), self.searchBar.height())
        self.centralWidget().setStyleSheet(
            "QWidget#centralwidget {border-image:url("
            "alternatives/sheet-music-texture.png) "
            "0 0 stretch stretch;}")
        self.actionUbuntu.triggered.connect(self.change_theme)
        self.actionCandy.triggered.connect(self.change_theme)
        self.searchFrame.hide()
        self.scoreWindow.hide()
        self.multistndBtn.hide()
        self.popoutBtn.hide()
        self.popoutBtn.setToolTip("Open in default pdf viewer")
        self.multistndBtn.setToolTip("Open in multi stand mode")
        self.zoomOutBtn.hide()
        self.zoomInBtn.hide()
        self.zoomInBtn.clicked.connect(self.zoomIn)
        self.zoomOutBtn.clicked.connect(self.zoomOut)
        self.popoutBtn.clicked.connect(self.onPopoutClicked)
        self.multistndBtn.clicked.connect(self.onMultistandClicked)
        self.wifiButton.clicked.connect(self.onWifiClicked)
        # self.scoreWebView.hide()
        self.playlistTable.hide()
        self.playlistTable.itemDoubleClicked.connect(
            self.onPlaylistItemClicked)

        self.actionRefresh_Collection.triggered.connect(self.qApp.updateDb)
        self.actionNew_Collection.triggered.connect(self.newCollection)
        self.actionImport.triggered.connect(self.qApp.importWindow)
        self.viewer = pdfViewer.PDFViewer(self.scoreWindow.width() / 2)
        if platform == "win32":
            self.applyTheme()

    def onWifiClicked(self):
        wifiOn = self.qApp.toggleWifi()
        if wifiOn:
            self.wifiButton.setStyleSheet("""background:
            url(/themes/icons/{}/wifi-on.png) center no-repeat;
            """.format(self.theme))
        else:
            self.wifiButton.setStyleSheet("""
            background: url(/themes/icons/{}/wifi-off.png)
            center no-repeat;
            """.format(self.theme))

    def zoomIn(self):
        self.scoreWindow.scale(1.1, 1.1)
        pass

    def zoomOut(self):
        self.scoreWindow.scale(0.9, 0.9)
        pass

    def mousePressEvent(self, QMouseEvent):
        if not self.themeSet:
            self.applyTheme()
        QMouseEvent.accept()

    def focusInEvent(self, QFocusEvent):
        print("hello, world")
        if not self.themeSet:
            self.themeSet = True
            self.applyTheme()
        QFocusEvent.accept()

    def change_theme(self):
        sender = self.sender()
        name = sender.objectName()[6:].lower()
        self.theme = name
        self.qApp.updateTheme(self.theme)
        self.applyTheme()

    # methods which handle querying
    def updateOptions(self):
        text = self.searchInput.text()
        self.widgets["search"].clear()
        self.qApp.query(text)
        self.searchFrame.show()
        self.searchFrame.raise_()
        self.scoreWindow.lower()
        self.playlistTable.lower()

    def onQueryReturned(self, results, query):
        """
        callback which gets called when the query
        has been handled by the parent application
        :param results:  nested list of results to put into the tree
        :return:
        """
        if len(results) > 0:
            self.widgets["search"].load(results)
        else:
            self.widgets["search"].clear()
        self.widgets["search"].show()
        self.searchFrame.show()

    def finished(self):
        """
        callback for when a user has finished entering text in the search bar
        :return:
        """
        widget = self.focusWidget()
        if (self.searchInput.text() == ""
            or self.searchInput.text() == " ") \
                or widget.objectName() != "treeWidget":
            try:
                self.searchFrame.hide()
            except:
                print("we're done here. gbye")

    # methods which handle playlists
    def loadPlaylist(self, playlist_title, playlist_to_load, length):
        """
        method which gets called by either of the playlist
         widgets when a user clicks a playlist
        :param playlist_title: title of the playlist
        :param playlist_to_load: list of files in the playlist
        :param length: length of the playlist items
        :return:
        """
        self.scoreWindow.hide()
        self.playlistTable.setRowCount(length)
        file_data = self.qApp.getPlaylistFileInfo(playlist_to_load)
        data_items = self.setup_data_items(
            playlist_to_load, file_data, 0, len(file_data))
        for i in range(len(data_items)):
            for j in range(len(data_items[i])):
                self.playlistTable.setItem(i, j, data_items[i][j])
        self.setWindowTitle("MuseLib | Playlist: " + playlist_title)
        self.playlistTable.show()
        self.playlistTable.lower()
        fit_columns_to_widget(self.playlistTable, 10)
        self.playlist = playlist_title
        self.resizeCenterWidget(self.playlistTable)

    def setup_data_items(
            self,
            playlist_fnames,
            playlist_data,
            start_index,
            end_index):
        items = []
        keys = (
            "title",
            "composer",
            "lyricist",
            "instruments",
            "filename",
            "clefs",
            "keys",
            "tempos",
            "time_signatures")
        alternate_method = {"instruments": merge_instruments,
                            "clefs": merge_clefs_and_keys,
                            "keys": merge_clefs_and_keys}
        for i in range(start_index, end_index):
            file = playlist_data[i]
            row = []
            for key in keys:
                if key in file:
                    if key in alternate_method:
                        value = alternate_method[key](file[key])
                    else:
                        value = file[key]
                        if isinstance(value, list):
                            value = ", ".join(file[key])
                    item = QtGui.QTableWidgetItem(value)
                    item.setData(32, file["filename"])
                    item.setData(3, i)
                    item.setData(4, playlist_fnames)
                    row.append(item)

                else:
                    item = QtGui.QTableWidgetItem("")
                    item.setData(32, file["filename"])
                    item.setData(3, i)
                    item.setData(4, playlist_fnames)
                    row.append(item)
            items.append(row)
        return items

    def onPlaylistItemClicked(self, current_item):
        """
        callback for when an item is double clicked in a playlist table
        :param current_item: the current QTableItem
        :return:
        """
        self.playlist = current_item.data(4)
        self.index = current_item.data(3)
        self.playlistTable.hide()
        self.qApp.loadFile(current_item.data(32))

    def onMultistandClicked(self):
        self.popout = MultistandWidget.MultistandWidget(
            self.pdf_loaded, self.folder, self.theme)
        self.popout.applyTheme()
        self.popout.show()

    def onPopoutClicked(self):
        os.open(self.pdf_loaded, 0)

    # methods to handle pieces
    def onPieceLoaded(self, filename, split_file):
        """
        callback which is called when the parent application has finished working on an xml file
        :param filename: the fully qualified filename location including folder
        :param split_file: the filename with no folder location
        :return:
        """
        self.pdf_loaded = filename
        file_to_load = split_file.split(".")[0] + ".xml"
        self.current_piece = file_to_load
        # self.showToolbarBtns()
        # self.loadPieceData(file_to_load)
        if platform != "win32":
            self.loadPdfToGraphicsWidget(filename)
        else:
            os.startfile(filename)
        # self.loadPdfToWebWidget(filename)
        self.setWindowTitle("MuseLib | Piece: " + file_to_load)
        self.resizeCenterWidget(self.scoreWindow)
        self.scoreWindow.show()
        self.scoreWindow.lower()
        self.multistndBtn.show()
        self.popoutBtn.show()
        self.zoomInBtn.show()
        self.zoomOutBtn.show()
        # self.loadFeaturedIn(file_to_load)
        # self.playlistViewer.hide()
        # self.pieceInfoWidget.show()

    def loadPdfToGraphicsWidget(self, filename):
        """
        sets up the graphics view with pairs of pages
        :param filename: pdf file to load
        :return:
        """
        self.viewer.setPDF(filename)
        scene = self.viewer.getScene()
        self.scoreWindow.setScene(scene)

    def loadPdfToWebWidget(self, filename):
        f = QtCore.QUrl().fromLocalFile(filename)
        print(f)

    def _loadfinished(self):
        print("complete")
        # self.scoreWebView.repaint()
        pass

    # callbacks for the buttons in the side menu
    def sidemenu_callback(self):
        sender = self.sender()
        frame_name = sender.objectName().lower()[:-3]
        if self.loaded != frame_name:
            self.loadFrame(frame_name)
        else:
            self.unloadFrame(frame_name)

    def cleanupContentLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widge = item.widget()
                if widge is not None:
                    widge.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(layout)

    # methods to handle loading frames
    def loadFrame(self, child, ypos=72):
        """
        method which fetches the appropriate widget, puts it in the
        content frame and starts an animation to pull the frame out
        :param child: the name of the widget to load
        :param ypos: position to place the widget on the y plane
        :return:
        """
        position = self.contentFrame.pos()
        widget = self.widgets[child]
        self.connect(
            widget,
            SIGNAL("widget_signal(PyQt_PyObject, PyQt_PyObject, PyQt_PyObject)"),
            self.qApp.on_WidgetSignal)
        self.connect(self,
                     SIGNAL("onWidgetReady()"),
                     widget.onWidgetReady)
        endx = self.buttonFrame.width() - 1
        endy = position.y()
        endwidth = widget.width()
        layout = self.contentFrame.layout()
        self.cleanupContentLayout(layout)

        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(widget)
        fob = open(os.path.join(self.theme_folder, "basic_widget.qss"), 'r')
        lines = fob.readlines()
        fob.close()
        stylesheet = []
        if child in self.colors:
            background = "QFrame#contentFrame { background:" + \
                self.colors[child] + ";}"
            stylesheet.append(background)

        stylesheet.extend(lines)

        if not self.contentFrame.layout():
            self.contentFrame.setLayout(layout)
        style = parseStyle(stylesheet, self.theme, self.theme_folder)
        self.contentFrame.setStyleSheet(postProcessLines(style))
        self.contentFrame.show()
        self.contentFrame.lower()
        self.scoreWindow.lower()
        self.playlistTable.lower()
        animation = QtCore.QPropertyAnimation(self.contentFrame, "geometry")
        animation.setDuration(200)
        animation.setStartValue(
            QtCore.QRect(
                0,
                ypos,
                self.buttonFrame.width(),
                self.buttonFrame.height()))
        animation.setEndValue(
            QtCore.QRect(endx, ypos, endwidth, self.buttonFrame.height()))
        animation.start()
        self.animation = animation
        self.loaded = child
        self.emit(SIGNAL("onWidgetReady()"))

    def unloadFrame(self, child):
        """
        method which handles the animation of a frame in
        terms of putting it back where it started
        :param child: name of the frame to onload. No longer really used
        :return:
        """
        position = self.contentFrame.pos()
        endx = 0
        endy = position.y()
        endwidth = self.buttonFrame.width()
        # self.contentFrame.lower()

        animation = QtCore.QPropertyAnimation(self.contentFrame, "geometry")
        animation.setDuration(200)
        animation.setStartValue(
            QtCore.QRect(
                position.x(),
                position.y(),
                self.contentFrame.width(),
                self.contentFrame.height()))
        animation.setEndValue(
            QtCore.QRect(endx, endy, endwidth, self.contentFrame.height()))
        animation.start()
        self.animation = animation
        self.loaded = None

    def unloadSearch(self):
        self.searchFrame.hide()

    # callbacks for actions
    def newCollection(self):
        self.qApp.folder = ""
        self.qApp.setup_startup()
        self.close()
