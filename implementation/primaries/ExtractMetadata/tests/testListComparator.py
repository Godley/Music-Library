import unittest
from implementation.primaries.ExtractMetadata.classes import MusicManager
from implementation.primaries import ExtractMetadata
import os


class TestListComparator(unittest.TestCase):

    def setUp(self):
        self.folder = os.path.join(os.path.dirname(ExtractMetadata.__file__), 'tests', 'test_files')
        self.current = os.path.join(self.folder, 'folder_tests')
        print(self.current)
        self.folderBrowser = MusicManager.FolderBrowser(
            db_files=[
                'file1.xml',
                'file2.xml'],
            folder=self.current)

    def testGetListFromFolder(self):
        self.assertEqual(
            self.folderBrowser.getFolderFiles(), {
                "xml": [
                    "file1.xml", "file3.xml"], "mxl": ["file5.mxl"]})

    def testComparatorWithMultipleFolders(self):
        current = os.path.join(self.folder, 'folder_tests_2')
        self.folderBrowser = MusicManager.FolderBrowser(
            db_files=[],
            folder=current)
        self.assertEqual(self.folderBrowser.getFolderFiles(),
                         {"xml": ["test.xml", "folder_2/test2.xml"]})

    def testGetZipList(self):
        self.assertEqual(self.folderBrowser.getZipFiles(), ["file5.mxl"])

    def testFilesToBeAdded(self):
        self.assertEqual(
            self.folderBrowser.getNewFileList(), ["file3.xml"])

    def testRecordsToBeArchived(self):
        self.assertEqual(self.folderBrowser.getOldRecords(), ["file2.xml"])

    def testOldAndNewFiles(self):
        self.assertEqual(
            self.folderBrowser.getNewAndOldFiles(), {
                "old": ["file2.xml"], "new": ["file3.xml"]})

    def tearDown(self):
        if os.path.exists(os.path.join(self.current, "file5.xml")):
            os.remove(os.path.join(self.current, "file5.xml"))
