import unittest
import os
from implementation.primaries.ImportOnlineDBs.classes import ApiManager
import logging

log_name = 'TEST_LOG'
logger = logging.getLogger('TEST_LOG')


class testApiManager(unittest.TestCase):

    def testFetchAllFiles(self):
        apiMan = ApiManager.ApiManager(logger=logger)
        result = apiMan.fetchAllData()
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)

    def testMuseScoreEnabledIfApiKeySet(self):
        if 'MSCORE' not in os.environ:
            os.environ['MSCORE'] = 'hello'
        apiMan = ApiManager.ApiManager(logger=logger)
        self.assertIn('MuseScore', apiMan.sources)

    def testMuseScoreDisabledIfApiKeyUnset(self):
        copy_of_key = None
        if 'MSCORE' in os.environ:
            copy_of_key = os.environ['MSCORE']
            os.environ.pop('MSCORE')
        apiMan = ApiManager.ApiManager(logger=logger)
        self.assertNotIn('MuseScore', apiMan.sources)
        if copy_of_key is not None:
            os.environ['MSCORE'] = copy_of_key



class testFileDownload(unittest.TestCase):

    def setUp(self):
        self.apiMan = ApiManager.ApiManager()
        self.result = self.apiMan.downloadAllFiles()

    def testInstance(self):
        self.assertIsInstance(self.result, dict)

    def testHasData(self):
        self.assertTrue(len(self.result) > 0)

    def testFileCreation(self):
        for source_id in self.result:
            for file in self.result[source_id]:
                self.assertTrue(os.path.exists(file))

    def tearDown(self):
        for source_id in self.result:
            for file in self.result[source_id]:
                if os.path.exists(file):
                    os.remove(file)


class testSingularFileDownload(testFileDownload):

    def setUp(self):
        testFileDownload.setUp(self)
        self.result = self.apiMan.downloadFile(
            source="MuseScore", file="1365861", secret="423b4c25b8")
        self.bad_request = self.apiMan.downloadFile(source="notASource")
        self.evenWorseRequest = self.apiMan.downloadFile(
            source="MuseScore", file="notAFile", secret="noSecrets")

    def testInstance(self):
        self.assertEqual(self.result, 200)

    def testFileCreation(self):
        self.assertTrue(os.path.exists("1365861.mxl"))

    def testErrorRequest(self):
        self.assertEqual(self.bad_request, 4004)

    def testBiggerErrorRequest(self):
        self.assertEqual(self.evenWorseRequest, 403)

    def testHasData(self):
        pass

    def tearDown(self):
        pass
