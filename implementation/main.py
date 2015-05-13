from PyQt4 import QtCore, QtGui
import sys, os, pickle, queue
from threading import Lock
from xml.sax._exceptions import *
import os, sip
from PyQt4 import QtXml
from implementation.primaries.GUI.helpers import get_base_dir
from implementation.primaries.scripts.setup_script import setup_lilypond
from implementation.primaries.exceptions import LilypondNotInstalledException
from implementation.primaries.GUI import StartupWidget, qt_threading, thread_classes, MainWindow, SetupWindow, PlaylistDialog, licensePopup, renderingErrorPopup, ImportDialog
from implementation.primaries.ExtractMetadata.classes import MusicManager, SearchProcessor


class Application(QtCore.QObject):
    windows = {}
    def __init__(self, parent):
        QtCore.QObject.__init__(self)
        self.parent = parent
        self.previous_collections = []
        self.col_file = os.path.join(get_base_dir(), ".collections")
        self.getPreviousCollections()
        self.SaveCollections()
        self.manager = None
        self.folder = ""
        self.theme = "light"
        self.script = os.path.join(get_base_dir(), "scripts", "lilypond")

        self.setup_windows()

    def start(self):
        self.loadAndHideWindows()

        self.windows["startup"].show()
        self.windows["startup"].load(self.previous_collections)
        if len(self.previous_collections) > 0:
            self.folder = self.previous_collections[-1]
            self.setupMain()
        try:
            setup_lilypond()
        except LilypondNotInstalledException as e:
            self.windows["setup"].show()
            self.windows["setup"].load()

    def loadAndHideWindows(self):
        self.windows["playlist"].load()
        self.windows["playlist"].show()
        self.windows["playlist"].hide()
        #self.windows["import"].load()
        self.windows["import"].show()
        self.windows["import"].hide()
        self.windows["error"].load([])
        self.windows["error"].show()
        self.windows["error"].hide()
        self.windows["license"].load("", None)
        self.windows["license"].show()
        self.windows["license"].hide()


    def show_start(self):
        self.windows["startup"].show()
        self.windows["startup"].load(self.previous_collections)

    def show_playlist(self):
        self.windows["playlist"].show()



    def setup_windows(self):
        startup = StartupWidget.StartupWindow(self)
        self.windows["startup"] = startup

        main = MainWindow.MainWindow(self, self.theme)
        self.windows["main"] = main
        self.windows["main"].show()

        setup = SetupWindow.SetupWindow(self)
        self.windows["setup"] = setup

        self.windows["playlist"] = PlaylistDialog.PlaylistDialog(self, self.theme)
        self.windows["import"] = ImportDialog.ImportDialog(self, self.theme)
        self.windows["error"] = renderingErrorPopup.RenderingErrorPopup(self, self.theme)
        self.windows["license"] = licensePopup.LicensePopup(self, self.theme)


    def setUp(self):
        try:
            setup_lilypond()
        except LilypondNotInstalledException as e:
            self.setup_win = SetupWindow.SetupWindow(self)
            self.setup_win.show()

    def removeCollection(self, folder):
        if os.path.exists(os.path.join(folder, "music.db")):
            os.remove(os.path.join(folder, "music.db"))
        self.previous_collections.remove(folder)
        self.SaveCollections()

    def getPreviousCollections(self):
        try:
            col_fob = open(self.col_file, 'rb')
        except:
            self.SaveCollections()
            col_fob = open(self.col_file, 'rb')
        result_temp = pickle.load(col_fob)
        if result_temp is not None:
            self.previous_collections = result_temp
        return self.previous_collections

    def SaveCollections(self):
        col_fob = open(self.col_file, 'wb')
        pickle_obj = pickle.Pickler(col_fob)
        pickle_obj.dump(self.previous_collections)

    def addFolderToCollectionList(self, name):
        if name not in self.previous_collections:
            self.previous_collections.append(name)

    def FolderFetched(self, foldername):
        self.folder = foldername
        if self.folder != "":
            self.addFolderToCollectionList(foldername)
            self.SaveCollections()
            self.setupMain()

    def setupMain(self):
        self.manager = MusicManager.MusicManager(self, folder=self.folder)
        self.manager.refresh()
        self.windows["main"].setup()
        self.windows["startup"].hide()
        self.windows["main"].show()
        self.windows["main"].runLoadingProcedure()



    def getPlaylistFileInfo(self, playlist):
        return self.manager.getPlaylistFileInfo(playlist)

    def getFileInfo(self, filename):
        file_info = self.manager.getFileInfo(filename)
        return file_info

    def loadUserPlaylistsForAGivenFile(self, filename):
        data = self.manager.getPlaylistByFilename(filename)
        return data

    def onFileDownload(self, filename):
        fqd_fname = os.path.join(self.folder, filename)
        self.windows["main"].onPieceLoaded(fqd_fname, filename)

    def onRenderError(self, error):
        self.errorPopup([str(error)])

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
        QtCore.QObject.connect(async, QtCore.SIGNAL("fileReady(PyQt_PyObject)"), self.onFileDownload)
        QtCore.QObject.connect(async, QtCore.SIGNAL("downloadError(bool)"), self.onFileError)
        async.run()

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





    def copyFiles(self, fnames):
        self.manager.copyFiles(fnames)
        self.updateDb()
        self.windows["main"].onSortMethodChange()
        self.windows["main"].loadPlaylists()

    def errorPopup(self, errors):
        self.windows["error"].show()
        self.windows["error"].load(errors)

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
        data_queue = queue.Queue()
        OfflineThread = thread_classes.Async_Handler_Queue(self.manager.runQueries,
                                                           self.onQueryComplete,
            data_queue, (data,))
        OnlineThread = thread_classes.Async_Handler_Queue(self.manager.runQueries,
                                                          self.onQueryComplete,
            data_queue, (data,), kwargs={"online": True})
        OfflineThread.execute()
        OnlineThread.execute()






    def updateDb(self):
        self.manager.refresh()

    def makeNewCollection(self):
        self.windows["main"].close()
        self.startUp()

    def addPlaylist(self, data):
        self.manager.addPlaylist(data)

    def onPiecesLoad(self, summary_strings):
        self.windows["main"].onScorebookLoad(summary_strings)

    def loadPieces(self, method="title"):
        worker = qt_threading.mythread(self, self.manager.getPieceSummaryStrings, (method,))
        QtCore.QObject.connect(worker, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), self.onPiecesLoad)
        worker.run()

    def onPlaylistsLoad(self, data):
        self.windows["main"].onPlaylistReady(data)

    def onUserPlaylistsLoad(self, data):
        self.windows["main"].onMyPlaylistsReady(data)

    def getPlaylists(self, select_method="all"):
        async = qt_threading.mythread(self, self.manager.getPlaylists, (select_method,))
        QtCore.QObject.connect(async, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), self.onPlaylistsLoad)
        async.run()

    def getCreatedPlaylists(self):
        async = qt_threading.mythread(self, self.manager.getPlaylistsFromPlaylistTable, ())
        QtCore.QObject.connect(async, QtCore.SIGNAL("dataReady(PyQt_PyObject)"), self.onUserPlaylistsLoad)
        async.run()




    def removePlaylists(self, playlists):
        self.manager.deletePlaylists(playlists)

    def updatePlaylistTitle(self, new_title, old_title):
        self.manager.updatePlaylistTitle(new_title, old_title)

    def loadPlaylists(self):
        pass

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)

    application = Application(app)
    application.start()
    sys.exit(app.exec_())

