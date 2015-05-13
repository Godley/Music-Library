from PyQt4 import QtCore, QtGui, uic
from PyQt4.QtGui import QFileDialog
from implementation.primaries.GUI.helpers import get_base_dir
from implementation.primaries.GUI import MessageBox
from implementation.primaries.scripts import setup_script
from implementation.primaries.exceptions import LilypondNotInstalledException
import os




class SetupWindow(QtGui.QDialog):

    def __init__(self, parent):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        designer_file = os.path.join(get_base_dir(return_this_dir=True), 'designer_files', 'SetupWindow.ui')
        uic.loadUi(designer_file, self)


    def refresh(self):
        try:
            setup_script.setup_lilypond()
        except LilypondNotInstalledException as e:
            messageBox = MessageBox.MessageBox(parent=self, message="Lilypond was not found", title="Lilypond error, default install")
            messageBox.show()


    def browse(self):
        path = str(QFileDialog.getExistingDirectory(self, "Select Directory"))
        try:
            setup_script.setup_lilypond(path=path)
        except LilypondNotInstalledException as e:
             messageBox = MessageBox.MessageBox(parent=self, message="Lilypond was not found", title="Lilypond error, custom install")
             messageBox.show()
