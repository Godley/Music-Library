import unittest
from implementation.primaries.ExtractMetadata.classes import MusicManager

class testListComparator(unittest.TestCase):
    def setUp(self):
        self.folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/ExtractMetadata/tests/test_files/folder_tests'
        self.folderBrowser = MusicManager.FolderBrowser(db_files=['file1.xml','file2.xml'], folder=self.folder)


    def testGetListFromFolder(self):
        self.assertEqual(self.folderBrowser.getFolderFiles(), {"xml":["file1.xml","file3.xml"], "mxl":["file5.mxl"]})


    def testGetZipList(self):
        self.assertEqual(self.folderBrowser.getZipFiles(), ["file5.mxl"])

    def testFilesToBeAdded(self):
        self.assertEqual(self.folderBrowser.getNewFileList(), ["file3.xml"])

    def testRecordsToBeArchived(self):
        self.assertEqual(self.folderBrowser.getOldRecords(), ["file2.xml"])

    def testOldAndNewFiles(self):
        self.assertEqual(self.folderBrowser.getNewAndOldFiles(), {"old":["file2.xml"],"new":["file3.xml"]})
