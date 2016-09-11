import unittest
import os, sys
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MusicManager
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict
class TestMusicManager(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../test_files/manager_tests")
        self.manager = MusicManager.MusicManager(None, folder=self.folder)

    def testRunUnzipper(self):
        self.manager.handleZips()
        self.assertTrue(os.path.exists(os.path.join(self.folder, "file5.xml")))
        self.assertFalse(os.path.exists(os.path.join(self.folder, 'META-INF')))

    def testParseXMLFiles(self):
        self.manager.addPiece("file.xml", {})
        self.manager.refreshWithoutDownload()
        self.manager.parseNewFiles = MagicMock(name='method')
        self.manager.parseOldFiles = MagicMock(name='method')
        self.manager.handleXMLFiles()
        expected = sorted(["file5.xml", "testcase2.xml"])
        self.manager.parseNewFiles.assert_called_once_with(expected)
        self.manager.parseOldFiles.assert_called_once_with(["file.xml"])

    def testParseFile(self):
        self.manager.parseNewFiles(["testcase2.xml"])
        result = self.manager.getPieceInfo(["testcase2.xml"])[0]
        expected_result = {'filename': 'testcase2.xml',
                           'keys': {'Piano': ['D major']},
                           'tempos': ['half=quarter',
                                      'eighth.=80'],
                           'clefs': {'Piano': ['bass',
                                               'alto',
                                               'treble']},
                           'title': 'my metaparsing testcase',
                           'composer': 'charlotte godley',
                           'lyricist': 'fran godley',
                           'instruments': {hashdict(name='Piano', chromatic=0, diatonic=0)},
                           'timesigs': ['4/4']}

        for key in expected_result:
            self.assertIn(key, result)
            self.assertEqual(type(result[key]), type(expected_result[key]))
            if type(expected_result[key]) == dict:
                for elem in expected_result[key]:
                    self.assertIn(elem, result[key])
                    self.assertEqual(type(result[key]), type(expected_result[key]))

                    if type(expected_result[key][elem]) == list:
                        for member in expected_result[key][elem]:
                            self.assertIn(member, result[key][elem])

                    else:
                        self.assertEqual(result[key][elem], expected_result[key][elem])

            elif type(expected_result[key]) is list:
                for elem in expected_result[key]:
                    self.assertIn(elem, result[key])

            else:
                self.assertEqual(result[key], expected_result[key])

        self.assertEqual(
            ["testcase2.xml"], self.manager.getFileList())

    def testHandleOldFiles(self):
        self.manager.parseOldFiles(["file.xml"])
        self.assertEqual(self.manager.getPieceInfo(["file.xml"]), [])

    def testRefresh(self):
        self.manager.addPiece("file.xml", {})
        self.manager.refreshWithoutDownload()
        self.assertEqual(
            self.manager.folder_browser.getNewAndOldFiles(self.manager.folder_browser.getFolderFiles())["old"],
            ["file.xml"])

    def testCopyFiles(self):
        path_to_primaries = []
        value = ''
        filepath = os.path.dirname(os.path.realpath(__file__))
        while value != 'ExtractMetadata':
            pair = os.path.split(filepath)
            filepath = pair[0]
            value = pair[1]
        path_to_primaries.append(filepath)
        path_to_primaries.append("SampleMusicXML")
        path_to_primaries.append("testcases")
        path_to_primaries.append("3repeats.xml")
        file = os.path.join(*path_to_primaries)
        self.manager.copyFiles([file])
        self.assertTrue(
            os.path.exists(
                os.path.join(
                    self.folder,
                    "3repeats.xml")))

    def tearDown(self):
        files = ["testcase2.xml", "file5.mxl"]
        val = os.listdir(self.folder)
        for file in val:
            if file not in files:
                os.remove(os.path.join(self.folder, file))