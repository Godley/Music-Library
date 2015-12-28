from PyQt4 import uic, QtGui
from implementation.primaries.GUI.helpers import get_base_dir
import os
from implementation.primaries.GUI import themedWindow


class StartupWindow(QtGui.QDialog, themedWindow.ThemedWindow):

    def __init__(self, app, theme, themes, design_folder):
        super().__init__()
        self.qApp = app
        themedWindow.ThemedWindow.__init__(self, theme, themes)
        self.design_folder = design_folder

    def load(self, items):
        file = os.path.join(self.design_folder, "Startup.ui")
        uic.loadUi(file, self)

        self.folderBtn.clicked.connect(self.openFolderDialog)
        self.collectionListWidget.itemDoubleClicked.connect(
            self.onItemDoubleClicked)
        self.removeColBtn.clicked.connect(self.deleteCollection)
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
        self.hide()

    def openFolderDialog(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self, "Select Directory")
        if folder is not None and folder != "":
            self.qApp.FolderFetched(str(folder))
            self.hide()

