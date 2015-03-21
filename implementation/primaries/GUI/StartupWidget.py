from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
import sys

class Startup(QtGui.QMainWindow):
    def __init__(self, parent):
        #somewhere in constructor:
        self.parent = parent
        QtGui.QMainWindow.__init__(self)
        uic.loadUi('Startup.ui', self)
        previous_items = self.parent.getPreviousCollections()
        for item in previous_items:
            l_item = QtGui.QListWidgetItem(item)
            l_item.setData(1, item)
            self.collectionListWidget.addItem(l_item)
        self.collectionListWidget.show()
        self.folderBtn.clicked.connect(self.openFolderDialog)
        self.collectionListWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        self.removeCollBtn.clicked.connect(self.deleteCollection)

    def deleteCollection(self):
        listItems=self.collectionListWidget.selectedItems()
        if not listItems: return
        for item in listItems:
            self.parent.removeCollection(item.data(1))
            self.collectionListWidget.takeItem(self.collectionListWidget.row(item))
        self.collectionListWidget.show()

    def onItemDoubleClicked(self, item):
        self.parent.FolderFetched(item.data(1))

    def openFolderDialog(self):
        self.parent.FolderFetched(str(QFileDialog.getExistingDirectory(self, "Select Directory")))

