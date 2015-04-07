'''
A basic class which defines what methods sub classes must implement using exceptions.
If methods are not implemented and should be, the dev will know because it tips over.
'''

class Api(object):
    def __init__(self, folder=""):
        self.folder = folder

    def downloadFile(self, fname):
        raise NotImplementedError

    def getCollection(self):
        raise NotImplementedError

    def cleanCollection(self):
        raise NotImplementedError

    def search(self, filters):
        raise NotImplementedError

    def searchForAnyMatch(self, filters):
        pass

    def searchForExactMatch(self, filters):
        pass