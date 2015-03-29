from PyQt4 import QtCore, QtGui, uic

class RenderingErrorPopup(QtGui.QDialog):
    def __init__(self, parent, errorList, theme):
        self.theme = theme
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uic.loadUi('renderingErrorPopup.ui', self)
        self.errors = errorList
        self.loadItems()
        self.pushButton.clicked.connect(self.close)
        self.setTheme()

    def loadItems(self):
        for error in self.errors:
            item = QtGui.QListWidgetItem(error)
            self.listWidget.addItem(item)
        self.listWidget.show()

    def setTheme(self):
        file = open("themes/"+self.theme+".qss",'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        self.repaint()


