from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
import os
from implementation.primaries.GUI.helpers import get_base_dir
from implementation.primaries.GUI import themedWindow


class ImportDialog(QtGui.QDialog, themedWindow.ThemedWindow):

    def __init__(self, parent, theme, themes):
        self.parent = parent
        self.theme = theme
        QtGui.QDialog.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, themes)
        path_to_file = os.path.join(
            get_base_dir(return_this_dir=True), "designer_files", "importDialog.ui")
        uic.loadUi(path_to_file, self)
        self.browseBtn.clicked.connect(self.findFiles)
        self.buttonBox.accepted.connect(self.updateAndClose)
        self.fnames = []
        self.applyTheme()

    def findFiles(self):
        filterList = ["*.xml", "*.mxl"]
        fnames, filter = QFileDialog.getOpenFileNamesAndFilter(
            self, caption="Select files to import", filter="MusicXML Files (*.xml *.mxl)")
        for fname in fnames:
            item = QtGui.QListWidgetItem(fname)
            self.listWidget.addItem(item)
        self.fnames = fnames
        self.listWidget.show()

    def updateAndClose(self):
        self.parent.copyFiles(self.fnames)
