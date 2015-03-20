from PyQt4 import QtCore, QtGui, uic
from popplerqt4 import Poppler
import sys
import threading

class MainWindow(QtGui.QMainWindow):
    def __init__(self, parent):
        self.parent = parent

        #somewhere in constructor:
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('MainWindow.ui', self)
        pieces = self.parent.loadPieces()
        self.autoCompleteFrame.hide()
        for i in pieces:
            item = QtGui.QListWidgetItem(i[0])
            item.setData(1, i[1])
            self.scoreListWidget.addItem(item)
        self.loadPlaylists()
        self.loadMyPlaylists()
        self.progressBarRendering.hide()
        options = ["title","composer","lyricist"]
        self.scoreSortCombo.addItems(options)
        self.scoreListWidget.show()
        self.refreshScoreBtn.clicked.connect(self.refreshScores)
        self.refreshAutoBtn.clicked.connect(self.refreshPlaylists)
        self.AddPlaylistButton.clicked.connect(self.addPlaylist)
        self.searchInput.textChanged.connect(self.updateOptions)
        self.searchInput.returnPressed.connect(self.searchDb)
        self.searchInput.editingFinished.connect(self.onInactiveSearchBar)
        self.searchBtn.clicked.connect(self.searchDb)
        self.scoreSortCombo.currentIndexChanged.connect(self.onSortMethodChange)
        self.scoreListWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.autoPlaylistsView.itemDoubleClicked.connect(self.onPlaylistDoubleClicked)
        self.playlistTable.itemDoubleClicked.connect(self.onItemInPlaylistDoubleClicked)
        #self.myPlaylistsWidget.itemDoubleClicked.connect(self.onPlaylistDoubleClicked)
        self.editPlaylistTitle.hide()
        self.playlistViewer.hide()

    def onItemInPlaylistDoubleClicked(self, current_item):
        playlist = current_item.data(4)
        filename = current_item.data(1)
        index_in_playlist = current_item.data(3)
        data = self.parent.getPlaylistFileInfo(playlist)
        self.playlistList.clear()
        self.playlistList.setRowCount(len(data))
        for i in range(0, index_in_playlist):
            if "composer" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["composer"])
                self.playlistList.setItem(i, 1, item)
            if "title" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["title"])
                self.playlistList.setItem(i, 0, item)
            if "filename" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["filename"])
                self.playlistList.setItem(i, 3, item)
        if "title" in data[index_in_playlist]:
            item = QtGui.QTableWidgetItem(data[index_in_playlist]["title"])
            self.playlistList.setItem(index_in_playlist, 0, item)

        if "composer" in data[index_in_playlist]:
            item = QtGui.QTableWidgetItem(data[index_in_playlist]["composer"])
            self.playlistList.setItem(index_in_playlist, 1, item)

        if "filename" in data[index_in_playlist]:
            item = QtGui.QTableWidgetItem(data[index_in_playlist]["filename"])
            self.playlistList.setItem(index_in_playlist, 2, item)

        for i in range(index_in_playlist+1, len(data)):
            if "composer" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["composer"])
                self.playlistList.setItem(i, 1, item)
            if "title" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["title"])
                self.playlistList.setItem(i, 0, item)
            if "filename" in data[i]:
                item = QtGui.QTableWidgetItem(data[i]["filename"])
                self.playlistList.setItem(i, 3, item)
        self.playlistList.show()

    def setUpDataItems(self, playlist_fnames, playlist_data, start_index, end_index):
        items = []
        for i in range(start_index, end_index):
            file = playlist_data[i]
            row = []
            item = QtGui.QTableWidgetItem(file["title"])
            item.setData(1, file["filename"])
            item.setData(3, i)
            item.setData(4, playlist_fnames)
            row.append(item)
            if "composer" in file:
                item = QtGui.QTableWidgetItem(file["composer"])
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            if "lyricist" in file:
                item = QtGui.QTableWidgetItem(file["lyricist"])
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            if "instruments" in file:
                item = QtGui.QTableWidgetItem(", ".join([data["name"] for data in file["instruments"]]))
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            item = QtGui.QTableWidgetItem(file["filename"])
            item.setData(1, file["filename"])
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
                item.setData(1, file["filename"])
                row.append(item)
            if "keys" in file:
                result = ""
                for instrument in file["keys"]:
                    result += ", ".join(file["keys"][instrument])
                item = QtGui.QTableWidgetItem(result)
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            if "tempos" in file:
                item = QtGui.QTableWidgetItem(", ".join(file["tempos"]))
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                self.playlistTable.setItem(i, 7, item)
            if "time_signatures" in file:
                item = QtGui.QTableWidgetItem(", ".join(file["time_signatures"]))
                item.setData(1, file["filename"])
                item.setData(3, i)
                item.setData(4, playlist_fnames)
                row.append(item)
            items.append(row)
        return items


    def onPlaylistDoubleClicked(self, current_item):
        self.scoreWindow.hide()
        playlist_to_load = current_item.data(1)
        length = len(playlist_to_load)
        playlist_title = current_item.data(3)
        self.playlistTable.setRowCount(length)
        file_data = self.parent.getPlaylistFileInfo(playlist_to_load)
        data_items = self.setUpDataItems(playlist_to_load, file_data, 0, len(file_data))
        for i in range(len(data_items)):
            for j in range(len(data_items[i])):
                self.playlistTable.setItem(i, j, data_items[i][j])
        self.musicTitle.setText(playlist_title)
        self.editPlaylistTitle.show()
        self.playlistTable.show()
        self.playlistViewer.show()


    def onInactiveSearchBar(self):
        self.autoCompleteBox.clear()
        self.autoCompleteFrame.hide()

    def onItemDoubleClicked(self, current_item):
        self.scoreWindow.show()
        #self.progressBarRendering.show()
        #self.progressBarRendering.setRange(0, 100)
        self.editPlaylistTitle.hide()
        file_to_load = current_item.data(1)
        filename = self.parent.loadFile(file_to_load)

        self.loadPieceData(file_to_load)
        self.pdf_view(filename)
        self.musicTitle.setText(file_to_load)
        self.musicTitle.repaint()
        self.playlistViewer.hide()

    def updateProgressBar(self):
        bar_value = self.progressBarRendering.value()
        self.progressBarRendering.setValue(bar_value+1)
        self.progressBarRendering.repaint()

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

    def loadMyPlaylists(self):
        self.myPlaylistsWidget.clear()
        myPlaylists = self.parent.getCreatedPlaylists()
        for entry in myPlaylists:
            item = QtGui.QListWidgetItem(entry["name"])
            item.setData(1, entry["pieces"])
            self.myPlaylistsWidget.addItem(item)
        self.myPlaylistsWidget.show()


    def refreshPlaylists(self):
        self.parent.updateDb()
        self.loadPlaylists()

    def addPlaylist(self):
        self.parent.PlaylistPopup()
        self.loadMyPlaylists()

    def searchDb(self):
        print("finding thing")

    def updateOptions(self):
        text = self.searchInput.text()
        results = self.parent.query(text)
        self.autoCompleteBox.clear()
        for result in results:
            item = QtGui.QListWidgetItem(result[0])
            item.setData(1, result[1])
            self.autoCompleteBox.addItem(item)
        self.autoCompleteBox.show()
        self.autoCompleteFrame.show()


def main():

    app = QtGui.QApplication(sys.argv)

    w = MainWindow()
    w.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()