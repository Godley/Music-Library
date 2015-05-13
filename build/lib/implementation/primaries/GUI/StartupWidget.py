from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
from implementation.primaries.GUI.helpers import get_base_dir
import os




class Startup(QtGui.QMainWindow):

    def __init__(self, parent):
        # somewhere in constructor:
        QtGui.QMainWindow.__init__(self)
        self.parent = parent.parent
        self.app = parent

    def setupWindow(self):
        designer_file = os.path.join(get_base_dir(return_this_dir=True), 'designer_files', 'Startup.ui')
        uic.loadUi(designer_file, self)
        previous_items = self.app.getPreviousCollections()
        for item in previous_items:
            l_item = QtGui.QListWidgetItem(item)
            l_item.setData(1, item)
            self.collectionListWidget.addItem(l_item)
        self.collectionListWidget.show()
        self.folderBtn.clicked.connect(self.openFolderDialog)
        self.collectionListWidget.itemDoubleClicked.connect(
            self.onItemDoubleClicked)
        self.removeCollBtn.clicked.connect(self.deleteCollection)

    def deleteCollection(self):
        listItems = self.collectionListWidget.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.app.removeCollection(item.data(1))
            self.collectionListWidget.takeItem(
                self.collectionListWidget.row(item))
        self.collectionListWidget.show()

    def onItemDoubleClicked(self, item):
        self.app.FolderFetched(item.data(1))

    def openFolderDialog(self):
        self.app.FolderFetched(
            str(QFileDialog.getExistingDirectory(self, "Select Directory")))
