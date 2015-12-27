from threading import Lock
import sys
import os
import pickle
from xml.parsers import expat
from PyQt4 import QtGui, QtCore, QtXml

from implementation.primaries.GUI import renderingErrorPopup, SetupWindow, qt_threading, PlaylistDialog, ImportDialog, licensePopup, \
    StartupWindow, MainWindow
from implementation.primaries.ExtractMetadata.classes import MusicManager, SearchProcessor
from implementation.primaries.scripts.setup_script import do_setup
from implementation.primaries.exceptions import LilypondNotInstalledException
from implementation.primaries.GUI.helpers import get_base_dir


class Application(QtCore.QObject):
    windows = {}

    def __init__(self, app):
        QtCore.QObject.__init__(self)
        self.meta = {}
        self.meta["collections"] = []
        self.theme_folder = os.path.join(get_base_dir(True), "themes")
        self.meta["theme"] = "ubuntu"
        self.meta["path"] = None
        self.LoadMeta()
        self.folder = None
        self.load_windows()

    def meta_file(self):
        return os.path.join(os.path.expanduser("~"), ".musiclib")

    def start(self):
        if len(self.meta["collections"]) > 0:
            self.loadFolder(self.meta["collections"][-1])
        else:
            self.setup_startup()

        try:
            do_setup(path=self.meta["path"])
        except LilypondNotInstalledException as e:
            self.windows["setup"].show()

    def loadFolder(self, folder):
        self.folder = folder
        self.manager = MusicManager.MusicManager(self, folder=self.folder)
        self.windows["main"].show()
        if not hasattr(self.windows["main"], "contentFrame"):
            self.windows["main"].load()
            self.windows["main"].themeSet = False

    def removeCollection(self, folder):
        if folder in self.meta["collections"]:
            self.meta["collections"].remove(folder)
        self.SaveMeta()

    def createNewPlaylist(self):
        self.windows["newplaylist"].load()
        self.windows["newplaylist"].show()

    def addPlaylist(self, data):
        self.manager.addPlaylist(data)

    def removePlaylists(self, playlists):
        self.manager.deletePlaylists(playlists)

    def FolderFetched(self, folder):
        if folder is not None:
            if folder not in self.meta["collections"]:
                self.meta["collections"].append(folder)
            self.SaveMeta()
            self.LoadMeta()
            self.loadFolder(folder)

    def LoadMeta(self):
        try:
            col_fob = open(self.meta_file(), 'rb')
        except:
            self.SaveMeta()
            col_fob = open(self.meta_file(), 'rb')
        result_temp = pickle.load(col_fob)
        if result_temp is not None:
            if "collections" in result_temp:
                for item in result_temp["collections"]:
                    if item not in self.meta["collections"]:
                        if os.path.exists(item):
                            self.meta["collections"].append(item)
            if "path" in result_temp:
                self.meta["path"] = result_temp["path"]
            if "theme" in result_temp:
                self.meta["theme"] = result_temp["theme"]
        return self.meta

    def SaveMeta(self):
        col_fob = open(self.meta_file(), 'wb')
        pickle_obj = pickle.Pickler(col_fob)
        pickle_obj.dump(self.meta)
        col_fob.close()

    def load_windows(self):
        startup = StartupWindow.StartupWindow(
            self, self.meta["theme"], self.theme_folder)
        self.windows["startup"] = startup

        main = MainWindow.MainWindow(
            self, self.meta["theme"], self.theme_folder)
        self.windows["main"] = main
        self.windows["main"].show()
        self.windows["main"].applyTheme()
        self.windows["main"].hide()

        setup = SetupWindow.SetupWindow(
            self, self.meta["theme"], self.theme_folder)
        self.windows["setup"] = setup
        self.windows["setup"].show()
        self.windows["setup"].hide()

        self.windows["error"] = renderingErrorPopup.RenderingErrorPopup(
            self, self.meta["theme"], self.theme_folder)
        self.windows["error"].show()
        self.windows["error"].hide()

        self.windows["import"] = ImportDialog.ImportDialog(
            self, self.meta["theme"], self.theme_folder)
        self.windows["import"].show()
        self.windows["import"].hide()

        self.windows["newplaylist"] = PlaylistDialog.PlaylistDialog(
            self, self.meta["theme"], self.theme_folder)
        self.windows["newplaylist"].show()
        self.windows["newplaylist"].hide()

        self.windows["license"] = licensePopup.LicensePopup(
            self, self.meta["theme"], self.theme_folder)
        self.windows["license"].show()
        self.windows["license"].hide()

    def updateTheme(self, theme):
        for window in self.windows:
            self.windows[window].theme = theme
        self.meta["theme"] = theme
        self.SaveMeta()

    def onFileDownload(self, filename):
        fqd_fname = os.path.join(self.folder, filename)
        self.windows["main"].onPieceLoaded(fqd_fname, filename)

    def onFileError(self, error):
        self.errorPopup(["Problem with internet connection on file download"])

    def downloadFile(self, filename):
        """
        method which starts a thread to get a file from an API server, this gets called
        by license window when a user presses "ok"
        :param filename: xml file name not including current folder
        :return: None, thread will call a method to pass back the result
        """
        async = qt_threading.DownloadThread(self, self.manager.downloadFile,
                                            filename)
        QtCore.QObject.connect(
            async, QtCore.SIGNAL("fileReady(PyQt_PyObject)"), self.onFileDownload)
        QtCore.QObject.connect(
            async, QtCore.SIGNAL("downloadError(bool)"), self.onFileError)
        async.run()

    def loadPieces(self, method="title", slot=None):
        worker = qt_threading.mythread(
            self, self.manager.getPieceSummaryStrings, (method,))
        QtCore.QObject.connect(
            worker, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        worker.run()

    def setup_startup(self):
        self.windows["startup"].load(self.meta["collections"])
        self.windows["startup"].show()

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
        if len(data) > 0:
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
        OfflineThread = qt_threading.QueryThread(
            self, self.manager.runQueries, (data,), False)
        QtCore.QObject.connect(OfflineThread, QtCore.SIGNAL(
            "dataReady(PyQt_PyObject, bool)"), self.onQueryComplete)
        OfflineThread.run()
        OnlineThread = qt_threading.QueryThread(
            self, self.manager.runQueries, (data,), True)
        QtCore.QObject.connect(OnlineThread, QtCore.SIGNAL(
            "dataReady(PyQt_PyObject, bool)"), self.onQueryComplete)
        OnlineThread.run()
        # data_queue = queue.Queue()
        # OnlineThread = thread_classes.Async_Handler_Queue(self.manager.runQueries,
        #                                                   self.onQueryComplete,
        #     data_queue, (data,), kwargs={"online": True})
        # OnlineThread.execute()

    def getFileInfo(self, filename):
        file_info = self.manager.getFileInfo(filename)
        return file_info

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
                self.windows["license"].show()
                self.windows["license"].load(license, filename)

            else:
                render_thread = qt_threading.RenderThread(self, self.manager.startRenderingTask,
                                                          (filename,), pdf_version)
                QtCore.QObject.connect(render_thread, QtCore.SIGNAL(
                    "fileReady(PyQt_PyObject, PyQt_PyObject)"), self.onRenderTaskFinished)
                QtCore.QObject.connect(render_thread, QtCore.SIGNAL(
                    "renderingError(PyQt_PyObject)"), self.onRenderError)
                render_thread.run()

    def onRenderError(self, error):
        self.errorPopup([str(error)])

    def errorPopup(self, errors):
        self.windows["error"].show()
        self.windows["error"].load(errors)

    def getCreatedPlaylists(self, slot=None):
        async = qt_threading.mythread(
            self, self.manager.getPlaylistsFromPlaylistTable, ())
        QtCore.QObject.connect(
            async, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        async.run()

    def getPlaylists(self, select_method="all", slot=None):
        async = qt_threading.mythread(
            self, self.manager.getPlaylists, (select_method,))
        QtCore.QObject.connect(
            async, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), slot)
        async.run()

    def getPlaylistFileInfo(self, playlist):
        return self.manager.getPlaylistFileInfo(playlist)

    def updateDb(self):
        worker = qt_threading.mythread(self, self.manager.refresh, ())
        worker.run()

    def importWindow(self):
        self.windows["import"].show()

    def copyFiles(self, fnames):
        self.manager.copyFiles(fnames)
        self.updateDb()

    def loadUserPlaylistsForAGivenFile(self, filename):
        data = self.manager.getPlaylistByFilename(filename)
        return data

    def applyTheme(self):
        for window in self.windows:
            self.windows[window].applyTheme()


app = QtGui.QApplication(sys.argv)
application = Application(app)
application.start()
# event = QtGui.QMouseEvent(QtCore.QEvent.MouseButtonPress, QtCore.QPoint(0,0), QtCore.Qt.MiddleButton)
# app.sendEvent(application, event)
# application.applyTheme()
timer = QtCore.QTimer()
timer.singleShot(1, application.applyTheme)
sys.exit(app.exec_())
