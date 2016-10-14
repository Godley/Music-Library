from PyQt4 import uic, QtCore, QtGui
from PyQt4.QtCore import QObject, QThread, pyqtSignal, SIGNAL
from implementation.primaries.GUI.helpers import get_base_dir, merge_clefs_and_keys, merge_instruments, fit_columns_to_widget
import os


class Window(QtGui.QWidget):

    def __init__(self, parent, file, title, design_folder):
        QtGui.QWidget.__init__(self)
        self.main_window = parent
        self.application = self.main_window.qApp
        design = os.path.join(design_folder, file)
        uic.loadUi(design, self)
        self.title_str = title
        try:
            self.title.setText(title)
        except:
            pass

    def onWidgetReady(self):
        pass

    def loadPiece(self, current_item):
        file_to_load = current_item.data(32)
        self.application.loadFile(file_to_load)
        self.main_window.unloadFrame(self.title_str.lower())

    def emit_signal(self, data, slot):
        self.emit(SIGNAL("widget_signal(PyQt_PyObject, PyQt_PyObject,PyQt_PyObject)"),
                         data, slot, self.title_str)


class Scorebook(Window):

    def __init__(self, parent, design_folder):
        Window.__init__(
            self,
            parent,
            "BasicListWidgetWithSort.ui",
            "Scorebook",
            design_folder)
        self.setGeometry(0, 0, self.width(), self.height())
        self.listWidget.itemDoubleClicked.connect(self.loadPiece)
        self.listWidget.setFocusPolicy(QtCore.Qt.NoFocus)
        self.comboBox.currentIndexChanged.connect(self.onSortChange)
        options = ["title", "composer", "lyricist"]
        self.comboBox.addItems(options)

    def onWidgetReady(self):
        self.onSortChange()

    def onSortChange(self):
        sort_method = self.comboBox.currentText()
        self.emit_signal(sort_method, self.onScoresReady)
        self.comboBox.show()

    def onScoresReady(self, pieces):
        self.listWidget.clear()
        for i in pieces:
            item = QtGui.QListWidgetItem(i[0])
            item.setData(32, i[1])
            self.listWidget.addItem(item)


class PlaylistWidget(Window):

    def __init__(self, parent, file, title, design_folder, data_set="mine"):
        Window.__init__(self, parent, file, title, design_folder)
        self.listWidget.itemDoubleClicked.connect(self.loadPlaylist)
        self.data_set = data_set

    def onWidgetReady(self):
        self.loadPlaylists()

    def onPlaylistsReady(self, myPlaylists):
        self.listWidget.clear()
        self.create_widgets(myPlaylists)
        self.listWidget.show()

    def create_widgets(self, data):
        for entry in data:
            item = QtGui.QListWidgetItem(entry)
            item.setData(1, data[entry])
            item.setData(3, entry)
            self.listWidget.addItem(item)

    def loadPlaylists(self, select_method="all"):
        self.emit_signal(select_method, self.onPlaylistsReady)

    def load_data(self):
        pass

    def loadPlaylist(self, current_item):
        # self.scoreWindow.hide()
        playlist_to_load = current_item.data(1)
        length = len(playlist_to_load)
        playlist_title = current_item.data(3)
        self.main_window.loadPlaylist(playlist_title, playlist_to_load, length)
        self.main_window.unloadFrame(self.name)


class MyPlaylists(PlaylistWidget):
    name = "myplaylist"

    def __init__(self, parent, design_folder):
        PlaylistWidget.__init__(
            self,
            parent,
            "MyPlaylists.ui",
            self.name,
            design_folder)
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

    def __init__(self, parent, design_folder):
        PlaylistWidget.__init__(
            self,
            parent,
            "BasicListWidgetWithSort.ui",
            self.name,
            design_folder,
            data_set="auto")
        options = ["all", "time signatures", "keys",
                   "clefs", "instruments", "tempos"]
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
                item.setData(3, i + j)
                self.listWidget.addItem(item)
        self.listWidget.show()


