from PyQt4 import QtCore, QtGui, uic
import os
from helper import get_base_dir

class Searchbox(QtGui.QTreeWidget):
    def __init__(self):
        QtGui.QTreeView.__init__(self)
        file = os.path.join(get_base_dir(True), "alternatives", "treeWidget.ui")
        uic.loadUi(file, self)
