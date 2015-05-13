from PyQt4 import uic, QtGui
from implementation.primaries.GUI.helpers import get_base_dir
import os

class StartupWindow(QtGui.QMainWindow):
    def __init__(self, app):
        QtGui.QMainWindow.__init__(self)
        self.qApp = app

    def load(self, items):
        file = os.path.join(get_base_dir(True), "designer_files", "Startup.ui")
        uic.loadUi(file, self)
        self.folderBtn.clicked.connect(self.openFolderDialog)
        self.collectionListWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        for item in items:
            col_item = QtGui.QListWidgetItem(item)
            col_item.setData(1, item)
            self.collectionListWidget.addItem(col_item)
        self.collectionListWidget.show()

    def deleteCollection(self):
        listItems = self.collectionListWidget.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.qApp.removeCollection(item.data(1))
            self.collectionListWidget.takeItem(
                self.collectionListWidget.row(item))
        self.collectionListWidget.show()

    def onItemDoubleClicked(self, item):
        self.qApp.FolderFetched(item.data(1))

    def openFolderDialog(self):
        self.qApp.FolderFetched(
            str(QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")))