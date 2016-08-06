from PyQt4 import QtGui, QtCore
import sys
if sys.platform == "darwin":
    from popplerqt4 import Poppler
import math

class PDFViewer(object):
    def __init__(self, width=None, pages=None):
        self.width = width
        self.pages = pages


    def setPDF(self, pdf):
        self.pdf_filepath = pdf
        self.doc = Poppler.Document.load(self.pdf_filepath)
        self.doc.setRenderHint(Poppler.Document.Antialiasing)
        self.doc.setRenderHint(Poppler.Document.TextAntialiasing)

    def getNumPages(self):
        return self.doc.numPages()

    def getPageWidth(self, number):
        return self.doc.page(number).pageSize().width()

    def getNumGroups(self):
        pages = self.getNumPages()
        pairings = (pages + 1) // 2
        return pairings

    def getPageLabel(self, number):
        page = self.doc.page(number)

        if page is not None:
            image = page.renderToImage(100, 100)
            pixmap = QtGui.QPixmap.fromImage(image)
            container = QtGui.QLabel()
            if self.width is None:
                self.width = pixmap.width()
            container.setFixedWidth(self.width)
            container.setStyleSheet("pages[number] { background-color : transparent}")
            container.setContentsMargins(0, 0, 0, 0)
            container.setScaledContents(True)
            container.setPixmap(pixmap)
            return container

        return page

    def getPageSize(self, number):
        page = self.doc.page(number)
        pageSize = page.pageSize()
        return pageSize

    def setGroupLength(self, number):
        self.group = number

    def getScene(self):
        scene = QtGui.QGraphicsScene()
        scene.setBackgroundBrush(QtGui.QColor('transparent'))
        layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
        layout.setContentsMargins(0, 0, 0, 0)
        pages = self.getNumPages()
        for n in range(pages):
            page = self.getPageLabel(n)
            layout.addItem(scene.addWidget(page))

        graphicsWidget = QtGui.QGraphicsWidget()
        graphicsWidget.setLayout(layout)
        scene.addItem(graphicsWidget)
        return scene

