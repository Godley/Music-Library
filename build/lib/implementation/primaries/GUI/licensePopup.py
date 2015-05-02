from PyQt4 import QtCore, QtGui, uic
import os
from implementation.primaries.GUI.helpers import get_base_dir


class LicensePopup(QtGui.QDialog):

    def __init__(self, parent, terms, file, theme):
        self.theme = theme
        self.parent = parent
        QtGui.QDialog.__init__(self)
        path_to_file = os.path.join(get_base_dir(return_this_dir=True), "designer_files", "licensePopup.ui")
        uic.loadUi(path_to_file, self)
        self.license_terms = terms
        self.file = file
        self.loadLicense()
        self.buttonBox.accepted.connect(self.fetchAndClose)
        self.setTheme()

    def loadLicense(self):
        sizeHint = self.licenseScrollArea.size()
        width = sizeHint.width()
        license = self.license_terms
        label = QtGui.QLabel()
        label.setFixedWidth(width)
        label.setWordWrap(True)
        label.setText(license)
        self.licenseScrollArea.setWidget(label)
        self.licenseScrollArea.show()

    def fetchAndClose(self):
        self.parent.downloadFile(self.file)

    def setTheme(self):
        path_to_file = os.path.join(get_base_dir(return_this_dir=True), "themes", self.theme+".qss")
        file = open(path_to_file, 'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        self.repaint()

