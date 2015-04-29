from PyQt4.QtCore import QObject, QThread, pyqtSignal, SIGNAL

from threading import Lock


class mythread(QThread):
    def __init__(self, parent, method, args, **kwargs):
        QThread.__init__(self,parent)
        self.args = args
        self.kwargs = kwargs
        self.method = method

    def run(self):
        result = self.method(*self.args, **self.kwargs)
        self.emit(SIGNAL("dataReady(PyQt_PyObject)"), result)

class QueryThread(QThread):
    def __init__(self, parent, method, args, online):
        QThread.__init__(self,parent)
        self.args = args
        self.method = method
        self.online = online

    def run(self):
        result = self.method(*self.args, online=self.online)
        self.emit(SIGNAL("dataReady(PyQt_PyObject, bool)"), result, self.online)

class RenderThread(QThread):
    def __init__(self, parent, method, args, filename):
        QThread.__init__(self,parent)
        self.args = args
        self.method = method
        self.filename = filename

    def run(self):
        result = self.method(*self.args)
        self.emit(SIGNAL("fileReady(PyQt_PyObject, PyQt_PyObject)"), result, self.filename)

class DownloadThread(QThread):
    def __init__(self, parent, method, args):
        QThread.__init__(self,parent)
        self.fname = args
        self.method = method

    def run(self):
        result = self.method(self.fname)
        if not result:
            self.emit(SIGNAL("downloadError(bool)"), result)
        else:
            pdf = self.fname.split(".")[0]+".pdf"
            self.emit(SIGNAL("fileReady(PyQt_PyObject)"), pdf)

