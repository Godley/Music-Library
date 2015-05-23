from PyQt4 import QtGui, QtCore, uic
import sip
from implementation.primaries.GUI.helper import get_base_dir
import os, time, copy
from implementation.primaries.GUI.alt_python.parseStyle import parseStyle
from implementation.primaries.GUI.alt_python import Widgets
from popplerqt4 import Poppler

class MainWindow(QtGui.QMainWindow):
    widgets = {}
    frames = {}
    colors = {}
    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)
        self.qApp = app
        self.loaded = ""
        self.theme = "ubuntu"
        self.current_piece = ""

    def resizeEvent(self, QResizeEvent):
        if hasattr(self, "scoreWindow"):
            if not self.scoreWindow.isHidden():
                self.resizeScoreWindow()
        if hasattr(self, "searchBar"):
            self.resizeSearchbar()
        QResizeEvent.accept()

    def resizeScoreWindow(self):
        score_position = self.scoreWindow.pos()
        score_width = self.width() - self.buttonFrame.width()
        score_height = self.height() - self.searchBar.height()
        self.scoreWindow.setGeometry(score_position.x(), score_position.y(), score_width, score_height)

    def resizeSearchbar(self):
        search_position = self.searchBar.pos()
        search_width = self.width()
        search_height = self.searchBar.height()
        self.searchBar.setGeometry(search_position.x(), search_position.y(), search_width, search_height)

    def applyStyle(self):
        stylesheet = os.path.join(get_base_dir(True), "themes", self.theme+".qss")
        fob = open(stylesheet, 'r')
        lines = fob.readlines()
        fob.close()
        self.setStyleSheet(parseStyle(lines))

    def load(self):
        file = os.path.join(get_base_dir(True), "alternatives", "MainWindow.ui")
        uic.loadUi(file, self)
        self.applyStyle()
        self.setGeometry(0, 0, self.width(), self.height())
        self.widgets["scorebook"] = Widgets.Scorebook
        self.colors["scorebook"] = "rgba(170, 255, 8, 100)"
        self.colors["myplaylist"] = "rgba(248, 213, 17, 100)"
        self.colors["autoplaylist"] = "rgba(235, 25, 39, 100)"
        self.colors["info"] = "rgba(253, 127, 60, 100)"
        self.widgets["myplaylist"] = Widgets.MyPlaylists
        self.widgets["autoplaylist"] = Widgets.AutoPlaylists
        self.widgets["info"] = Widgets.PieceInfo
        self.widgets["featured"] = Widgets.FeaturedIn
        self.widgets["browser"] = Widgets.PlaylistBrowser
        self.scorebookBtn.clicked.connect(self.scorebook)
        self.myPlaylistBtn.clicked.connect(self.myplaylist)
        self.autoPlaylistBtn.clicked.connect(self.autoplaylist)
        self.browserBtn.clicked.connect(self.browser)
        self.featuredBtn.clicked.connect(self.featured)
        self.infoBtn.clicked.connect(self.info)
        self.lineEdit.setCursorPosition(10)
        self.lineEdit.textChanged.connect(self.searchbox)
        self.lineEdit.editingFinished.connect(self.finished)
        self.contentFrame.setGeometry(0, 0, 10, 10)
        self.contentFrame.hide()
        self.searchBar.setGeometry(self.searchBar.pos().x(), self.searchBar.pos().y(), self.width(), self.searchBar.height())
        self.centralWidget().setStyleSheet("QWidget#centralwidget {border-image:url(alternatives/sheet-music-texture.png) 0 0 stretch stretch;}")
        self.actionUbuntu.triggered.connect(self.ubuntu)
        self.actionCandy.triggered.connect(self.candy)
        self.menuBar().addMenu("File")
        self.searchFrame.hide()
        self.scoreWindow.hide()

    def candy(self):
        self.theme = "candy"
        self.applyStyle()

    def ubuntu(self):
        self.theme = "ubuntu"
        self.applyStyle()

    def searchbox(self, text):
        self.searchFrame.show()

    def finished(self):
        self.searchFrame.hide()


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


    # def paintEvent(self, paint_event):
    #     QtGui.QMainWindow.paintEvent(self, paint_event)
    #     pixmap = QtGui.QPixmap()
    #     pixmap.load("alternatives/sheet-music-texture.png")
    #     paint = QtGui.QPainter(self)
    #     widWidth = self.centralWidget().width()
    #     widheight = self.centralWidget().height()
    #     pixmap = pixmap.scaled(widWidth, widheight, QtCore.Qt.KeepAspectRatioByExpanding)
    #     paint.drawPixmap(0, 0, pixmap)

    def onPieceLoaded(self, filename, split_file):
        """
        :param filename: the fully qualified filename location including folder
        :param split_file: the filename with no folder location
        :return:
        """
        file_to_load = split_file.split(".")[0]+".xml"
        self.current_piece = file_to_load
        #self.showToolbarBtns()
        #self.loadPieceData(file_to_load)
        self.pdf_view(filename)
        self.titleOfPiece.setText(file_to_load)
        self.titleOfPiece.adjustSize()
        self.titleOfPiece.repaint()
        self.resizeScoreWindow()
        self.scoreWindow.show()
        self.scoreWindow.lower()
        #self.loadFeaturedIn(file_to_load)
        #self.playlistViewer.hide()
        #self.pieceInfoWidget.show()

    def pdf_view(self, filename):
        """Return a Scrollarea showing the first page of the specified PDF file."""

        scene = QtGui.QGraphicsScene()
        scene.setBackgroundBrush(QtGui.QColor('darkGray'))
        layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        doc = Poppler.Document.load(filename)
        doc.setRenderHint(Poppler.Document.Antialiasing)
        doc.setRenderHint(Poppler.Document.TextAntialiasing)


        pageNum = doc.numPages()
        for number in range(pageNum):
            page = doc.page(number)
            image = page.renderToImage(100, 100)
            pixmap = QtGui.QPixmap.fromImage(image)
            container = QtGui.QLabel()
            container.setFixedSize(page.pageSize())
            container.setStyleSheet("Page { background-color : transparent}")
            container.setContentsMargins(0, 0, 0, 0)
            container.setScaledContents(True)
            container.setPixmap(pixmap)
            label = scene.addWidget(container)
            opacity = QtGui.QGraphicsOpacityEffect(self)
            opacity.setOpacity(0.5)
            label.setGraphicsEffect(opacity)
            layout.addItem(label)

        graphicsWidget = QtGui.QGraphicsWidget()
        graphicsWidget.setLayout(layout)
        scene.addItem(graphicsWidget)
        #self.view = View(scene)
        #self.scoreWindow.scale(1,1)
        #self.scoreWindow.scale(1.4,1.4)
        self.scoreWindow.setScene(scene)

    def loadFrame(self, child, ypos=72):
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
        animation = QtCore.QPropertyAnimation(self.contentFrame, "geometry")
        animation.setDuration(200)
        animation.setStartValue(QtCore.QRect(0, ypos, self.buttonFrame.width(), self.buttonFrame.height()))
        animation.setEndValue(QtCore.QRect(endx, ypos, endwidth, self.buttonFrame.height()))
        animation.start()
        self.animation = animation
        self.loaded = child

    def unloadFrame(self, child):
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


