from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
import sys

class Startup(QtGui.QMainWindow):
    def __init__(self, parent):
        #somewhere in constructor:
        self.parent = parent
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('Startup.ui', self)
        self.folderBtn.clicked.connect(self.openFolderDialog)

    def openFolderDialog(self):
        self.parent.FolderFetched(str(QFileDialog.getExistingDirectory(self, "Select Directory")))

