from PyQt4 import QtCore, QtGui, uic
from popplerqt4 import Poppler
import sys

class PlaylistDialog(QtGui.QDialog):
    def __init__(self, parent):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uic.loadUi('NewPlaylist.ui', self)
        self.buttonBox.accepted.connect(self.newPlaylistOk)

    def newPlaylistOk(self):
        data = {"name":self.playlistNameLineEdit.text(), "pieces":[]}
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            fname = item.data(1)
            data["pieces"].append(fname)
        self.parent.addPlaylist(data)