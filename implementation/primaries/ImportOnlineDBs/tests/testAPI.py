import unittest
from implementation.primaries.ImportOnlineDBs.classes import API

class testAPI(unittest.TestCase):
    def setUp(self):
        self.api = API.Api(folder="")

    def testDownloadFile(self):
        self.assertEqual(self.api.downloadFile("fname.xml"), "fname.xml")

    def testGetCollection(self):
        self.assertEqual(self.api.getCollection(), [])

    def testSearchForAnyMatch(self):
        self.assertEqual(self.api.searchForAnyMatch({}), [])

    def testSearchForExactMatch(self):
        self.assertEqual(self.api.searchForExactMatch({}), [])


