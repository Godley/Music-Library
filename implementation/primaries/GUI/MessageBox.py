from PyQt4 import QtGui,uic
from implementation.primaries.GUI.helpers import get_base_dir
import os

class MessageBox(QtGui.QWidget):
     def __init__(self, parent=None, message="", title="mbox"):
         QtGui.QWidget.__init__(self, parent)

         self.setGeometry(300, 300, 250, 150)
         self.setWindowTitle(title)
         designer_file = os.path.join(get_base_dir(return_this_dir=True), 'designer_files', 'MessageBox.ui')
         uic.loadUi(designer_file, self)
         self.errorLabel.setText(message)
         self.okBtn.clicked.connect(self.close)

