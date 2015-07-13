import unittest
from implementation.primaries.ImportOnlineDBs.classes import API

class testAPI(unittest.TestCase):
    def setUp(self):
        self.api = API.Api(folder="")

    def testDownloadFile(self):
        with self.assertRaises(NotImplementedError):
            self.api.downloadFile("heh", "")

    def testGetCollection(self):
        with self.assertRaises(NotImplementedError):
            self.api.getCollection()

    def testCleanCollection(self):
        with self.assertRaises(NotImplementedError):
            self.api.cleanCollection()

    def testSearch(self):
        with self.assertRaises(NotImplementedError):
            self.api.search({})


