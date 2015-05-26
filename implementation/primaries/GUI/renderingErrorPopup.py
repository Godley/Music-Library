from PyQt4 import QtCore, QtGui, uic
import os
from implementation.primaries.GUI.helpers import  get_base_dir
from implementation.primaries.GUI import themedWindow
class RenderingErrorPopup(QtGui.QDialog, themedWindow.ThemedWindow):

    def __init__(self, parent, theme, themes):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, themes)
        path_to_file = os.path.join(get_base_dir(return_this_dir=True), "designer_files", "renderingErrorPopup.ui")
        uic.loadUi(path_to_file, self)
        self.pushButton.clicked.connect(self.close)
        self.applyTheme()

    def load(self, errorList):
        self.listWidget.clear()
        for error in errorList:
            item = QtGui.QListWidgetItem(error)
            self.listWidget.addItem(item)
        self.listWidget.show()
