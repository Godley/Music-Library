from PyQt4 import QtCore, QtGui
import sys
from implementation.primaries.GUI import StartupWidget, MainWindow
from implementation.primaries.ExtractMetadata.classes import MusicManager

class Application(object):
    def __init__(self):
        self.startup = StartupWidget.Startup(self)
        self.startup.show()
        self.manager = None
        self.main = None
        self.folder = ""


    def FolderFetched(self, foldername):
        self.folder = foldername
        if self.folder != "":
            self.startup.close()
            self.setupMainWindow()

    def setupMainWindow(self):
        self.manager = MusicManager.MusicManager(folder=self.folder)
        self.updateDb()
        self.main = MainWindow.MainWindow(self)
        self.main.show()

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
