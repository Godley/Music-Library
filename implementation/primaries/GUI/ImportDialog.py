from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog

class ImportDialog(QtGui.QDialog):
    def __init__(self, parent):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uic.loadUi('importDialog.ui', self)
        self.browseBtn.clicked.connect(self.findFiles)
        self.fnames = []

    def findFiles(self):
        filterList = ["*.xml","*.mxl"]
        fnames, filter = QFileDialog.getOpenFileNamesAndFilter(self, caption="Select files to import",filter="MusicXML Files (*.xml *.mxl)")
        for fname in fnames:
            item = QtGui.QListWidgetItem(fname)
            self.listWidget.addItem(item)
        self.fnames = fnames
        self.listWidget.show()

    def close(self):
        self.parent.copyFiles(self.fnames)
        self.close()



