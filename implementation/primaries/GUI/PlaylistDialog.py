from PyQt4 import QtCore, QtGui, uic

import os
from implementation.primaries.GUI.helpers import get_base_dir
from implementation.primaries.GUI import themedWindow


class PlaylistDialog(QtGui.QDialog, themedWindow.ThemedWindow):

    def __init__(self, app, theme, themes, design_folder):
        QtGui.QDialog.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, themes)
        self.qApp = app
        self.theme = theme
        self.design_folder = design_folder

    def load(self):
        path_to_file = os.path.join(self.design_folder, "NewPlaylist.ui")
        uic.loadUi(path_to_file, self)
        self.autoCompleteFrame.hide()
        self.buttonBox.accepted.connect(self.newPlaylistOk)
        self.autoCompleteBox.itemDoubleClicked.connect(self.itemClicked)
        self.piecesLineEdit.editingFinished.connect(self.onInactiveSearchBar)
        self.deleteItem.clicked.connect(self.removeItem)
        self.piecesLineEdit.textChanged.connect(self.updateOptions)
        self.piecesLineEdit.editingFinished.connect(self.onInactiveSearchBar)
        self.applyTheme()

    def removeItem(self):
        listItems = self.listWidget.selectedItems()
        if not listItems:
            return
        for item in listItems:
            self.listWidget.takeItem(self.listWidget.row(item))
        self.listWidget.show()

    def newPlaylistOk(self):
        data = {"name": self.playlistNameLineEdit.text(), "pieces": []}
        for i in range(self.listWidget.count()):
            item = self.listWidget.item(i)
            fname = item.data(2)
            data["pieces"].append(fname)
        self.qApp.addPlaylist(data)

    def updateOptions(self):
        text = self.piecesLineEdit.text()
        results = self.qApp.queryNotThreaded(text)
        self.autoCompleteBox.clear()
        for key in results:
            item = QtGui.QTreeWidgetItem(key)
            item.setData(0, 0, key)
            self.autoCompleteBox.addTopLevelItem(item)
            for file in results[key]:
                fitem = QtGui.QTreeWidgetItem(file[0])
                fitem.setData(0, 0, file[1])
                item.addChild(fitem)
        if len(results) == 0:
            pass
        else:
            pass

        self.autoCompleteBox.show()
        self.autoCompleteFrame.show()

    def onInactiveSearchBar(self):
        if self.piecesLineEdit.text() == "" or self.piecesLineEdit.text(
        ) == " " or self.autoCompleteBox.topLevelItemCount() == 0 or self.focusWidget() != self.autoCompleteBox:
            self.autoCompleteBox.clear()
            self.autoCompleteFrame.hide()
            self.autoCompleteBox.hide()
        else:
            self.updateOptions()

    def itemClicked(self, current_item):
        fname = current_item.data(0, 0)
        item = QtGui.QListWidgetItem(fname)
        self.listWidget.addItem(item)
        self.listWidget.show()
        self.autoCompleteFrame.hide()
