from PyQt4 import QtCore, QtGui, uic

class ImportDialog(QtGui.QDialog):
    def __init__(self, parent):
        self.parent = parent
        QtGui.QDialog.__init__(self)
        uic.loadUi('importDialog.ui', self)



