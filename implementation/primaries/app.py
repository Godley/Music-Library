import sys
from PyQt4.QtGui import QApplication, QMainWindow
from PyQt4.QtCore import QTimer
from implementation.primaries.GUI import MainWindow
from implementation.main import Application

if __name__ == "__main__":
    app = QApplication(sys.argv)

    application = Application(app)
    sys.exit(app.exec_())

