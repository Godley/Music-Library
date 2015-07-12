import sip, os
from sys import platform
if platform == "darwin":
    from popplerqt4 import Poppler

from PyQt4 import QtGui, QtCore, uic

from implementation.primaries.GUI.helpers import get_base_dir, parseStyle
from implementation.primaries.GUI import themedWindow, Widgets
from implementation.primaries.GUI import Widgets
from implementation.primaries.GUI import qt_threading


class MultistandWidget(QtGui.QWidget, themedWindow.ThemedWindow):
    def __init__(self, file):
        QtGui.QWidget.__init__(self)
        self.pages = 2
        self.file = file
        self.load()
        self.loadPdfToGraphicsWidget(file)
        self.move(0,0)

    def load(self):
        file = os.path.join(get_base_dir(True), "designer_files", "MultiStandWidget.ui")
        uic.loadUi(file, self)

        self.pageValue.valueChanged.connect(self.pageValChanged)

    def loadPdfToGraphicsWidget(self, filename):
        """
        sets up the graphics view with pairs of pages
        :param filename: pdf file to load
        :return:
        """

        scene = QtGui.QGraphicsScene()
        scene.setBackgroundBrush(QtGui.QColor('transparent'))
        layout = QtGui.QGraphicsLinearLayout(QtCore.Qt.Vertical)
        layout.setContentsMargins(0,0,0,0)
        doc = Poppler.Document.load(filename)
        doc.setRenderHint(Poppler.Document.Antialiasing)
        doc.setRenderHint(Poppler.Document.TextAntialiasing)


        pageNum = doc.numPages()
        number = 0
        scenes = []
        pairings = []
        pages = []
        images = []
        pixmaps = []
        containers = []
        labels = []

        while number < pageNum:
            scenes.append(QtGui.QGraphicsScene())
            pairings.append(QtGui.QGraphicsLinearLayout(QtCore.Qt.Horizontal))
            pages.append(doc.page(number))
            images.append(pages[number].renderToImage(100, 100))
            width = pages[number].pageSize().width()
            height = pages[number].pageSize().height()
            self.scoreWindow.setFixedWidth(width*self.pages)
            self.scoreWindow.setFixedHeight(height)

            self.resize(width*self.pages, height+50)
            pixmaps.append(QtGui.QPixmap.fromImage(images[number]))
            containers.append(QtGui.QLabel())
            containers[number].setFixedWidth(width)
            containers[number].setFixedHeight(pages[number].pageSize().height())
            #containers[number].setFixedSize(pages[number].pageSize())
            containers[number].setStyleSheet("pages[number] { background-color : transparent}")
            containers[number].setContentsMargins(0, 0, 0, 0)
            containers[number].setScaledContents(True)
            containers[number].setPixmap(pixmaps[number])
            labels.append(scenes[number].addWidget(containers[number]))
            pairings[number].addItem(labels[number])
            number += 1
            if number < pageNum:
                for i in range(1, self.pages):
                    pages.append(doc.page(i))
                    images.append(pages[i].renderToImage(100, 100))
                    pixmaps.append(QtGui.QPixmap.fromImage(images[i]))
                    containers.append(QtGui.QLabel())
                    containers[i].setFixedWidth(self.scoreWindow.width()/2)
                    containers[i].setFixedHeight(pages[number].pageSize().height())
                    #containers[number].setFixedSize(pages[number].pageSize())
                    containers[i].setStyleSheet("pages[number] { background-color : transparent}")
                    containers[i].setContentsMargins(0, 0, 0, 0)
                    containers[i].setScaledContents(True)
                    containers[i].setPixmap(pixmaps[number])
                    labels.append(scenes[number-1].addWidget(containers[i]))
                    pairings[number-1].addItem(labels[i])
                    if i >= pageNum:
                        break
                number += self.pages-1
            elif self.pages > 1:
                for i in range(number, self.pages):
                    containers.append(QtGui.QLabel())
                    containers[number].setFixedSize(pages[number-1].pageSize())
                    containers[number].setStyleSheet("pages[number] { background-color : transparent}")
                    containers[number].setContentsMargins(0, 0, 0, 0)
                    containers[number].setScaledContents(True)
                    pixmaps.append(QtGui.QPixmap())
                    containers[number].setPixmap(pixmaps[number])
                    labels.append(scenes[number-1].addWidget(containers[number]))
                    pairings[number-1].addItem(labels[number])
            layout.addItem(pairings[number-1])
            number += 1

        # use this to test that the layout works for more than 2 pages
        # while number < 3:
        #     scenes.append(QtGui.QGraphicsScene())
        #     pairings.append(QtGui.QGraphicsLinearLayout(QtCore.Qt.Horizontal))
        #     containers.append(QtGui.QLabel())
        #     containers[number].setFixedSize(pages[-1].pageSize())
        #     containers[number].setStyleSheet("pages[number] { background-color : transparent}")
        #     containers[number].setContentsMargins(0, 0, 0, 0)
        #     containers[number].setScaledContents(True)
        #     pixmaps.append(QtGui.QPixmap())
        #     containers[number].setPixmap(pixmaps[number])
        #     labels.append(scenes[-1].addWidget(containers[number]))
        #     pairings[-1].addItem(labels[number])
        #     layout.addItem(pairings[-1])
        #     number += 1

        graphicsWidget = QtGui.QGraphicsWidget()
        graphicsWidget.setLayout(layout)
        scene.addItem(graphicsWidget)
        self.scoreWindow.setScene(scene)

    def pageValChanged(self, pageVal):
        self.pages = pageVal
        self.loadPdfToGraphicsWidget(self.file)