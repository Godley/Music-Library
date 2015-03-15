from PyQt4 import QtCore, QtGui
import sys
import pickle
from implementation.primaries.GUI import StartupWidget, MainWindow
from implementation.primaries.ExtractMetadata.classes import MusicManager

class Application(object):
    def __init__(self):
        self.previous_collections = []
        self.col_file = ".collections"
        self.getPreviousCollections()
        self.SaveCollections()
        self.startup = StartupWidget.Startup(self)
        self.startup.show()
        self.manager = None
        self.main = None
        self.folder = ""


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

    def loadFile(self, filename):
        '''
        This method should:
        - setup a renderer object
        - run it
        - return the pdf location
        :return: filename of generated pdf
        '''
        pass

    def updateDb(self):
        self.manager.refresh()

    def loadPieces(self, method="title"):
        summary_strings = self.manager.getPieceSummaryStrings(method)
        return summary_strings

    def loadPlaylists(self):
        pass


def main():

    app = QtGui.QApplication(sys.argv)

    app_obj = Application()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
