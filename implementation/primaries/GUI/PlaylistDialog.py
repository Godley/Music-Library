from PyQt4 import QtCore, QtGui, uic


class PlaylistDialog(QtGui.QDialog):

    def __init__(self, parent, theme):
        self.parent = parent
        self.theme = theme

        QtGui.QDialog.__init__(self)
        uic.loadUi('designer_files/NewPlaylist.ui', self)
        self.autoCompleteFrame.hide()
        self.buttonBox.accepted.connect(self.newPlaylistOk)
        self.autoCompleteBox.itemDoubleClicked.connect(self.itemClicked)
        self.piecesLineEdit.editingFinished.connect(self.onInactiveSearchBar)
        self.deleteItem.clicked.connect(self.removeItem)
        self.piecesLineEdit.textChanged.connect(self.updateOptions)
        self.setTheme()

    def setTheme(self):
        file = open("themes/" + self.theme + ".qss", 'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        self.repaint()

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
        self.parent.addPlaylist(data)

    def updateOptions(self):
        text = self.piecesLineEdit.text()
        results = self.parent.query(text)
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
            # self.noResultsSmiley.show()
            # self.noResultsLabel.show()
        else:
            pass
            # self.noResultsSmiley.hide()
            # self.noResultsLabel.hide()
            # rows = len(results)
            # rowSize = self.autoCompleteBox.sizeHintForRow(0)
            # height = rows * rowSize
            # frameWidth = self.autoCompleteBox.frameWidth()
            # fixedHeight = height + frameWidth * 2
            # if fixedHeight > self.sizeHint().height():
            #     fixedHeight = self.sizeHint().height() / 1.2
            # self.autoCompleteBox.setFixedHeight(fixedHeight)
            # self.autoCompleteFrame.setFixedHeight(fixedHeight+50)

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
