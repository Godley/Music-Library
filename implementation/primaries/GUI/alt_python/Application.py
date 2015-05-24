from PyQt4 import QtGui, QtCore, QtXml
from implementation.primaries.GUI.alt_python import StartupWindow, MainWindow
from implementation.primaries.scripts.setup_script import setup_lilypond
from implementation.primaries.GUI import SetupWindow
from implementation.primaries.exceptions import LilypondNotInstalledException
import pickle, sys
from implementation.primaries.GUI import qt_threading
from implementation.primaries.ExtractMetadata.classes import MusicManager, SearchProcessor
from threading import Lock
import os

class Application(QtCore.QObject):
    windows = {}
    def __init__(self, app):
        QtCore.QObject.__init__(self)
        self.app = app
        self.folder = ""
        self.collections = []
        self.path = None
        self.manager = None
        self.LoadCollections()
        self.load_windows()

    def loadPath(self):
        try:
            fob = open(".path", 'r')
            self.path = fob.read()
            fob.close()
        except:
            pass

    def setup_startup(self):
        self.windows["startup"].show()
        self.windows["startup"].load(self.collections)
        

    def start(self):
        self.setup_startup()

        if len(self.collections) > 0:
            self.loadFolder(self.collections[-1])

        try:
            self.loadPath()
            setup_lilypond(path=self.path)
        except LilypondNotInstalledException as e:
            self.windows["setup"].show()

    def loadPieces(self, method="title", slot=None):
        worker = qt_threading.mythread(self, self.manager.getPieceSummaryStrings, (method,))
        QtCore.QObject.connect(worker, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        worker.run()

    def getPlaylistFileInfo(self, playlist):
        return self.manager.getPlaylistFileInfo(playlist)

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

        setup = SetupWindow.SetupWindow(self)
        self.windows["setup"] = setup
        self.windows["setup"].show()
        self.windows["setup"].hide()

    def onQueryComplete(self, data, online=False):
        """
        Async callback which will send the results of a query back to the main window as the user
        types stuff in
        :param data: the results of the query
        :param online: bool indicator of whether files are online or local
        :return: None, calls the handler inside main window
        """
        lock = Lock()
        lock.acquire()
        query_results = {}
        if online:
            query_results["Online"] = data
        else:
            query_results["Offline"] = data
        self.windows["main"].onQueryReturned(query_results)
        lock.release()

    def queryNotThreaded(self, input):
        """
        Method which does the querying for adding pieces to playlists without using threads.
        exists because pyqt fell over when threading

        :return:
        """
        data = SearchProcessor.process(input)
        results = self.manager.runQueries(data)
        return results

    def query(self, input, playlist=False):
        """
        Async method which will process the given input, create thread classes
        for each type of query and then start those thread classes. When done they will call
        the callback above
        :param input: text input from the main window
        :return: None, thread classes will call the callback above
        """
        data = SearchProcessor.process(input)
        OfflineThread = qt_threading.QueryThread(self, self.manager.runQueries, (data,), False)
        QtCore.QObject.connect(OfflineThread, QtCore.SIGNAL("dataReady(PyQt_PyObject, bool)"), self.onQueryComplete)
        OfflineThread.run()
        OnlineThread = qt_threading.QueryThread(self, self.manager.runQueries, (data,), True)
        QtCore.QObject.connect(OnlineThread, QtCore.SIGNAL("dataReady(PyQt_PyObject, bool)"), self.onQueryComplete)
        OnlineThread.run()
        # data_queue = queue.Queue()
        # OnlineThread = thread_classes.Async_Handler_Queue(self.manager.runQueries,
        #                                                   self.onQueryComplete,
        #     data_queue, (data,), kwargs={"online": True})
        # OnlineThread.execute()






    def updateDb(self):
        worker = qt_threading.mythread(self, self.manager.refresh, ())
        worker.run()


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

    def copyFiles(self, fnames):
        self.manager.copyFiles(fnames)
        self.updateDb()

app = QtGui.QApplication(sys.argv)
application = Application(app)
application.start()
sys.exit(app.exec_())
