from PyQt4 import QtCore, QtGui, uic
from popplerqt4 import Poppler
import sys

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent):
        self.parent = parent

        #somewhere in constructor:
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('MainWindow.ui', self)
        pieces = self.parent.loadPieces()
        for i in pieces:
            item = QtGui.QListWidgetItem(i[0])
            item.setData(1, i[1])
            self.scoreListWidget.addItem(item)
        self.loadPlaylists()
        options = ["title","composer","lyricist"]
        self.scoreSortCombo.addItems(options)
        self.scoreListWidget.show()
        self.refreshScoreBtn.clicked.connect(self.refreshScores)
        self.refreshAutoBtn.clicked.connect(self.refreshPlaylists)
        self.AddPlaylistButton.clicked.connect(self.addPlaylist)
        #self.searchInput.textChanged.connect(self.updateOptions)
        #self.searchInput.returnPressed.connect(self.searchDb)
        self.scoreSortCombo.currentIndexChanged.connect(self.onSortMethodChange)
        self.scoreListWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.autoPlaylistsView.itemDoubleClicked.connect(self.onPlaylistDoubleClicked)
        #self.myPlaylistsWidget.itemDoubleClicked.connect(self.onPlaylistDoubleClicked)
        self.editPlaylistTitle.hide()
        self.playlistViewer.hide()

    def onPlaylistDoubleClicked(self, current_item):
        self.scoreWindow.hide()
        playlist_to_load = current_item.data(1)
        length = len(playlist_to_load)
        self.playlistTable.setRowCount(length)
        for i in range(length):
            file_data = self.parent.getFileInfo(playlist_to_load[i])[0]
            item = QtGui.QTableWidgetItem(str(i))
            self.playlistTable.setItem(i, 0, item)
            item = QtGui.QTableWidgetItem(file_data["title"])
            self.playlistTable.setItem(i, 1, item)
            if "composer" in file_data:
                item = QtGui.QTableWidgetItem(file_data["composer"])
                self.playlistTable.setItem(i, 2, item)
            if "lyricist" in file_data:
                item = QtGui.QTableWidgetItem(file_data["lyricist"])
                self.playlistTable.setItem(i, 3, item)
            if "instruments" in file_data:
                item = QtGui.QTableWidgetItem(", ".join([data["name"] for data in file_data["instruments"]]))
                self.playlistTable.setItem(i, 4, item)
            item = QtGui.QTableWidgetItem(playlist_to_load[i])
            self.playlistTable.setItem(i, 5, item)
            if "clefs" in file_data:
                result = ""
                for instrument in file_data["clefs"]:
                    result += ", ".join(file_data["clefs"][instrument])
                item = QtGui.QTableWidgetItem(result)
                self.playlistTable.setItem(i, 6, item)
            if "keys" in file_data:
                result = ""
                for instrument in file_data["keys"]:
                    result += ", ".join(file_data["keys"][instrument])
                item = QtGui.QTableWidgetItem(result)
                self.playlistTable.setItem(i, 7, item)
            if "tempos" in file_data:
                item = QtGui.QTableWidgetItem(", ".join(file_data["tempos"]))
                self.playlistTable.setItem(i, 8, item)
            if "time_signatures" in file_data:
                item = QtGui.QTableWidgetItem(", ".join(file_data["time_signatures"]))
                self.playlistTable.setItem(i, 9, item)
        num = self.playlistTable.rowCount()
        playlist_title = current_item.data(3)
        self.musicTitle.setText(playlist_title)
        self.editPlaylistTitle.show()
        self.playlistTable.show()
        self.playlistViewer.show()


    def onItemDoubleClicked(self, current_item):
        self.scoreWindow.show()
        self.editPlaylistTitle.hide()
        file_to_load = current_item.data(1)
        filename = self.parent.loadFile(file_to_load)
        self.loadPieceData(file_to_load)
        self.pdf_view(filename)
        self.musicTitle.setText(file_to_load)
        self.musicTitle.repaint()
        self.playlistViewer.hide()

    def loadPieceData(self, filename):
        self.pieceInfoView.clear()
        data = self.parent.getFileInfo(filename)[0]
        datastring = ""

        datastring = "title: "+data["title"]
        title = QtGui.QListWidgetItem(datastring)
        self.pieceInfoView.addItem(title)
        if "composer" in data and data["composer"] != -1:
            datastring = "composer: "+data["composer"]
            composer = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(composer)
        if "lyricist" in data and data["lyricist"] != -1:
            datastring = "lyricist: "+data["lyricist"]
            lyricist = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(lyricist)
        if "instruments" in data:
            datastring = "instruments: "+", ".join([d["name"] for d in data["instruments"]])
            instruments = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(instruments)
        if "clefs" in data:
            datastring = "clefs: "
            clef_list = []
            for instrument in data["clefs"]:
                for clef in data["clefs"][instrument]:
                    if clef not in clef_list:
                        clef_list.append(clef)
            datastring += ", ".join(clef_list)
            clefs = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(clefs)
        if "keys" in data:
            datastring = "keys: "
            key_list = []
            for instrument in data["keys"]:
                for key in data["keys"][instrument]:
                    if key_list not in key_list:
                        key_list.append(key)
            datastring += ", ".join(key_list)
            keys = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(keys)

        if "tempos" in data:
            datastring = "tempos: "
            tempo_list = []
            for tempo in data["tempos"]:
                datastring += tempo
                datastring += ", "
            tempos = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(tempos)

        if "time_signatures" in data:
            datastring = "time signatures: "
            tempo_list = []
            for tempo in data["time_signatures"]:
                datastring += tempo
                datastring += ", "
            tempos = QtGui.QListWidgetItem(datastring)
            self.pieceInfoView.addItem(tempos)

        self.pieceInfoView.show()


    def pdf_view(self, filename):
        """Return a Scrollarea showing the first page of the specified PDF file."""

        label = QtGui.QLabel(self)


        doc = Poppler.Document.load(filename)
        doc.setRenderHint(Poppler.Document.Antialiasing)
        doc.setRenderHint(Poppler.Document.TextAntialiasing)

        page = doc.page(0)
        dimensions = page.pageSize()
        scroll_height = self.scoreWindow.height()
        scroll_width = self.scoreWindow.width()
        image = page.renderToImage(90, 90, -10, 0, scroll_width, scroll_height)

        label.setPixmap(QtGui.QPixmap.fromImage(image))

        self.scoreWindow.setWidget(label)


    def onSortMethodChange(self):
        sort_method = self.scoreSortCombo.currentText()
        pieces = self.parent.loadPieces(method=sort_method)
        self.scoreListWidget.clear()
        for i in pieces:
            item = QtGui.QListWidgetItem(i[0])
            item.setData(1, i[1])
            self.scoreListWidget.addItem(item)
        self.scoreListWidget.show()

    def refreshScores(self):
        self.parent.updateDb()
        self.onSortMethodChange()

    def loadPlaylists(self):
        playlist_summaries = self.parent.getPlaylists()
        self.autoPlaylistsView.clear()
        for i in playlist_summaries:
            item = QtGui.QListWidgetItem(i)
            self.autoPlaylistsView.addItem(item)
            for j in playlist_summaries[i]:
                item = QtGui.QListWidgetItem(j)
                item.setData(1, playlist_summaries[i][j])
                item.setData(3, i+j)
                self.autoPlaylistsView.addItem(item)
        self.autoPlaylistsView.show()

    def refreshPlaylists(self):
        self.parent.updateDb()
        self.loadPlaylists()

    def addPlaylist(self):
        self.parent.PlaylistPopup()

    def searchDb(self):
        print("finding thing")

    def updateOptions(self):
        print("updating autocomplete searchbox under lineedit")

def main():

    app = QtGui.QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()