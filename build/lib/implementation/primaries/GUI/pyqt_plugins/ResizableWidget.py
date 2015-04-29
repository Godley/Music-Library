from PyQt4.QtGui import *


class ResizeableWidget(QWidget):
  def __init__(self, title="", parent = None):

     QWidget.__init__(self, parent)

     self.titleLabel = QLabel(self.tr(title))
     self.xButton_drop = QPushButton()
     self.xButton_drop.move(2,2)
     self.xButton = QPushButton()
     self.xButton.move(0,0)

     self.xButton.connect(self.hide)

