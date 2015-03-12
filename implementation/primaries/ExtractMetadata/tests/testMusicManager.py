import unittest, os
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MusicManager

class testMusicManager(unittest.TestCase):
    def setUp(self):
        self.folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/ExtractMetadata/tests/test_files/manager_tests"
        self.manager = MusicManager.MusicManager(folder=self.folder)
        self.manager.data.addPiece("file.xml",{})

    def testRunUnzipper(self):
        self.manager.setupFolderBrowser()
        self.manager.handleZips()
        self.assertTrue(os.path.exists(os.path.join(self.folder, "file5.xml")))
        self.assertFalse(os.path.exists(os.path.join(self.folder, 'META-INF')))

    def testParseXMLFiles(self):
        self.manager.setupFolderBrowser()
        self.manager.parseNewFiles = MagicMock(name='method')
        self.manager.parseOldFiles = MagicMock(name='method')
        self.manager.handleXMLFiles()
        self.manager.parseNewFiles.assert_called_once_with(["file1.xml"])
        self.manager.parseOldFiles.assert_called_once_with(["file.xml"])

    def testRefresh(self):
        pass

    def tearDown(self):
        os.remove(os.path.join(self.folder, "music.db"))
        if os.path.exists(os.path.join(self.folder, "file5.xml")):
            os.remove(os.path.join(self.folder, "file5.xml"))