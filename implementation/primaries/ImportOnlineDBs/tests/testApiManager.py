import unittest, os
from implementation.primaries.ImportOnlineDBs.classes import ApiManager

class testApiManager(unittest.TestCase):
    def setUp(self):
        self.apiMan = ApiManager.ApiManager()

    def testFetchAllFiles(self):
        result = self.apiMan.fetchAllData()
        self.assertIsInstance(result, dict)
        self.assertTrue(len(result) > 0)

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
        self.result = self.apiMan.downloadFile(source="MuseScore", file="780706", secret="54953dd4f8")
        self.bad_request = self.apiMan.downloadFile(source="notASource")
        self.evenWorseRequest = self.apiMan.downloadFile(source="MuseScore", file="notAFile", secret="noSecrets")

    def testInstance(self):
        self.assertEqual(self.result, 200)

    def testFileCreation(self):
        self.assertTrue(os.path.exists("780706.mxl"))

    def testErrorRequest(self):
        self.assertEqual(self.bad_request, 4004)

    def testBiggerErrorRequest(self):
        self.assertEqual(self.evenWorseRequest, 403)

    def testHasData(self):
        pass

    def tearDown(self):
        pass
