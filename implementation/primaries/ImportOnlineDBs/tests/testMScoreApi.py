import unittest
from implementation.primaries.ImportOnlineDBs.classes import MScoreApi

class testMScoreApi(unittest.TestCase):
    def setUp(self):
        self.api = MScoreApi.MuseScoreApi(folder="")

    def testDownloadFile(self):
        uri = 'http://api.musescore.com/services/rest/score/770081'

        self.assertEqual(None, self.api.downloadFile(uri))

    def testGetCollection(self):
        self.assertIsInstance(self.api.getCollection(), list)

    def testGetCollectionLength(self):
        self.assertTrue(len(self.api.getCollection()) > 0)

    def testCleanCollection(self):
        self.assertIsInstance(self.api.cleanCollection(), list)


    def testSearchForExactMatchTitle(self):
        self.assertIsInstance(self.api.search({'text':['"Natural (di Vassily B.)-Album:Life(completd Song)"']}), dict)

    def testSearchKeys(self):
        results = self.api.search({'text':['"Natural (di Vassily B.)-Album:Life(completd Song)"']})
        self.assertEqual(list(results.keys()), ['"Natural (di Vassily B.)-Album:Life(completd Song)"'])

    def testSearchForExactMatchTitleLength(self):
        self.assertTrue(len(self.api.search({'text':['"Natural (di Vassily B.)-Album:Life(completd Song)"']})) > 0)


    def testSearchForAnyMatchTitles(self):
        self.assertIsInstance(self.api.searchForExactMatch({'text':['"Natural (di Vassily B.)-Album:Life(completd Song)"', 'Hello']}), list)

