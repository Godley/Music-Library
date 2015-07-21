from PyQt4 import uic, QtCore, QtGui
from implementation.primaries.GUI.helpers import get_base_dir
import os

class Window(QtGui.QWidget):
    def __init__(self, parent, file, title):
        QtGui.QWidget.__init__(self)
        self.main_window = parent
        self.application = self.main_window.qApp
        design = os.path.join(get_base_dir(return_this_dir=True), "designer_files", file)
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


    def loadPiece(self, current_item):
        file_to_load = current_item.data(32)
        self.application.loadFile(file_to_load)
        self.main_window.unloadFrame("scorebook")


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

    def loadPlaylist(self, current_item):
        #self.scoreWindow.hide()
        playlist_to_load = current_item.data(1)
        length = len(playlist_to_load)
        playlist_title = current_item.data(3)
        self.main_window.loadPlaylist(playlist_title, playlist_to_load, length)
        self.main_window.unloadFrame(self.name)


class MyPlaylists(PlaylistWidget):
    name = "myplaylist"
    def __init__(self, parent):
        PlaylistWidget.__init__(self, parent, "MyPlaylists.ui", "My Playlists")
        self.deleteBtn.hide()
        self.listWidget.itemClicked.connect(self.deleteBtn.show)
        self.addBtn.clicked.connect(self.addClicked)
        self.deleteBtn.clicked.connect(self.delete)

    def addClicked(self):
        self.application.createNewPlaylist()
        self.main_window.unloadFrame("myplaylist")

    def delete(self):
        items = self.listWidget.selectedItems()
        self.application.deletePlaylists([item.data(3) for item in items])



class AutoPlaylists(PlaylistWidget):
    name = "autoplaylist"
    def __init__(self, parent):
        PlaylistWidget.__init__(self, parent, "BasicListWidgetWithSort.ui", "Auto Playlists", data_set="auto")
        options = ["all", "time signatures","keys","clefs","instruments","tempos"]
        self.comboBox.addItems(options)
        self.comboBox.currentIndexChanged.connect(self.sortMethodChanged)

    def sortMethodChanged(self):
        sortMethod = self.comboBox.currentText()
        self.loadPlaylists(select_method=sortMethod)

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
        self.loadInfo()
    
    def loadInfo(self):
        if self.main_window.current_piece != "":
            self.listWidget.clear()
            data = self.application.getFileInfo(self.main_window.current_piece)[0]

            datastring = "title: "+data["title"]
            title = QtGui.QListWidgetItem(datastring)
            self.listWidget.addItem(title)
            if "composer" in data and data["composer"] != -1:
                datastring = "composer: "+data["composer"]
                composer = QtGui.QListWidgetItem(datastring)
                self.listWidget.addItem(composer)
            if "lyricist" in data and data["lyricist"] != -1:
                datastring = "lyricist: "+data["lyricist"]
                lyricist = QtGui.QListWidgetItem(datastring)
                self.listWidget.addItem(lyricist)
            if "instruments" in data:
                datastring = "instruments: "+", ".join([d["name"] for d in data["instruments"]])
                instruments = QtGui.QListWidgetItem(datastring)
                self.listWidget.addItem(instruments)
            if "clefs" in data:
                datastring = "clefs: "
                clef_list = []
                for instrument in data["clefs"]:
                    for clef in data["clefs"][instrument]:
                        if clef not in clef_list:
                            clef_list.append(clef)
                datastring += ", ".join(clef_list)
                clefs = QtGui.QListWidgetItem(datastring)
                self.listWidget.addItem(clefs)
            if "keys" in data:
                datastring = "keys: "
                key_list = []
                for instrument in data["keys"]:
                    for key in data["keys"][instrument]:
                        if key_list not in key_list:
                            key_list.append(key)
                datastring += ", ".join(key_list)
                keys = QtGui.QListWidgetItem(datastring)
                self.listWidget.addItem(keys)

            if "tempos" in data:
                datastring = "tempos: "
                tempo_list = []
                for tempo in data["tempos"]:
                    datastring += tempo
                    datastring += ", "
                tempos = QtGui.QListWidgetItem(datastring)
                self.listWidget.addItem(tempos)

            if "time_signatures" in data:
                datastring = "time signatures: "
                tempo_list = []
                for tempo in data["time_signatures"]:
                    datastring += tempo
                    datastring += ", "
                tempos = QtGui.QListWidgetItem(datastring)
                self.listWidget.addItem(tempos)

            self.listWidget.show()

