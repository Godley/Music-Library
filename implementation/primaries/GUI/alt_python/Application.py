from PyQt4 import QtGui, QtCore, QtXml
from implementation.primaries.GUI.alt_python import StartupWindow, MainWindow
import pickle, sys
from implementation.primaries.GUI import qt_threading
from implementation.primaries.ExtractMetadata.classes import MusicManager
import os

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

        if len(self.collections) > 0:
            self.loadFolder(self.collections[-1])

    def loadPieces(self, method="title", slot=None):
        worker = qt_threading.mythread(self, self.manager.getPieceSummaryStrings, (method,))
        QtCore.QObject.connect(worker, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        worker.run()

    def onRenderTaskFinished(self, errorList, filename=""):
        """
        asynchronous handler. This gets called when an async task has finished rendering a piece,
        adn thus comes back and calls the handler for this result in the main window
        :param errorList: the list of problems encountered
        :param filename: the filename ending in pdf without the current folder
        :return: None, calls another method lower down
        """
        pdf = os.path.join(self.folder, filename)
        if not os.path.exists(pdf):
            errorList.append(
                "file rendering failed to produce a pdf, check above errors")
        if len(errorList) > 0:
            self.errorPopup(errorList)
        if os.path.exists(pdf):
            self.windows["main"].onPieceLoaded(pdf, filename)

    def loadFile(self, filename):
        """
        Method which will do 3 things;
        - check a pdf version for given file exists
        - if not check if an xml version exists
            - if so, start another thread to load it which will call the async callback above when done
            - if not, open up a licensing agreement box for the file which will either load the file or close
        :param filename: xml filename, not including current folder
        :return: None, calls methods instead
        """
        pdf_version = filename.split(".")[0] + ".pdf"
        if os.path.exists(os.path.join(self.folder, pdf_version)):
            self.onRenderTaskFinished([], pdf_version)
        else:
            if not os.path.exists(os.path.join(self.folder, filename)):
                license = self.manager.getLicense(filename)
                self.windows["license"].load(license, filename)
                self.windows["license"].setWindowFlags(QtCore.Qt.Dialog)
                self.windows["license"].exec()
            else:
                render_thread = qt_threading.RenderThread(self, self.manager.startRenderingTask,
                                                            (filename,), pdf_version)
                QtCore.QObject.connect(render_thread, QtCore.SIGNAL("fileReady(PyQt_PyObject, PyQt_PyObject)"), self.onRenderTaskFinished)
                QtCore.QObject.connect(render_thread, QtCore.SIGNAL("renderingError(PyQt_PyObject)"), self.onRenderError)
                render_thread.run()

    def onRenderError(self, error):
        pass

    def getFileInfo(self, filename):
        file_info = self.manager.getFileInfo(filename)
        return file_info

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
            col_fob = open(".collections", 'rb')
        except:
            self.SaveCollections()
            col_fob = open(".collections", 'rb')
        result_temp = pickle.load(col_fob)
        if result_temp is not None:
            self.collections = result_temp
        return self.collections

    def SaveCollections(self):
        col_fob = open(".collections", 'wb')
        pickle_obj = pickle.Pickler(col_fob)
        pickle_obj.dump(self.collections)
        col_fob.close()

    def loadFolder(self, folder):
        self.folder = folder
        self.windows["startup"].hide()
        self.manager = MusicManager.MusicManager(self, folder=self.folder)
        self.windows["main"].show()
        self.windows["main"].load()




    def FolderFetched(self, folder):
        if self.folder is not None:
            self.collections.append(folder)
            self.SaveCollections()
            self.LoadCollections()
            self.loadFolder(folder)


    def getCreatedPlaylists(self, slot=None):
        async = qt_threading.mythread(self, self.manager.getPlaylistsFromPlaylistTable, ())
        QtCore.QObject.connect(async, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        async.run()

    def getPlaylists(self, select_method="all", slot=None):
        async = qt_threading.mythread(self, self.manager.getPlaylists, (select_method,))
        QtCore.QObject.connect(async, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        async.run()

app = QtGui.QApplication(sys.argv)
application = Application(app)
application.start()
sys.exit(app.exec_())
