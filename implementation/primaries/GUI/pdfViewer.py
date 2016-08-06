from PyQt4 import QtGui, QtCore
import sys
if sys.platform == "darwin":
    from popplerqt4 import Poppler
import math

class PDFViewer(object):
    def setPDF(self, pdf):
        self.pdf_filepath = pdf
        self.doc = Poppler.Document.load(self.pdf_filepath)
        self.doc.setRenderHint(Poppler.Document.Antialiasing)
        self.doc.setRenderHint(Poppler.Document.TextAntialiasing)

    def getNumPages(self):
        return self.doc.numPages()

    def getNumGroups(self):
        pages = self.getNumPages()
        pairings = (pages + 1) // 2
        return pairings

    def getPageLabel(self, number):
        page = self.doc.page(number)

        if page is not None:
            image = page.renderToImage(100, 100)
            pixmap = QtGui.QPixmap.fromImage(image)
            pageSize = self.getPageSize(number)
            container = QtGui.QLabel()
            container.setFixedSize(pageSize)
            container.setStyleSheet("pages[number] { background-color : transparent}")
            container.setContentsMargins(0, 0, 0, 0)
            container.setScaledContents(True)
            container.setPixmap(pixmap)
            return container

        return page


    def getEmptyPage(self):
        page = QtGui.QLabel()
        pageSize = self.getPageSize(0)
        page.setFixedSize(pageSize)
        page.setStyleSheet("Page { background-color : transparent}")
        page.setContentsMargins(0, 0, 0, 0)
        page.setScaledContents(True)
        pixmap = QtGui.QPixmap()
        page.setPixmap(pixmap)
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
        layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        layout.setContentsMargins(0, 0, 0, 0)
        groups = self.getNumGroups()
        for group in range(groups):
            pair_scene = QtGui.QGraphicsScene()
            pair_layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Horizontal)
            for i in range(group * 2, group * 2 + 2):
                page = self.getPageLabel(i)
                if page is None:
                    page = self.getEmptyPage()
                pair_layout.addItem(pair_scene.addWidget(page))
            layout.addItem(pair_layout)

        graphicsWidget = QtGui.QGraphicsWidget()
        graphicsWidget.setLayout(layout)
        scene.addItem(graphicsWidget)
        return scene

