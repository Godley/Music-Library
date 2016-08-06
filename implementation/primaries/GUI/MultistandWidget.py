import sip
import os
from sys import platform
if platform == "darwin":
    from popplerqt4 import Poppler

from PyQt4 import QtGui, QtCore, uic

from implementation.primaries.GUI.helpers import get_base_dir, parseStyle
from implementation.primaries.GUI import themedWindow, Widgets
from implementation.primaries.GUI import pdfViewer


class MultistandWidget(QtGui.QWidget, themedWindow.ThemedWindow):

    def __init__(self, file, theme_folder, theme):
        QtGui.QWidget.__init__(self)
        themedWindow.ThemedWindow.__init__(self, theme, theme_folder)
        self.pages = 2
        self.file = file
        self.load()
        self.viewer = pdfViewer.PDFViewer(width=None)
        self.loadPdfToGraphicsWidget(file)
        self.move(0, 0)


    def load(self):
        design_file = os.path.join(
            get_base_dir(True), "designer_files", "MultiStandWidget.ui")
        uic.loadUi(design_file, self)
        self.setWindowTitle("MuseLib Multistand View: " + self.file)
        self.pageValue.valueChanged.connect(self.pageValChanged)
        self.zoomInBtn.clicked.connect(self.zoomIn)
        self.zoomOutBtn.clicked.connect(self.zoomOut)

    def zoomIn(self):
        self.scoreWindow.scale(1.1, 1.1)

    def zoomOut(self):
        self.scoreWindow.scale(0.9, 0.9)

    def loadPdfToGraphicsWidget(self, filename):
        """
        sets up the graphics view with pairs of pages
        :param filename: pdf file to load
        :return:
        """
        self.viewer.setPDF(filename)
        scene = self.scoreWindow.scene()
        if scene is not None:
            scene.clear()
        scene = self.viewer.getScene()
        self.scoreWindow.setScene(scene)

    def pageValChanged(self, pageVal):
        self.pages = pageVal
        width = self.viewer.getPageWidth(0) * self.pages
        self.scoreWindow.setFixedWidth(width)
        self.setFixedWidth(width)


