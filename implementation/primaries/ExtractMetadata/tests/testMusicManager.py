import unittest, os
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MusicManager

class testMusicManager(unittest.TestCase):
    def setUp(self):
        self.folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/ExtractMetadata/tests/test_files/manager_tests"
        self.manager = MusicManager.MusicManager(folder=self.folder)


    def testRunUnzipper(self):
        self.manager.handleZips()
        self.assertTrue(os.path.exists(os.path.join(self.folder, "file5.xml")))
        self.assertFalse(os.path.exists(os.path.join(self.folder, 'META-INF')))

    def testParseXMLFiles(self):
        self.manager.addPiece("file.xml",{})
        self.manager.refresh()
        self.manager.parseNewFiles = MagicMock(name='method')
        self.manager.parseOldFiles = MagicMock(name='method')
        self.manager.handleXMLFiles()
        self.manager.parseNewFiles.assert_called_once_with(["file5.xml","testcase2.xml"])
        self.manager.parseOldFiles.assert_called_once_with(["file.xml"])

    def testParseFile(self):
        self.manager.addPiece("file.xml",{})
        self.manager.refresh()
        self.manager.parseNewFiles(["testcase2.xml"])
        expected_result = {'filename':'testcase2.xml','keys': {'Piano': ['D major']}, 'tempos': ['half=quarter', 'eighth.=80'], 'clefs': {'Piano': ['treble','bass','alto']}, 'title': 'my metaparsing testcase', 'composer': 'charlotte godley', 'instruments': [{'name': 'Piano'}], 'time_signatures': ['4/4']}
        self.assertEqual(self.manager.getPieceInfo(["testcase2.xml"]), [expected_result])
        self.assertEqual(["file.xml","testcase2.xml"], self.manager.getFileList())

    def testHandleOldFiles(self):
        self.manager.parseOldFiles(["file.xml"])
        self.assertEqual(self.manager.getPieceInfo(["file.xml"]), [])


    def testGetAutoPlaylist(self):
        pass

    def testGetPlaylist(self):
        pass

    def testRefresh(self):
        self.manager.addPiece("file.xml",{})
        self.manager.refresh()
        self.assertEqual(self.manager.folder_browser.getNewAndOldFiles()["old"], ["file.xml"])

    def tearDown(self):
        os.remove(os.path.join(self.folder, "music.db"))
        if os.path.exists(os.path.join(self.folder, "file5.xml")):
            os.remove(os.path.join(self.folder, "file5.xml"))