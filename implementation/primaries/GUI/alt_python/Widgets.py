from PyQt4 import uic, QtCore, QtGui
from implementation.primaries.GUI.helper import get_base_dir
import os

class Window(QtGui.QWidget):
    def __init__(self, parent, file, title):
        QtGui.QWidget.__init__(self)
        self.main_window = parent
        self.application = self.main_window.qApp
        design = os.path.join(get_base_dir(return_this_dir=True), "alternatives", file)
        uic.loadUi(design, self)
        try:
            self.title.setText(title)
        except:
            pass



class Scorebook(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicListWidgetWithSort.ui", "Scorebook")
        self.setGeometry(0, 0, self.width(), self.height())
        self.listWidget.itemDoubleClicked.connect(self.loadPiece)
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox.currentIndexChanged.connect(self.onSortChange)
        options = ["title","composer","lyricist"]
        self.comboBox.addItems(options)
        self.onSortChange()

    def onSortChange(self):
        sort_method = self.comboBox.currentText()
        self.application.loadPieces(method=sort_method, slot=self.onScoresReady)
        self.comboBox.show()

    def onScoresReady(self, pieces):
        self.listWidget.clear()
        for i in pieces:
            item = QtGui.QListWidgetItem(i[0])
            item.setData(32, i[1])
            self.listWidget.addItem(item)


    def loadPiece(self):
        pass


class PlaylistWidget(Window):
    def __init__(self, parent, file, title, data_set="mine"):
        Window.__init__(self, parent, file, title)
        self.listWidget.itemDoubleClicked.connect(self.loadPlaylist)
        self.data_set = data_set
        self.loadPlaylists()

    def onPlaylistsReady(self, myPlaylists):
        self.listWidget.clear()
        for entry in myPlaylists:
            item = QtGui.QListWidgetItem(entry)
            item.setData(1, myPlaylists[entry])
            item.setData(3, entry)
            self.listWidget.addItem(item)
        self.listWidget.show()

    def loadPlaylists(self, select_method="all"):
        if self.data_set == "auto":
            self.application.getPlaylists(select_method=select_method, slot=self.onPlaylistsReady)
        else:
            self.application.getCreatedPlaylists(slot=self.onPlaylistsReady)


    def load_data(self):
        pass

    def loadPlaylist(self):
        pass


class MyPlaylists(PlaylistWidget):
    def __init__(self, parent):
        PlaylistWidget.__init__(self, parent, "MyPlaylists.ui", "My Playlists")
        self.deleteBtn.hide()
        self.listWidget.itemClicked.connect(self.deleteBtn.show)

    def loadPlaylist(self):
        pass

class AutoPlaylists(PlaylistWidget):
    def __init__(self, parent):
        PlaylistWidget.__init__(self, parent, "MyPlaylists.ui", "Auto Playlists", data_set="auto")

    def onPlaylistsReady(self, playlist_summaries):
        self.listWidget.clear()
        for i in playlist_summaries:
            item = QtGui.QListWidgetItem(i)
            self.listWidget.addItem(item)
            for j in playlist_summaries[i]:
                item = QtGui.QListWidgetItem(j)
                item.setData(1, playlist_summaries[i][j])
                item.setData(3, i+j)
                self.listWidget.addItem(item)
        self.listWidget.show()

class PieceInfo(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicListWidget.ui", "Piece Information")

class FeaturedIn(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicListWidget.ui", "Featured In...")

class PlaylistBrowser(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicTableWidget.ui", "Playlist Browser")