class FeaturedIn(PlaylistWidget):
    name = "featured"
    def __init__(self, parent):
        PlaylistWidget.__init__(self, parent, "BasicListWidget.ui", "Featured In...", data_set="featured")
    
    def loadPlaylists(self):
        if self.main_window.current_piece != "":
            data = self.application.loadUserPlaylistsForAGivenFile(self.main_window.current_piece)
            self.listWidget.clear()
            for item in data:
                widget = QtGui.QListWidgetItem(item)
                widget.setData(1, data[item])
                widget.setData(3, item)
                self.listWidget.addItem(widget)
            self.listWidget.show()

class PlaylistBrowser(Window):
    def __init__(self, parent):
        Window.__init__(self, parent, "BasicTableWidget.ui", "Playlist Browser")
        self.playlist = self.main_window.playlist
        self.index = self.main_window.index
        if self.playlist is not None and self.index is not None:
            self.load()
        self.tableWidget.itemDoubleClicked.connect(self.clicked)
        
    
    def load(self):
        data = self.application.getPlaylistFileInfo(self.playlist)
        if self.tableWidget.rowCount() != 0:
            self.tableWidget.clear()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(['Title', 'Composer', 'Filename'])
        for i in range(3):
            self.tableWidget.setColumnWidth(i, self.tableWidget.width()/3)
        self.tableWidget.setRowCount(len(data))
        for i in range(len(data)):
            if "composer" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["composer"])
                item.setData(32,data[i]["filename"])
                self.tableWidget.setItem(i, 1, item)
            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(32, data[i]["filename"])
                self.tableWidget.setItem(i, 1, item)

            if "title" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["title"])
                item.setData(32,data[i]["filename"])
                self.tableWidget.setItem(i, 0, item)
            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(32, data[i]["filename"])
                self.tableWidget.setItem(i, 0, item)

            if "filename" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["filename"])
                item.setData(32, data[i]["filename"])
                self.tableWidget.setItem(i, 2, item)
            else:
                item = QtGui.QTableWidgetItem("")
                item.setData(32, data[i]["filename"])
                self.tableWidget.setItem(i, 2, item)

        self.tableWidget.selectRow(self.index)
        self.tableWidget.show()

    def clicked(self, current_item):
        file_to_load = current_item.data(32)
        self.application.loadFile(file_to_load)
        self.main_window.unloadFrame("browser")

class SearchTree(QtGui.QTreeWidget):
    def __init__(self, parent):
        QtGui.QTreeWidget.__init__(self)
        self.main_window = parent
        self.application = self.main_window.qApp
        design = os.path.join(get_base_dir(return_this_dir=True), "designer_files", "treeWidget.ui")
        uic.loadUi(design, self)
        self.treeWidget.itemDoubleClicked.connect(self.clicked)

    def leaveEvent(self, QFocusEvent):
        if not self.hasFocus():
            self.main_window.unloadSearch()
        QFocusEvent.accept()

    def clicked(self, current_item):
        self.main_window.unloadFrame("searchtree")
        file_to_load = current_item.data(0,32)
        self.application.loadFile(file_to_load)

    def load(self, results):
        root = self.treeWidget.invisibleRootItem()
        child_count = root.childCount()
        children = [(i, root.child(i).text(0)) for i in range(child_count)]
        names = [child[1] for child in children]
        for location_type in results:
            item = QtGui.QTreeWidgetItem(location_type)
            item.setData(0,0,location_type)
            if location_type in names:
                index = [child[0] for child in children if child[1] == location_type]
                item = root.child(index[0])
                for i in range(item.childCount()):
                    child = item.child(i)
                    item.removeChild(child)

            else:
                self.treeWidget.addTopLevelItem(item)
            for key in results[location_type]:
                sub_item = QtGui.QTreeWidgetItem(key)
                sub_item.setData(0,0,key)
                item.addChild(sub_item)
                for file in results[location_type][key]:
                    fitem = QtGui.QTreeWidgetItem(file[0])
                    fitem.setData(0, 0, file[0])
                    fitem.setData(0, 32, file[1])
                    sub_item.addChild(fitem)

    def quack(self):
        print("quack")

