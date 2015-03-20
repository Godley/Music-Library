from PyQt4 import QtCore, QtGui, uic
from popplerqt4 import Poppler
import sys

class PlaylistDialog(QtGui.QDialog):
    def __init__(self, parent):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uic.loadUi('NewPlaylist.ui', self)
        self.autoCompleteFrame.hide()
        self.buttonBox.accepted.connect(self.newPlaylistOk)
        self.autoCompleteBox.itemDoubleClicked.connect(self.itemClicked)
        self.piecesLineEdit.textChanged.connect(self.updateOptions)

    def newPlaylistOk(self):
        data = {"name":self.playlistNameLineEdit.text(), "pieces":[]}
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            fname = item.data(1)
            data["pieces"].append(fname)
        self.parent.addPlaylist(data)

    def updateOptions(self):
        text = self.piecesLineEdit.text()
        results = self.parent.query(text)
        self.autoCompleteBox.clear()
        for result in results:
            item = QtGui.QListWidgetItem(result[0])
            item.setData(1, result[1])
            self.autoCompleteBox.addItem(item)
        self.autoCompleteFrame.show()
        self.autoCompleteBox.show()

    def itemClicked(self, current_item):
        self.listWidget.addItem(current_item)
        self.listWidget.show()
        self.autoCompleteFrame.hide()
