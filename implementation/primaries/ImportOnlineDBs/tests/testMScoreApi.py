import unittest
import os
from implementation.primaries.ImportOnlineDBs.classes import MScoreApi



class testMScoreApi(unittest.TestCase):

    def setUp(self):
        self.api = MScoreApi.MuseScoreApi(folder="")

    def testDownloadFile(self):
        file_tuple = (770336, '6c3a00d9e0')
        self.assertEqual(
            200, self.api.downloadFile(file_tuple[0], file_tuple[1]))

    def testDownloadFileExists(self):
        file_tuple = (770336, '6c3a00d9e0')
        self.api.downloadFile(file_tuple[0], file_tuple[1])
        self.assertTrue(os.path.exists('770336.mxl'))

    def testGetCollection(self):
        self.assertIsInstance(self.api.getCollection(), list)

    def testGetCollectionLength(self):
        self.assertTrue(len(self.api.getCollection()) > 0)

    def testCleanCollection(self):
        self.assertIsInstance(self.api.cleanCollection(), list)

    def testSearchForExactMatchTitle(self):
        self.assertIsInstance(self.api.search(
            {'text': ['"Natural (di Vassily B.)-Album:Life(completd Song)"']}), dict)

    def testSearchKeys(self):
        results = self.api.search(
            {'text': ['"Natural (di Vassily B.)-Album:Life(completd Song)"']})
        self.assertEqual(
            list(results.keys()), ['"Natural (di Vassily B.)-Album:Life(completd Song)"'])

    def testSearchForExactMatchTitleLength(self):
        self.assertTrue(len(self.api.search(
            {'text': ['"Natural (di Vassily B.)-Album:Life(completd Song)"']})) > 0)

    def testSearchForAnyMatchTitles(self):
        self.assertIsInstance(self.api.searchForExactMatch(
            {'text': ['"Natural (di Vassily B.)-Album:Life(completd Song)"', 'Hello']}), list)
