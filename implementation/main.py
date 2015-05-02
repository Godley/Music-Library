from PyQt4 import QtCore, QtGui
import sys, os, pickle, queue
from threading import Lock
from xml.sax._exceptions import *
import os, sip
from PyQt4 import QtXml
from implementation.primaries.GUI.helpers import get_base_dir
from implementation.primaries.GUI import StartupWidget, qt_threading, thread_classes, MainWindow, PlaylistDialog, licensePopup, renderingErrorPopup, ImportDialog
from implementation.primaries.ExtractMetadata.classes import MusicManager, SearchProcessor
from implementation.primaries.Drawing.classes import LilypondRender, MxmlParser, Exceptions

class Application(QtCore.QObject):

    def __init__(self, app):

        QtCore.QObject.__init__(self, app)
        self.app = app
        self.previous_collections = []
        self.col_file = os.path.join(get_base_dir(), ".collections")
        self.getPreviousCollections()
        self.SaveCollections()
        self.manager = None
        self.main = None
        self.folder = ""
        self.theme = "dark"
        if len(self.previous_collections) == 0:
            self.startUp()
        else:
            self.folder = self.previous_collections[-1]
            self.setupMainWindow()

    def startUp(self):
        self.folder = ""
        self.startup = StartupWidget.Startup(self)
        self.startup.show()

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
            self.startup.close()
            print("closed")
            self.setupMainWindow()

    def setupMainWindow(self):
        self.manager = MusicManager.MusicManager(self, folder=self.folder)

        self.main = MainWindow.MainWindow(self)
        self.main.show()
        self.manager.runApiOperation()
        self.updateDb()
        self.main.runLoadingProcedure()

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
        self.main.onPieceLoaded(fqd_fname, filename)

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
            self.main.onPieceLoaded(pdf, filename)

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
                self.licensePopup = licensePopup.LicensePopup(self, license, filename, self.theme)
                self.licensePopup.setWindowFlags(QtCore.Qt.Dialog)
                self.licensePopup.exec()
            else:
                render_thread = qt_threading.RenderThread(self, self.startRenderingTask,
                                                            (filename,), pdf_version)
                QtCore.QObject.connect(render_thread, QtCore.SIGNAL("fileReady(PyQt_PyObject, PyQt_PyObject)"), self.onRenderTaskFinished)
                render_thread.run()


    def importPopup(self):
        dialog = ImportDialog.ImportDialog(self, self.theme)
        dialog.setWindowFlags(QtCore.Qt.Dialog)
        dialog.exec()

    def copyFiles(self, fnames):
        self.manager.copyFiles(fnames)
        self.updateDb()
        self.main.onSortMethodChange()
        self.main.loadPlaylists()

    def errorPopup(self, errors):
        popup = renderingErrorPopup.RenderingErrorPopup(
            self,
            errors,
            self.theme)
        popup.setWindowFlags(QtCore.Qt.Dialog)
        popup.exec()

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
        self.main.onQueryReturned(query_results)
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




    def startRenderingTask(self, fname):
        """
        method which parses a piece, then runs the renderer class on it which takes the lilypond
        output, runs lilypond on it and gets the pdf. This is not generally called directly,
        but rather called by a thread class in thread_classes.py
        :param fname: xml filename
        :return: list of problems encountered
        """
        errorList = []
        parser = MxmlParser.MxmlParser()
        piece_obj = None
        try:
            piece_obj = parser.parse(os.path.join(self.folder, fname))
        except Exceptions.DrumNotImplementedException as e:
            errorList.append(
                "Drum tab found in piece: this application does not handle drum tab.")
        except Exceptions.TabNotImplementedException as e:
            errorList.append(
                "Guitar tab found in this piece: this application does not handle guitar tab.")
        except SAXParseException as e:
            errorList.append("Sax parser had a problem with this file:"+str(e))
        if piece_obj is not None:
            try:
                loader = LilypondRender.LilypondRender(
                    piece_obj,
                    os.path.join(
                        self.folder,
                        fname))
                loader.run()
            except BaseException as e:
                errorList.append(str(e))
        return errorList

    def updateDb(self):
        self.manager.refresh()

    def makeNewCollection(self):
        self.main.close()
        self.startUp()

    def addPlaylist(self, data):
        self.manager.addPlaylist(data)

    def onPiecesLoad(self, summary_strings):
        self.main.onScorebookLoad(summary_strings)

    def loadPieces(self, method="title"):
        data_queue = queue.Queue()
        task = thread_classes.Async_Handler_Queue(self.manager.getPieceSummaryStrings,
                                                    self.onPiecesLoad,
                                                    data_queue,
                                                    (method,)
                                                    )
        task.execute()

    def onPlaylistsLoad(self, data):
        self.main.onPlaylistReady(data)

    def onUserPlaylistsLoad(self, data):
        self.main.onMyPlaylistsReady(data)

    def getPlaylists(self, select_method="all"):
        data_queue = queue.Queue()
        task = thread_classes.Async_Handler_Queue(self.manager.getPlaylists,
                                                  self.onPlaylistsLoad,
                                                  data_queue,
                                                (select_method,))
        task.execute()

    def getCreatedPlaylists(self):
        data_queue = queue.Queue()
        task = thread_classes.Async_Handler_Queue(self.manager.getPlaylistsFromPlaylistTable,
                                                  self.onUserPlaylistsLoad,
                                                  data_queue,
                                                ())
        task.execute()


    def PlaylistPopup(self):
        self.popup = PlaylistDialog.PlaylistDialog(self, self.theme)
        self.popup.setWindowFlags(QtCore.Qt.Dialog)
        self.popup.exec()

    def removePlaylists(self, playlists):
        self.manager.deletePlaylists(playlists)

    def updatePlaylistTitle(self, new_title, old_title):
        self.manager.updatePlaylistTitle(new_title, old_title)

    def loadPlaylists(self):
        pass


if __name__ == '__main__':
    sip.setdestroyonexit(True)
    app = QtGui.QApplication(sys.argv)
    app_obj = Application(app)

    sys.exit(app.exec_())
