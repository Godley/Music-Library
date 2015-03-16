from PyQt4 import QtCore, QtGui, uic
from popplerqt4 import Poppler
import sys

class PlaylistDialog(QtGui.QDialog):
    def __init__(self, parent):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uic.loadUi('NewPlaylist.ui', self)
