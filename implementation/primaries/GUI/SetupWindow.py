from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
from implementation.primaries.GUI.helpers import get_base_dir
from implementation.primaries.GUI import MessageBox
from implementation.primaries.scripts import setup_script
from implementation.primaries.exceptions import LilypondNotInstalledException
import os
from implementation.primaries.GUI import themedWindow




class SetupWindow(QtGui.QDialog, themedWindow.ThemedWindow):

    def __init__(self, parent, theme, themes):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, themes)
        designer_file = os.path.join(get_base_dir(return_this_dir=True), 'designer_files', 'SetupWindow.ui')
        uic.loadUi(designer_file, self)
        self.refreshBtn.clicked.connect(self.refresh)
        self.browseBtn.clicked.connect(self.browse)


    def refresh(self):
        try:
            setup_script.setup_lilypond()
            self.hide()
        except LilypondNotInstalledException as e:
            messageBox = MessageBox.MessageBox(parent=self, message="Lilypond was not found", title="Lilypond error, default install")
            messageBox.show()


    def browse(self):
        path, filter = QFileDialog.getOpenFileNameAndFilter(
            self, caption="Select files to import", filter="App file (*.app)")

        try:
            setup_script.setup_lilypond(path=path)
            fob = open(".path", 'w')
            fob.write(path)
            fob.close()
            self.hide()
        except LilypondNotInstalledException as e:
             messageBox = MessageBox.MessageBox(parent=self, message="Lilypond was not found", title="Lilypond error, custom install")
             messageBox.show()
