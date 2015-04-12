from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog


class ImportDialog(QtGui.QDialog):

    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme
        QtGui.QDialog.__init__(self)
        uic.loadUi('importDialog.ui', self)
        self.browseBtn.clicked.connect(self.findFiles)
        self.buttonBox.accepted.connect(self.updateAndClose)
        self.fnames = []
        self.setTheme()

    def findFiles(self):
        filterList = ["*.xml", "*.mxl"]
        fnames, filter = QFileDialog.getOpenFileNamesAndFilter(
            self, caption="Select files to import", filter="MusicXML Files (*.xml *.mxl)")
        for fname in fnames:
            item = QtGui.QListWidgetItem(fname)
            self.listWidget.addItem(item)
        self.fnames = fnames
        self.listWidget.show()

    def updateAndClose(self):
        self.parent.copyFiles(self.fnames)

    def setTheme(self):
        file = open("themes/" + self.theme + ".qss", 'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        self.repaint()
