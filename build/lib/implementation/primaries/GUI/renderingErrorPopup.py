from PyQt4 import QtCore, QtGui, uic
import os
from implementation.primaries.Drawing.classes.helpers import  get_base_dir

class RenderingErrorPopup(QtGui.QDialog):

    def __init__(self, parent, errorList, theme):
        self.theme = theme
        self.parent = parent
        QtGui.QDialog.__init__(self)
        path_to_file = os.path.join(get_base_dir(), "designer_files", "renderingErrorPopup.ui")
        uic.loadUi(path_to_file, self)
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
        path_to_file = os.path.join(get_base_dir(), "themes/", self.theme+".qss")
        file = open(path_to_file, 'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        self.repaint()
