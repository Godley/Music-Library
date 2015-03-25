from PyQt4 import QtCore, QtGui, uic

class RenderingErrorPopup(QtGui.QDialog):
    def __init__(self, parent, errorList):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uic.loadUi('renderingErrorPopup.ui', self)
        self.errors = errorList
        self.loadItems()
        self.pushButton.clicked.connect(self.close)

    def loadItems(self):
        for error in self.errors:
            item = QtGui.QListWidgetItem(error)
            self.listWidget.addItem(item)
        self.listWidget.show()


