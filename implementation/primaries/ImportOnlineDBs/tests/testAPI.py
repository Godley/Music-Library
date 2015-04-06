import unittest
from implementation.primaries.ImportOnlineDBs.classes import API

class testAPI(unittest.TestCase):
    def setUp(self):
        self.api = API.Api(folder="")

    def testDownloadFile(self):
        with self.assertRaises(NotImplementedError):
            self.api.downloadFile("heh")

    def testGetCollection(self):
        with self.assertRaises(NotImplementedError):
            self.api.getCollection()

    def testSearchForAnyMatch(self):
        with self.assertRaises(NotImplementedError):
            self.api.searchForAnyMatch({})

    def testSearchForExactMatch(self):
        with self.assertRaises(NotImplementedError):
            self.api.searchForExactMatch({})


