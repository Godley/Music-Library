from PyQt4 import QtCore, QtGui, uic
import os
from implementation.primaries.GUI.helpers import get_base_dir


class LicensePopup(QtGui.QDialog):

    def __init__(self, parent, theme):
        self.theme = theme
        self.parent = parent
        QtGui.QDialog.__init__(self)
        path_to_file = os.path.join(get_base_dir(return_this_dir=True), "designer_files", "licensePopup.ui")
        uic.loadUi(path_to_file, self)
        self.buttonBox.accepted.connect(self.fetchAndClose)
        self.setTheme()

    def load(self, terms, file):
        sizeHint = self.licenseScrollArea.size()
        width = sizeHint.width()
        label = QtGui.QLabel()
        label.setFixedWidth(width)
        label.setWordWrap(True)
        label.setText(terms)
        self.licenseScrollArea.setWidget(label)
        self.licenseScrollArea.show()
        self.file = file

    def fetchAndClose(self):
        self.parent.downloadFile(self.file)

    def setTheme(self):
        path_to_file = os.path.join(get_base_dir(return_this_dir=True), "themes", self.theme+".qss")
        file = open(path_to_file, 'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        self.repaint()

