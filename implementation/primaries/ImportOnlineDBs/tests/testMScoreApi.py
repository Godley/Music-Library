import unittest
from implementation.primaries.ImportOnlineDBs.classes import MScoreApi

class testMScoreApi(unittest.TestCase):
    def setUp(self):
        self.api = MScoreApi.MuseScoreApi(folder="")

    def testDownloadFile(self):
        self.assertEqual("heh", self.api.downloadFile("heh"))

    def testGetCollection(self):
        self.assertEqual([], self.api.getCollection())

    def testSearchForAnyMatch(self):
        self.assertEqual([],self.api.searchForAnyMatch({}))

    def testSearchForExactMatch(self):
        self.assertEqual([], self.api.searchForExactMatch({}))