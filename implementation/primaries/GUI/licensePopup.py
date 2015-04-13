from PyQt4 import QtCore, QtGui, uic


class LicensePopup(QtGui.QDialog):

    def __init__(self, parent, terms, file, theme):
        self.theme = theme
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uic.loadUi('designer_files/licensePopup.ui', self)
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
        file = open("themes/" + self.theme + ".qss", 'r')
        fstring = file.readlines()
        self.setStyleSheet("".join(fstring))
        self.repaint()

