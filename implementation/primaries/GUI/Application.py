from PyQt4 import QtCore, QtGui
import sys, os, pickle, threading, time
from implementation.primaries.GUI import StartupWidget, MainWindow, PlaylistDialog
from implementation.primaries.ExtractMetadata.classes import MusicManager, SearchProcessor
from implementation.primaries.Drawing.classes import LilypondRender, MxmlParser


class Application(object):
    def __init__(self):
        self.previous_collections = []
        self.col_file = ".collections"
        self.getPreviousCollections()
        self.SaveCollections()
        self.manager = None
        self.main = None
        self.folder = ""
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
            self.setupMainWindow()

    def setupMainWindow(self):
        self.manager = MusicManager.MusicManager(folder=self.folder)
        self.updateDb()
        self.main = MainWindow.MainWindow(self)
        self.main.show()

    def getPlaylistFileInfo(self, playlist):
        return self.manager.getPlaylistFileInfo(playlist)

    def getFileInfo(self, filename):
        file_info = self.manager.getFileInfo(filename)
        return file_info

    def loadFile(self, filename):
        '''
        This method should:
        - setup a renderer object
        - run it
        - return the pdf location
        :return: filename of generated pdf
        '''
        pdf_version = filename.split(".")[0]+".pdf"
        if os.path.exists(os.path.join(self.folder, pdf_version)):
            return os.path.join(self.folder, pdf_version)
        else:
            process = threading.Thread(target=self.startRenderingTask, args=(filename,))
            process.start()

            while process.isAlive() and not os.path.exists(os.path.join(self.folder, pdf_version)):
                self.main.updateProgressBar()
                time.sleep(1)
            process.join()
            return os.path.join(self.folder, pdf_version)

    def query(self, input):
        data = SearchProcessor.process(input)
        results = self.manager.runQueries(data)
        return results

    def startRenderingTask(self, filename):
        parser = MxmlParser.MxmlParser()
        piece_obj = parser.parse(os.path.join(self.folder,filename))
        loader = LilypondRender.LilypondRender(piece_obj, os.path.join(self.folder,filename))
        loader.run()

    def updateDb(self):
        self.manager.refresh()

    def addPlaylist(self, data):
        self.manager.addPlaylist(data)

    def loadPieces(self, method="title"):
        summary_strings = self.manager.getPieceSummaryStrings(method)
        return summary_strings

    def getPlaylists(self):
        results = self.manager.getPlaylists()
        return results

    def getCreatedPlaylists(self):
        results = self.manager.getPlaylistsFromPlaylistTable()
        return results

    def PlaylistPopup(self):
        popup = PlaylistDialog.PlaylistDialog(self)
        popup.setWindowFlags(QtCore.Qt.Popup)
        popup.exec()

    def updatePlaylistTitle(self, new_title, old_title):
        self.manager.updatePlaylistTitle(new_title, old_title)

    def loadPlaylists(self):
        pass


def main():

    app = QtGui.QApplication(sys.argv)

    app_obj = Application()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
