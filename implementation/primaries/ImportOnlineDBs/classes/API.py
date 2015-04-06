import os

class Api(object):
    def __init__(self, folder=""):
        self.folder = folder

    def downloadFile(self, fname):
        return os.path.join(self.folder, fname)

    def getCollection(self):
        return []

    def searchForAnyMatch(self, filters):
        return []

    def searchForExactMatch(self, filters):
        return []