from PyQt4 import uic, QtCore, QtGui
from implementation.primaries.GUI.helper import get_base_dir
import os

class Window(QtGui.QWidget):
    def __init__(self, parent, file, title):
        QtGui.QWidget.__init__(self)
        self.app = parent
        design = os.path.join(get_base_dir(return_this_dir=True), "alternatives", file)
        uic.loadUi(design, self)
        try:
            self.title.setText(title)
        except:
            pass



class Scorebook(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicListWidgetWithSort.ui", "Scorebook")
        self.application = self.app.qApp
        self.setGeometry(0, 0, self.width(), self.height())
        self.listWidget.itemDoubleClicked.connect(self.loadPiece)
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox.currentIndexChanged.connect(self.onSortChange)
        options = ["title","composer","lyricist"]
        self.comboBox.addItems(options)
        self.onSortChange()

    def onSortChange(self):
        sort_method = self.comboBox.currentText()
        self.app.qApp.loadPieces(method=sort_method, slot=self.onScoresReady)
        self.comboBox.show()

    def onScoresReady(self, pieces):
        self.listWidget.clear()
        for i in pieces:
            item = QtGui.QListWidgetItem(i[0])
            item.setData(32, i[1])
            self.listWidget.addItem(item)


    def loadPiece(self):
        pass


class MyPlaylists(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "MyPlaylists.ui", "My Playlists")
        self.deleteBtn.hide()

class AutoPlaylists(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicListWidgetWithSort.ui", "Auto-Playlists")

class PieceInfo(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicListWidget.ui", "Piece Information")

class FeaturedIn(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicListWidget.ui", "Featured In...")

class PlaylistBrowser(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicTableWidget.ui", "Playlist Browser")



