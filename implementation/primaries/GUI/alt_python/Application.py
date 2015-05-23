from PyQt4 import QtGui, QtCore
import StartupWindow, MainWindow
import pickle, sys
from implementation.primaries.GUI import qt_threading
from implementation.primaries.ExtractMetadata.classes import MusicManager

class Application(QtCore.QObject):
    windows = {}
    def __init__(self, app):
        QtCore.QObject.__init__(self)
        self.app = app
        self.folder = ""
        self.collections = []
        self.manager = None
        self.LoadCollections()
        self.load_windows()


    def start(self):
        self.windows["startup"].show()
        self.windows["startup"].load(self.collections)

    def loadPieces(self, method="title", slot=None):
        worker = qt_threading.mythread(self, self.manager.getPieceSummaryStrings, (method,))
        QtCore.QObject.connect(worker, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        worker.run()

    def load_windows(self):
        startup = StartupWindow.StartupWindow(self)
        self.windows["startup"] = startup
        self.windows["startup"].show()

        main = MainWindow.MainWindow(self)
        self.windows["main"] = main
        self.windows["main"].show()
        self.windows["main"].hide()


    def LoadCollections(self):
        try:
            fob = open(".collections", 'r')
            pickler = pickle.Unpickler(fob)
            self.collections = pickler.load()
            fob.close()
        except:
            self.SaveCollections()

    def SaveCollections(self):
        fob = open(".collections", 'wb')
        pickle.dump(self.collections, fob)
        fob.close()



    def FolderFetched(self, folder):
        self.folder = folder
        if self.folder is not None:
            self.collections.append(self.folder)
            self.SaveCollections()
            self.windows["startup"].hide()
            self.manager = MusicManager.MusicManager(self, folder=self.folder)
            self.windows["main"].show()
            self.windows["main"].load()

app = QtGui.QApplication(sys.argv)
application = Application(app)
application.start()
sys.exit(app.exec_())
