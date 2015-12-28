from PyQt4 import QtCore, QtGui, uic
import os
from helper import get_base_dir


class Searchbox(QtGui.QTreeWidget):

    def __init__(self, design_folder):
        QtGui.QTreeView.__init__(self)
        file = os.path.join(design_folder, "treeWidget.ui")
        uic.loadUi(file, self)
