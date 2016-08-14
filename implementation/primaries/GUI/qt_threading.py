from PyQt4.QtCore import QObject, QThread, pyqtSignal, SIGNAL

from threading import Lock

class AppThread(QThread):
    def __init__(self, parent, method, args, **kwargs):
        QThread.__init__(self, parent)
        self.args = args
        self.method = method

class mythread(AppThread):

    def __init__(self, parent, method, args, **kwargs):
        super().__init__(parent, method, args)
        self.kwargs = kwargs

    def run(self):
        result = self.method(*self.args, **self.kwargs)
        self.emit(SIGNAL("dataReady(PyQt_PyObject)"), result)


class QueryThread(AppThread):

    def __init__(self, parent, method, args, online):
        super().__init__(parent, method, args)
        self.online = online

    def run(self):
        result = self.method(*self.args, online=self.online)
        self.emit(
            SIGNAL("dataReady(PyQt_PyObject, bool)"), result, self.online)


class RenderThread(AppThread):

    def __init__(self, parent, method, args, filename):
        super().__init__(parent, method, args)
        self.filename = filename

    def run(self):
        try:
            result = self.method(*self.args)
            self.emit(
                SIGNAL("fileReady(PyQt_PyObject, PyQt_PyObject)"), result, self.filename)
        except BaseException as e:
            self.emit(SIGNAL("renderingError(PyQt_PyObject)"), e)


class DownloadThread(AppThread):

    def __init__(self, parent, method, args):
        super().__init__(parent, method, args)
        self.fname = args

    def run(self):
        result = self.method(self.fname)
        if not result:
            self.emit(SIGNAL("downloadError(bool)"), result)
        else:
            pdf = self.fname.split(".")[0] + ".pdf"
            self.emit(SIGNAL("fileReady(PyQt_PyObject)"), pdf)
