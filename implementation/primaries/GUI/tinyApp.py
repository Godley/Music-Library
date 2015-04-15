
from PyQt4 import QtCore, QtGui
import sys, time
 
class mythread(QtCore.QThread):
    def __init__(self, parent, method, data, n):
        QtCore.QThread.__init__(self,parent)
        self.max = n
        self.data = data
        self.method = method
 
    def run(self):
        self.emit(QtCore.SIGNAL("total(PyQt_PyObject)"),self.max)
        result = 0
        while self.data < self.max:
            self.data = self.method(self.data)
            self.emit(QtCore.SIGNAL("dataReady(PyQt_PyObject)"), self.data)

 
# create the dialog for zoom to point
class progress(QtGui.QDialog):
    def __init__(self): 
        QtGui.QDialog.__init__(self)
        self.t=mythread(self,self.method, 0, 100)
        QtCore.QObject.connect(self.t, QtCore.SIGNAL("total(PyQt_PyObject)"), self.total)
        QtCore.QObject.connect(self.t, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), self.update)
        self.n=0
        self.t.start()

    def method(self, n):
        return n+1

    def update(self, data):
        self.n = data
        print(self.n)
        #self.ui.progressBar.setValue(self.n)

    def total(self,total):
        pass
        #self.ui.progressBar.setMaximum(total)
 
if __name__=="__main__":
    app = QtGui.QApplication([])
    c=progress()
    c.show()
    sys.exit(app.exec_())