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
        options = ["title","composer","lyricist"]
        self.scoreSortCombo.addItems(options)
        self.scoreListWidget.show()
        self.refreshScoreBtn.clicked.connect(self.refreshScores)
        self.refreshAutoBtn.clicked.connect(self.refreshPlaylists)
        self.AddPlaylistButton.clicked.connect(self.addPlaylist)
        self.searchInput.textChanged.connect(self.updateOptions)
        self.searchInput.returnPressed.connect(self.searchDb)
        self.scoreSortCombo.currentIndexChanged.connect(self.onSortMethodChange)
        self.scoreListWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)


    def onItemDoubleClicked(self, current_item):
        file_to_load = current_item.data(1)
        filename = self.parent.loadFile(file_to_load)
        rendered_pdf = self.pdf_view(filename)
        self.musicArea.show()

    def pdf_view(self, filename):
        """Return a Scrollarea showing the first page of the specified PDF file."""

        label = QtGui.QLabel(self)

        doc = Poppler.Document.load(filename)
        doc.setRenderHint(Poppler.Document.Antialiasing)
        doc.setRenderHint(Poppler.Document.TextAntialiasing)

        page = doc.page(0)
        image = page.renderToImage()

        label.setPixmap(QtGui.QPixmap.fromImage(image))

        self.musicArea.setWidget(label)

    def onSortMethodChange(self):
        sort_method = self.scoreSortCombo.currentText()
        pieces = self.parent.loadPieces(method=sort_method)
        for i in pieces:
            item = QtGui.QListWidgetItem(i[0])
            item.setData(1, i[1])
            self.scoreListWidget.addItem(item)
        self.scoreListWidget.show()

    def refreshScores(self):
        self.parent.updateDb()
        self.onSortMethodChange()

    def refreshPlaylists(self):
        print("refreshed playlists")

    def addPlaylist(self):
        print("added playlist")

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