class PieceInfo(Window):

    def __init__(self, parent, design_folder):
        Window.__init__(
            self,
            parent,
            "BasicListWidget.ui",
            "info",
            design_folder)

    def onWidgetReady(self):
        self.loadInfo()

    def loadInfo(self):
        if self.main_window.current_piece != "":
            self.listWidget.clear()
            data = self.application.getFileInfo(
                self.main_window.current_piece)[0]

            datastring = "title: " + data["title"]
            title = QtGui.QListWidgetItem(datastring)
            self.listWidget.addItem(title)
            keys = (
                "composer",
                "lyricist",
                "instruments",
                "clefs",
                "keys",
                "tempos",
                "time_signatures")

            alternate_methods = {"instruments": merge_instruments,
                                 "clefs": merge_clefs_and_keys,
                                 "keys": merge_clefs_and_keys,
                                 "tempos": lambda k: ", ".join(k),
                                 "time_signatures": lambda k: ", ".join(k)}

            for key in keys:
                if key in data:
                    datastring = "{}: {}".format(key, data[key])
                    if key in alternate_methods:
                        datastring = alternate_methods[key](data[key])
                    elem = QtGui.QListWidgetItem(datastring)
                    self.listWidget.addItem(elem)

            self.listWidget.show()


class FeaturedIn(PlaylistWidget):
    name = "featured"

    def __init__(self, parent, design_folder):
        PlaylistWidget.__init__(
            self,
            parent,
            "BasicListWidget.ui",
            self.name,
            design_folder,
            data_set="featured")

    def loadPlaylists(self, sort_method='all'):
        if self.main_window.current_piece != "":
            data = self.application.loadUserPlaylistsForAGivenFile(
                self.main_window.current_piece)
            self.listWidget.clear()
            self.create_widgets(data)
            self.listWidget.show()


class PlaylistBrowser(Window):

    def __init__(self, parent, design_folder):
        Window.__init__(
            self,
            parent,
            "BasicTableWidget.ui",
            "Browser",
            design_folder)
        self.playlist = self.main_window.playlist
        self.index = self.main_window.index
        if self.playlist is not None and self.index is not None:
            self.load()
        self.tableWidget.itemDoubleClicked.connect(self.loadPiece)

    def load(self):
        data = self.application.getPlaylistFileInfo(self.playlist)
        if self.tableWidget.rowCount() != 0:
            self.tableWidget.clear()
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderLabels(
            ['Title', 'Composer', 'Filename'])
        fit_columns_to_widget(self.tableWidget, 3)
        self.tableWidget.setRowCount(len(data))
        columns = ("title", "composer", "filename")
        for i in range(len(data)):
            for j, column in zip(range(len(columns)), columns):
                if column in data[i]:
                    item = QtGui.QTableWidgetItem(data[i][column])
                    item.setData(32, data[i]["filename"])
                    self.tableWidget.setItem(i, j, item)
                else:
                    item = QtGui.QTableWidgetItem("")
                    item.setData(32, data[i]["filename"])
                    self.tableWidget.setItem(i, j, item)

        self.tableWidget.selectRow(self.index)
        self.tableWidget.show()


class SearchTree(QtGui.QTreeWidget):

    def __init__(self, parent, design_folder):
        QtGui.QTreeWidget.__init__(self)
        self.main_window = parent
        self.application = self.main_window.qApp
        design = os.path.join(design_folder, "treeWidget.ui")
        uic.loadUi(design, self)
        self.treeWidget.itemDoubleClicked.connect(self.clicked)

    def leaveEvent(self, QFocusEvent):
        if not self.hasFocus():
            self.main_window.unloadSearch()
        QFocusEvent.accept()

    def clicked(self, current_item):
        self.main_window.unloadFrame("searchtree")
        file_to_load = current_item.data(0, 32)
        self.application.loadFile(file_to_load)

    def clear(self):
        root = self.treeWidget.invisibleRootItem()
        children = self.group_children(root)
        names = [child[1] for child in children]
        for location_type in names:
            self.remove_children(location_type, children, root)

    def group_children(self, root):
        child_count = root.childCount()
        children = [(i, root.child(i).text(0)) for i in range(child_count)]
        return children

    def remove_children(self, location_type, children, root):
        index = [child[0]
                 for child in children if child[1] == location_type]
        item = root.child(index[0])
        for i in range(item.childCount()):
            child = item.child(i)
            item.removeChild(child)

    def load(self, results):
        root = self.treeWidget.invisibleRootItem()
        children = self.group_children(root)
        names = [child[1] for child in children]
        for location_type in results:
            item = QtGui.QTreeWidgetItem(location_type)
            item.setData(0, 0, location_type)
            if location_type in names:
                self.remove_children(location_type, children, root)

            else:
                self.treeWidget.addTopLevelItem(item)
            for key in results[location_type]:
                sub_item = QtGui.QTreeWidgetItem(key)
                sub_item.setData(0, 0, key)
                item.addChild(sub_item)
                for file in results[location_type][key]:
                    fitem = QtGui.QTreeWidgetItem(file[0])
                    fitem.setData(0, 0, file[0])
                    fitem.setData(0, 32, file[1])
                    sub_item.addChild(fitem)
