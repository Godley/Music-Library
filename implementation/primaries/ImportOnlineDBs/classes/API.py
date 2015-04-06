import os

class Api(object):
    def __init__(self, folder=""):
        self.folder = folder

    def downloadFile(self, fname):
        raise NotImplementedError

    def getCollection(self):
        raise NotImplementedError

    def searchForAnyMatch(self, filters):
        raise NotImplementedError

    def searchForExactMatch(self, filters):
        raise NotImplementedError