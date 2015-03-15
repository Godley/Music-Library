from PyQt4 import QtCore, QtGui, uic
import sys
from implementation.primaries.GUI import StartupWidget, MainWindow

class Application(object):
    def __init__(self):
        self.startup = StartupWidget.Startup(self)
        self.startup.show()
        self.main = MainWindow.MainWindow()

    def FolderFetched(self, foldername):
        self.folder = foldername
        self.startup.close()
        self.main.folder = self.folder
        self.main.show()

def main():

    app = QtGui.QApplication(sys.argv)

    app_obj = Application()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
