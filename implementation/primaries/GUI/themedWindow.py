import os
from implementation.primaries.GUI.helpers import parseStyle, postProcessLines


class ThemedWindow(object):

    def __init__(self, theme, themes_folder):
        self.theme = theme
        self.folder = themes_folder

    def applyTheme(self):
        file = os.path.join(self.folder, self.theme + ".qss")
        if os.path.exists(file):
            file_object = open(file, 'r')
            lines = file_object.readlines()
            file_object.close()
            self.setStyleSheet(postProcessLines(parseStyle(lines, self.theme, self.folder)))

    def setTheme(self, theme):
        self.theme = theme
