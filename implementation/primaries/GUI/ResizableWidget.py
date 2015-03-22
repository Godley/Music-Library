from PyQt4.QtGui import *
from PyQt4.QtCore import SIGNAL, SLOT
from PyQt4.QtDesigner import QPyDesignerCustomWidgetPlugin, QExtensionFactory, QPyDesignerTaskMenuExtension, QDesignerFormWindowInterface

class ResizeableWidget(QWidget):
  def __init__(self, title="", parent = None):

     QWidget.__init__(self, parent)

     self.titleLabel = QLabel(self.tr(title))
     self.xButton_drop = QPushButton()
     self.xButton_drop.move(2,2)
     self.xButton = QPushButton()
     self.xButton.move(0,0)

     self.xButton.connect(self.hide)

class ResizeableWidgetPlugin(QPyDesignerCustomWidgetPlugin):

   def __init__(self, parent = None):

      QPyDesignerCustomWidgetPlugin.__init__(self)
      self.initialized = False

   def initialize(self, formEditor):
       if self.initialized:
              return

       manager = formEditor.extensionManager()
       if manager:
            self.factory = \
            ResizeableWidgetTaskMenuFactory(manager)
            manager.registerExtensions(
            self.factory,
            "com.trolltech.Qt.Designer.TaskMenu")

       self.initialized = True

   def createWidget(self, parent):
       return ResizeableWidget(parent)

   def name(self):
       return "ResizeableWidget"

   def includeFile(self):
       return "QQ_Widgets.resizeablewidget"

class ResizeableWidgetMenuEntry(QPyDesignerTaskMenuExtension):

  def __init__(self, widget, parent):

      QPyDesignerTaskMenuExtension.__init__(self, parent)

      self.widget = widget
      self.editStateAction = QAction(
          self.tr("Update Location..."), self)
      self.connect(self.editStateAction,
          SIGNAL("triggered()"), self.updateLocation)

  def preferredEditAction(self):
      return self.editStateAction

  def taskActions(self):
      return [self.editStateAction]

  def updateLocation(self):
      dialog = ResizeableWidgetDialog(self.widget)
      dialog.exec_()

class ResizeableWidgetDialog(QDialog):

   def __init__(self, widget, parent = None):

      QDialog.__init__(self, parent)

      self.widget = widget

      self.previewWidget = ResizeableWidget()
      self.previewWidget.latitude = widget.latitude
      self.previewWidget.longitude = widget.longitude

      buttonBox = QDialogButtonBox()
      okButton = buttonBox.addButton(buttonBox.Ok)
      cancelButton = \
         buttonBox.addButton(buttonBox.Cancel)

      self.connect(okButton, SIGNAL("clicked()"),
                   self.updateWidget)
      self.connect(cancelButton, SIGNAL("clicked()"),
                   self, SLOT("reject()"))

      layout = QGridLayout()
      layout.addWidget(self.previewWidget, 1, 0, 1, 2)
      layout.addWidget(buttonBox, 2, 0, 1, 2)
      self.setLayout(layout)

      self.setWindowTitle(self.tr("Update Location"))

   def updateWidget(self):

      formWindow = \
        QDesignerFormWindowInterface.findFormWindow(
            self.widget)

      self.accept()

class ResizeableWidgetTaskMenuFactory(QExtensionFactory):

  def __init__(self, parent = None):

      QExtensionFactory.__init__(self, parent)

  def createExtension(self, obj, iid, parent):

      if iid != "com.trolltech.Qt.Designer.TaskMenu":
          return None

      if isinstance(obj, ResizeableWidget):
          return ResizeableWidgetMenuEntry(obj, parent)

      return None


