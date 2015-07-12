import sip
import os, time
from sys import platform
if platform == "darwin":
    from popplerqt4 import Poppler

from PyQt4 import QtGui, QtCore, uic

from implementation.primaries.GUI.helpers import get_base_dir, parseStyle
from implementation.primaries.GUI import themedWindow, Widgets
from implementation.primaries.GUI import Widgets
from implementation.primaries.GUI import qt_threading


class MainWindow(QtGui.QMainWindow, themedWindow.ThemedWindow):
    widgets = {}
    frames = {}
    colors = {}
    def __init__(self, app, theme, theme_folder):
        QtGui.QMainWindow.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, theme_folder)
        self.qApp = app
        self.theme = theme
        self.loaded = ""
        self.current_piece = ""
        self.playlist = None
        self.index = None
        self.themeSet = False

    def resizeEvent(self, QResizeEvent):
        if hasattr(self, "scoreWindow"):
            if not self.scoreWindow.isHidden():
                widgetSize = (self.scoreWindow.width(), self.scoreWindow.height())
                self.resizeCenterWidget(self.scoreWindow)
                self.resizePages(widgetSize)
        if hasattr(self, "playlistTable"):
            if not self.playlistTable.isHidden():
                self.resizeCenterWidget(self.playlistTable)
                for i in range(10):
                    self.playlistTable.setColumnWidth(i, self.playlistTable.width()/9)
        if hasattr(self, "searchBar"):
            self.resizeSearchbar()
        QResizeEvent.accept()

    def resizeCenterWidget(self, item):
        """
        method which resizes either center widget (should be score viewer or playlist table) according to changes in window size
        :param item: the item to modify
        :return:
        """
        position = item.pos()
        width = self.width() - self.buttonFrame.width()
        height = self.height() - self.searchBar.height()
        item.setGeometry(position.x(), position.y(), width, height)

    def resizePages(self, size):
        percentWidth = self.scoreWindow.width()/size[0]
        percentHeight = self.scoreWindow.height()/size[1]
        self.scoreWindow.scale(percentWidth, percentHeight)

    def resizeSearchbar(self):
        """
        method which resizes the search bar at the top of the screen according to window width
        :return:
        """
        search_position = self.searchBar.pos()
        search_width = self.width()
        search_height = self.searchBar.height()
        self.searchBar.setGeometry(search_position.x(), search_position.y(), search_width, search_height)

    def closeEvent(self, QCloseEvent):
        self.hide()
        self.qApp.setup_startup()
        QCloseEvent.accept()

    def load(self):
        file = os.path.join(get_base_dir(True), "designer_files", "MainWindow.ui")
        uic.loadUi(file, self)
        self.setGeometry(0, 0, self.width(), self.height())
        self.widgets["scorebook"] = Widgets.Scorebook
        self.colors["scorebook"] = "rgba(170, 255, 8, 255)"
        self.colors["myplaylist"] = "rgba(248, 213, 17, 255)"
        self.colors["autoplaylist"] = "rgba(235, 25, 39, 255)"
        self.colors["info"] = "rgba(253, 127, 60, 255)"
        self.widgets["myplaylist"] = Widgets.MyPlaylists
        self.widgets["autoplaylist"] = Widgets.AutoPlaylists
        self.widgets["info"] = Widgets.PieceInfo
        self.widgets["featured"] = Widgets.FeaturedIn
        self.widgets["browser"] = Widgets.PlaylistBrowser
        self.widgets["search"] = Widgets.SearchTree(self)
        layout = self.searchFrame.layout()
        layout.addWidget(self.widgets["search"])
        self.searchFrame.setGeometry(self.searchFrame.pos().x(), self.searchFrame.pos().y(), self.widgets["search"].width(), self.widgets["search"].height())
        self.scorebookBtn.clicked.connect(self.scorebook)
        self.myPlaylistBtn.clicked.connect(self.myplaylist)
        self.autoPlaylistBtn.clicked.connect(self.autoplaylist)
        self.browserBtn.clicked.connect(self.browser)
        self.featuredBtn.clicked.connect(self.featured)
        self.infoBtn.clicked.connect(self.info)
        self.searchInput.setCursorPosition(10)
        self.searchInput.textChanged.connect(self.updateOptions)
        self.searchInput.editingFinished.connect(self.finished)
        self.contentFrame.setGeometry(0, 0, 10, 10)
        self.contentFrame.hide()
        self.searchBar.setGeometry(self.searchBar.pos().x(), self.searchBar.pos().y(), self.width(), self.searchBar.height())
        self.centralWidget().setStyleSheet("QWidget#centralwidget {border-image:url(alternatives/sheet-music-texture.png) 0 0 stretch stretch;}")
        self.actionUbuntu.triggered.connect(self.ubuntu)
        self.actionCandy.triggered.connect(self.candy)
        self.searchFrame.hide()
        self.scoreWindow.hide()
        self.multistndBtn.hide()
        self.popoutBtn.hide()
        self.popoutBtn.clicked.connect(self.onPopoutClicked)
        #self.scoreWebView.hide()
        self.playlistTable.hide()
        self.playlistTable.itemDoubleClicked.connect(self.onPlaylistItemClicked)

        self.actionRefresh_Collection.triggered.connect(self.qApp.updateDb)
        self.actionNew_Collection.triggered.connect(self.newCollection)
        self.actionImport.triggered.connect(self.qApp.importWindow)
        if platform == "win32":
            self.applyTheme()


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


    def candy(self):
        """
        callback for the action to change theme to candy
        :return:
        """
        self.theme = "candy"
        self.qApp.updateTheme("candy")
        self.applyTheme()

    def ubuntu(self):
        """
        callback for the action to change theme to ubuntu
        :return:
        """
        self.theme = "ubuntu"
        self.qApp.updateTheme("ubuntu")
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

    def onQueryReturned(self, results):
        """
        callback which gets called when the query has been handled by the parent application
        :param results:  nested list of results to put into the tree
        :return:
        """



        self.widgets["search"].load(results)
        self.widgets["search"].show()
        self.searchFrame.show()



    def finished(self):
        """
        callback for when a user has finished entering text in the search bar
        :return:
        """
        widget = self.focusWidget()
        print((self.searchInput.text() == "" or self.searchInput.text() == " "))
        print(self.widgets["search"].topLevelItemCount() == 0)
        if (self.searchInput.text() == "" or self.searchInput.text() == " ") or widget.objectName() != "treeWidget":
            try:
                self.searchFrame.hide()
            except:
                print("we're done here. gbye")

    # methods which handle playlists
    def loadPlaylist(self, playlist_title, playlist_to_load, length):
        """
        method which gets called by either of the playlist widgets when a user clicks a playlist
        :param playlist_title: title of the playlist
        :param playlist_to_load: list of files in the playlist
        :param length: length of the playlist items
        :return:
        """
        self.scoreWindow.hide()
        self.playlistTable.setRowCount(length)
        file_data = self.qApp.getPlaylistFileInfo(playlist_to_load)
        data_items = self.setUpDataItems(playlist_to_load, file_data, 0, len(file_data))
        for i in range(len(data_items)):
            for j in range(len(data_items[i])):
                self.playlistTable.setItem(i, j, data_items[i][j])
        self.titleOfPiece.setText(playlist_title)
        self.titleOfPiece.adjustSize()
        self.titleOfPiece.show()
        self.playlistTable.show()
        self.playlistTable.lower()
        for i in range(10):
            self.playlistTable.setColumnWidth(i, self.playlistTable.width()/9)
        self.playlist = playlist_title
        self.resizeCenterWidget(self.playlistTable)

    def setUpDataItems(self, playlist_fnames, playlist_data, start_index, end_index):
        items = []
        for i in range(start_index, end_index):
            file = playlist_data[i]
            row = []
            item = QtGui.QTableWidgetItem(file["title"])
            item.setData(32, file["filename"])
            item.setData(3, i)
            item.setData(4, playlist_fnames)
            row.append(item)
            if "composer" in file:
                item = QtGui.QTableWidgetItem(file["composer"])
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

            if "lyricist" in file:
                item = QtGui.QTableWidgetItem(file["lyricist"])
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

            if "instruments" in file:
                item = QtGui.QTableWidgetItem(", ".join([data["name"] for data in file["instruments"]]))
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
            item = QtGui.QTableWidgetItem(file["filename"])
            item.setData(32, file["filename"])
            item.setData(3, i)
            item.setData(4, playlist_fnames)
            row.append(item)
            if "clefs" in file:
                result = ""
                for instrument in file["clefs"]:
                    result += ", ".join(file["clefs"][instrument])
                item = QtGui.QTableWidgetItem(result)
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                item.setData(32, file["filename"])
                row.append(item)

            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(32, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            if "keys" in file:
                result = ""
                for instrument in file["keys"]:
                    result += ", ".join(file["keys"][instrument])
                item = QtGui.QTableWidgetItem(result)
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

            if "tempos" in file:
                item = QtGui.QTableWidgetItem(", ".join(file["tempos"]))
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

            if "time_signatures" in file:
                item = QtGui.QTableWidgetItem(", ".join(file["time_signatures"]))
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
        pass

    def onPopoutClicked(self):
        os.system("open "+self.pdf_loaded)


    # methods to handle pieces
    def onPieceLoaded(self, filename, split_file):
        """
        callback which is called when the parent application has finished working on an xml file
        :param filename: the fully qualified filename location including folder
        :param split_file: the filename with no folder location
        :return:
        """
        self.pdf_loaded = filename
        file_to_load = split_file.split(".")[0]+".xml"
        self.current_piece = file_to_load
        #self.showToolbarBtns()
        #self.loadPieceData(file_to_load)
        self.loadPdfToGraphicsWidget(filename)
        #self.loadPdfToWebWidget(filename)
        self.titleOfPiece.setText(file_to_load)
        self.titleOfPiece.adjustSize()
        self.titleOfPiece.repaint()
        self.resizeCenterWidget(self.scoreWindow)
        self.scoreWindow.show()
        self.scoreWindow.lower()
        self.multistndBtn.show()
        self.popoutBtn.show()
        #self.loadFeaturedIn(file_to_load)
        #self.playlistViewer.hide()
        #self.pieceInfoWidget.show()

    def loadPdfToGraphicsWidget(self, filename):
        """
        sets up the graphics view with pairs of pages
        :param filename: pdf file to load
        :return:
        """

        scene = QtGui.QGraphicsScene()
        scene.setBackgroundBrush(QtGui.QColor('transparent'))
        layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        layout.setContentsMargins(0,0,0,0)
        doc = Poppler.Document.load(filename)
        doc.setRenderHint(Poppler.Document.Antialiasing)
        doc.setRenderHint(Poppler.Document.TextAntialiasing)


        pageNum = doc.numPages()
        number = 0
        scenes = []
        pairings = []
        pages = []
        images = []
        pixmaps = []
        containers = []
        labels = []

        while number < pageNum:
            scenes.append(QtGui.QGraphicsScene())
            pairings.append(QtGui.QGraphicsLinearLayout(QtCore.Qt.Horizontal))
            pages.append(doc.page(number))
            images.append(pages[number].renderToImage(100, 100))
            pixmaps.append(QtGui.QPixmap.fromImage(images[number]))
            containers.append(QtGui.QLabel())
            containers[number].setFixedWidth(self.scoreWindow.width()/2)
            containers[number].setFixedHeight(pages[number].pageSize().height())
            #containers[number].setFixedSize(pages[number].pageSize())
            containers[number].setStyleSheet("pages[number] { background-color : transparent}")
            containers[number].setContentsMargins(0, 0, 0, 0)
            containers[number].setScaledContents(True)
            containers[number].setPixmap(pixmaps[number])
            labels.append(scenes[number].addWidget(containers[number]))
            pairings[number].addItem(labels[number])
            number += 1
            if number < pageNum:
                pages.append(doc.page(number))
                images.append(pages[number].renderToImage(100, 100))
                pixmaps.append(QtGui.QPixmap.fromImage(images[number]))
                containers.append(QtGui.QLabel())
                containers[number].setFixedWidth(self.scoreWindow.width()/2)
                containers[number].setFixedHeight(pages[number].pageSize().height())
                #containers[number].setFixedSize(pages[number].pageSize())
                containers[number].setStyleSheet("pages[number] { background-color : transparent}")
                containers[number].setContentsMargins(0, 0, 0, 0)
                containers[number].setScaledContents(True)
                containers[number].setPixmap(pixmaps[number])
                labels.append(scenes[number-1].addWidget(containers[number]))
                pairings[number-1].addItem(labels[number])

            else:
                containers.append(QtGui.QLabel())
                containers[number].setFixedSize(pages[number-1].pageSize())
                containers[number].setStyleSheet("pages[number] { background-color : transparent}")
                containers[number].setContentsMargins(0, 0, 0, 0)
                containers[number].setScaledContents(True)
                pixmaps.append(QtGui.QPixmap())
                containers[number].setPixmap(pixmaps[number])
                labels.append(scenes[number-1].addWidget(containers[number]))
                pairings[number-1].addItem(labels[number])
            layout.addItem(pairings[number-1])
            number += 1

        # use this to test that the layout works for more than 2 pages
        # while number < 3:
        #     scenes.append(QtGui.QGraphicsScene())
        #     pairings.append(QtGui.QGraphicsLinearLayout(QtCore.Qt.Horizontal))
        #     containers.append(QtGui.QLabel())
        #     containers[number].setFixedSize(pages[-1].pageSize())
        #     containers[number].setStyleSheet("pages[number] { background-color : transparent}")
        #     containers[number].setContentsMargins(0, 0, 0, 0)
        #     containers[number].setScaledContents(True)
        #     pixmaps.append(QtGui.QPixmap())
        #     containers[number].setPixmap(pixmaps[number])
        #     labels.append(scenes[-1].addWidget(containers[number]))
        #     pairings[-1].addItem(labels[number])
        #     layout.addItem(pairings[-1])
        #     number += 1

        graphicsWidget = QtGui.QGraphicsWidget()
        graphicsWidget.setLayout(layout)
        scene.addItem(graphicsWidget)
        self.scoreWindow.setScene(scene)

    def loadPdfToWebWidget(self, filename):
        # self.scoreWebView.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        # self.scoreWebView.show()
        # self.scoreWebView.settings().setAttribute(QtWebKit.QWebSettings.PluginsEnabled, True)
        # self.scoreWebView.settings().setAttribute(QtWebKit.QWebSettings.PrivateBrowsingEnabled, True)
        # self.scoreWebView.settings().setAttribute(QtWebKit.QWebSettings.LocalContentCanAccessRemoteUrls, True)
        # self.scoreWebView.loadFinished.connect(self._loadfinished)
        f = QtCore.QUrl().fromLocalFile(filename)
        print(f)
        # self.scoreWebView.load(QtCore.QUrl("http://www.calvin.edu/~dsc8/documents/Podcasting-in-Education-Winter-2005.pdf"))

    def _loadfinished(self):
        print("complete")
        # self.scoreWebView.repaint()
        pass

    # callbacks for the buttons in the side menu
    def scorebook(self):
        if self.loaded != "scorebook":
            self.loadFrame("scorebook")
        else:
            self.unloadFrame("scorebook")

    def myplaylist(self):
        if self.loaded != "myplaylist":
            self.loadFrame("myplaylist")
        else:
            self.unloadFrame("myplaylist")

    def autoplaylist(self):
        if self.loaded != "autoplaylist":
            self.loadFrame("autoplaylist")
        else:
            self.unloadFrame("autoplaylist")

    def browser(self):
        if self.loaded != "browser":
            self.loadFrame("browser")
        else:
            self.unloadFrame("browser")

    def info(self):
        if self.loaded != "info":
            self.loadFrame("info")
        else:
            self.unloadFrame("info")

    def featured(self):
        if self.loaded != "featured":
            self.loadFrame("featured")
        else:
            self.unloadFrame("featured")



    # methods to handle loading frames
    def loadFrame(self, child, ypos=72):
        """
        method which fetches the appropriate widget, puts it in the content frame and starts an animation to pull the frame out
        :param child: the name of the widget to load
        :param ypos: position to place the widget on the y plane
        :return:
        """
        position = self.contentFrame.pos()
        widget = self.widgets[child](self)
        endx = self.buttonFrame.width()-1
        endy = position.y()
        endwidth = widget.width()
        layout = self.contentFrame.layout()

        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widge = item.widget()
                if widge is not None:
                    widge.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(layout)

        layout = QtGui.QHBoxLayout()
        layout.setSpacing(0)
        layout.setMargin(0)
        layout.addWidget(widget)
        fob = open(os.path.join(get_base_dir(True), "themes", "basic_widget.qss"), 'r')
        lines = fob.readlines()
        fob.close()
        stylesheet = []
        if child in self.colors:
            background = "QFrame#contentFrame { background:"+self.colors[child]+";}"
            stylesheet.append(background)

        stylesheet.extend(lines)

        if not self.contentFrame.layout():
            self.contentFrame.setLayout(layout)
        self.contentFrame.setStyleSheet(parseStyle(stylesheet))
        self.contentFrame.show()
        self.contentFrame.lower()
        self.scoreWindow.lower()
        self.playlistTable.lower()
        animation = QtCore.QPropertyAnimation(self.contentFrame, "geometry")
        animation.setDuration(200)
        animation.setStartValue(QtCore.QRect(0, ypos, self.buttonFrame.width(), self.buttonFrame.height()))
        animation.setEndValue(QtCore.QRect(endx, ypos, endwidth, self.buttonFrame.height()))
        animation.start()
        self.animation = animation
        self.loaded = child

    def unloadFrame(self, child):
        """
        method which handles the animation of a frame in terms of putting it back where it started
        :param child: name of the frame to onload. No longer really used
        :return:
        """
        position = self.contentFrame.pos()
        endx = 0
        endy = position.y()
        endwidth = self.buttonFrame.width()
        #self.contentFrame.lower()

        animation = QtCore.QPropertyAnimation(self.contentFrame, "geometry")
        animation.setDuration(200)
        animation.setStartValue(QtCore.QRect(position.x(), position.y(), self.contentFrame.width(), self.contentFrame.height()))
        animation.setEndValue(QtCore.QRect(endx, endy, endwidth, self.contentFrame.height()))
        animation.start()
        self.animation = animation
        self.loaded = ""

    def unloadSearch(self):
        self.searchFrame.hide()

    # callbacks for actions
    def newCollection(self):
        self.qApp.folder = ""
        self.qApp.setup_startup()
        self.close()

    def getCreatedPlaylists(self, slot=None):
        async = qt_threading.mythread(self, self.manager.getPlaylistsFromPlaylistTable, ())
        QtCore.QObject.connect(async, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        async.run()

    def getPlaylists(self, select_method="all", slot=None):
        async = qt_threading.mythread(self, self.manager.getPlaylists, (select_method,))
        QtCore.QObject.connect(async, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        async.run()



