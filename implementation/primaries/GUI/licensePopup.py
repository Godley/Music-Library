from PyQt4 import QtCore, QtGui, uic
import os
from implementation.primaries.GUI.helpers import get_base_dir
from implementation.primaries.GUI import themedWindow


class LicensePopup(QtGui.QDialog, themedWindow.ThemedWindow):

    def __init__(self, parent, theme, theme_folder):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, theme_folder)
        path_to_file = os.path.join(get_base_dir(return_this_dir=True), "designer_files", "licensePopup.ui")
        uic.loadUi(path_to_file, self)
        self.buttonBox.accepted.connect(self.fetchAndClose)
        self.applyTheme()

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

