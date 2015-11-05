import unittest
import os, sys
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MusicManager


class TestMusicManager(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_files/manager_tests")
        self.manager = MusicManager.MusicManager(None, folder=self.folder, apis='all')

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
        result = self.manager.getPieceInfo(["testcase2.xml"])
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
                           'instruments': [{'name': 'Piano'}],
                           'time_signatures': ['4/4']}
        for index in expected_result:
            self.assertTrue(index in result[0])
            if index != "clefs" and index != "tempos":
                self.assertEqual(expected_result[index], result[0][index])
            else:
                for item in expected_result[index]:
                    self.assertTrue(item in result[0][index])
        self.assertEqual(
            ["testcase2.xml"], self.manager.getFileList())

    def testHandleOldFiles(self):
        self.manager.parseOldFiles(["file.xml"])
        self.assertEqual(self.manager.getPieceInfo(["file.xml"]), [])

    def testRefresh(self):
        self.manager.addPiece("file.xml", {})
        self.manager.refreshWithoutDownload()
        self.assertEqual(
            self.manager.folder_browser.getNewAndOldFiles()["old"],
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

    def testFindPieceByTitleAndComposer(self):
        self.manager.addPiece(
            "file.xml", {
                "title": "Blabla", "composer": "Bartok"})
        self.manager.addPiece("file1.xml", {"title": "Blabla"})
        self.assertEqual(
            {
                'Composer: Bartok': [
                    ('Blabla by Bartok(file.xml)',
                     'file.xml')],
                'Exact Matches': [
                    ('Blabla by Bartok(file.xml)',
                     'file.xml')],
                'Title: Blabla': [
                    ('Blabla by Bartok(file.xml)',
                     'file.xml'),
                    ('Blabla(file1.xml)',
                     'file1.xml')]},
            self.manager.runQueries(
                {
                    "title": ["Blabla"],
                    "composer": ["Bartok"]}))

    def testFindPieceByTitleAndLyricist(self):
        self.manager.addPiece(
            "file.xml", {
                "title": "Blabla", "lyricist": "Bartok"})
        self.manager.addPiece("file1.xml", {"title": "Blabla"})
        self.assertEqual(
            {
                "Exact Matches": [
                    ('Blabla by , Bartok(file.xml)',
                     'file.xml')],
                "Title: Blabla": [
                    ('Blabla by , Bartok(file.xml)',
                     'file.xml'),
                    ('Blabla(file1.xml)',
                     'file1.xml')],
                "Lyricist: Bartok": [
                    ('Blabla by , Bartok(file.xml)',
                     'file.xml')]},
            self.manager.runQueries(
                {
                    "title": ["Blabla"],
                    "lyricist": ["Bartok"]}))

    def testFindPieceByTitleAndKey(self):
        self.manager.addPiece("file.xml", {"title": "Blabla", "instruments": [
                              {"name": "Clarinet"}], "key": {"Clarinet": [{"fifths": 0, "mode": "major"}]}})
        self.manager.addPiece("file1.xml", {"title": "Blabla"})
        self.assertEqual(
            {
                "Exact Matches": [
                    ('Blabla(file.xml)', 'file.xml')], "Title: Blabla": [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Keys": [
                    ('Blabla(file.xml)', 'file.xml')]}, self.manager.runQueries(
                        {
                            "title": ["Blabla"], "key": {
                                "other": ["C major"]}}))

    def testFindPieceByTitleAndKeyAndClef(self):
        self.manager.addPiece("file.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Clarinet"}],
                                  "clef": {"Clarinet": ["treble"]},
                                  "key": {"Clarinet": ["C major"]}})
        self.manager.addPiece("file1.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Clarinet"}],
                                  "key": {"Clarinet": ["C major"]}})
        self.assertEqual(
            {
                "Title: Blabla": [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Keys": [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Clefs": [
                    ('Blabla(file.xml)', 'file.xml')], "Exact Matches": [
                        ('Blabla(file.xml)', 'file.xml')]}, self.manager.runQueries(
                            {
                                "title": ["Blabla"], "key": {
                                    "other": ["C major"]}, "clef": {
                                        "other": ["treble"]}}))

    def testFindPieceByTitleAndKeyAndClefAndInstrument(self):
        self.manager.addPiece("file.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Clarinet"}],
                                  "clef": {"Clarinet": ["treble"]},
                                  "key": {"Clarinet": ["C major"]}})
        self.manager.addPiece("file1.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Sax"}],
                                  "key": {"Sax": ["C major"]}})
        self.assertEqual(
            {
                "Title: Blabla": [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Clefs": [
                    ('Blabla(file.xml)', 'file.xml')], "Exact Matches": [
                    ('Blabla(file.xml)', 'file.xml')], "Keys": [
                        ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Instruments": [
                            ('Blabla(file.xml)', 'file.xml')]}, self.manager.runQueries(
                                {
                                    "title": ["Blabla"], "key": {
                                        "other": ["C major"]}, "clef": {
                                            "other": ["treble"]}, "instrument": {
                                                "Clarinet": {}}}))

    def testFindPieceByTitleAndInstrumentWithClef(self):
        self.manager.addPiece("file.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Clarinet"}],
                                  "clef": {"Clarinet": ["treble"]},
                                  "key": {"Clarinet": ["C major"]}})
        self.manager.addPiece("file1.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Sax"},
                                               {"name": "Clarinet"}],
                                  "clef": {"Sax": ["treble"]}})
        self.assertEqual(
            {
                'Instrument in Clefs': [
                    ('Blabla(file.xml)', 'file.xml')], 'Exact Matches': [
                    ('Blabla(file.xml)', 'file.xml')], 'Instruments': [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], 'Keys': [
                        ('Blabla(file.xml)', 'file.xml')], 'Title: Blabla': [
                            ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')]}, self.manager.runQueries(
                                {
                                    "title": ["Blabla"], "key": {
                                        "other": ["C major"]}, "clef": {
                                            "Clarinet": ["treble"]}, "instrument": {
                                                "Clarinet": {}}}))

    def testFindPieceByTitleAndInstrumentWithClefAndOther(self):
        self.manager.addPiece("file.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Clarinet"},
                                               {"name": "Sax"}],
                                  "clef": {"Clarinet": [{"sign": "G",
                                                         "line": 2}],
                                           "Sax": [{"line": 4,
                                                    "sign": "F"}]},
                                  "key": {"Clarinet": ["C major"]}})
        self.manager.addPiece("file1.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Sax"},
                                               {"name": "Clarinet"}],
                                  "clef": {"Sax": [{"line": 4,
                                                    "sign": "F"}]}})
        self.assertEqual(
            {
                'Exact Matches': [
                    ('Blabla(file.xml)', 'file.xml')], 'Title: Blabla': [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], 'Instrument in Clefs': [
                    ('Blabla(file.xml)', 'file.xml')], 'Keys': [
                        ('Blabla(file.xml)', 'file.xml')], 'Instruments': [
                            ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], 'Clefs': [
                                ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')]}, self.manager.runQueries(
                                    {
                                        "title": ["Blabla"], "key": {
                                            "other": ["C major"]}, "clef": {
                                                "Clarinet": ["treble"], "other": ["bass"]}, "instrument": {
                                                    "Clarinet": {}}}))

    def testFindPieceByTitleAndInstrumentWithKey(self):
        self.manager.addPiece("file.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Clarinet"},
                                               {"name": "Sax"}],
                                  "clef": {"Clarinet": [{"sign": "G",
                                                         "line": 2}],
                                           "Sax": [{"line": 4,
                                                    "sign": "F"}]},
                                  "key": {"Clarinet": [{"fifths": 2,
                                                        "mode": "major"}]}})
        self.manager.addPiece("file1.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Sax"},
                                               {"name": "Clarinet"}],
                                  "key": {"Sax": [{"fifths": 2,
                                                   "mode": "major"}]},
                                  "clef": {"Sax": [{"line": 4,
                                                    "sign": "F"}]}})
        self.assertEqual(
            {
                "Title: Blabla": [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Exact Matches": [
                    ('Blabla(file.xml)', 'file.xml')], "Instruments in Keys": [
                    ('Blabla(file.xml)', 'file.xml')]}, self.manager.runQueries(
                        {
                            "title": ["Blabla"], "key": {
                                "Clarinet": ["D major"]}, "instrument": ["Clarinet"]}))

    def testFindPieceByTitleAndInstrumentWithKeyAndOther(self):
        self.manager.addPiece("file.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Clarinet"},
                                               {"name": "Sax"}],
                                  "clef": {"Clarinet": [{"sign": "G",
                                                         "line": 2}],
                                           "Sax": [{"line": 4,
                                                    "sign": "F"}]},
                                  "key": {"Clarinet": [{"fifths": 2,
                                                        "mode": "major"}],
                                          "Sax": [{"fifths": 0,
                                                   "mode": "major"}]}})
        self.manager.addPiece("file1.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Sax"},
                                               {"name": "Clarinet"}],
                                  "key": {"Sax": [{"fifths": 0,
                                                   "mode": "major"},
                                                  {"fifths": 2,
                                                   "mode": "major"}]},
                                  "clef": {"Sax": [{"line": 4,
                                                    "sign": "F"}]}})
        self.assertEqual(
            {
                "Title: Blabla": [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Exact Matches": [
                    ('Blabla(file.xml)', 'file.xml')], "Keys": [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Instruments in Keys": [
                        ('Blabla(file.xml)', 'file.xml')]}, self.manager.runQueries(
                            {
                                "title": ["Blabla"], "key": {
                                    "Clarinet": ["D major"], "other": ["C major"]}, "instrument": ["Clarinet"]}))

    def testFindPieceByTitleAndInstrumentWithKeyAndClef(self):
        self.manager.addPiece("file.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Clarinet"},
                                               {"name": "Sax"}],
                                  "clef": {"Clarinet": [{"sign": "G",
                                                         "line": 2}],
                                           "Sax": [{"line": 4,
                                                    "sign": "F"}]},
                                  "key": {"Clarinet": [{"fifths": 2,
                                                        "mode": "major"}]}})
        self.manager.addPiece("file1.xml",
                              {"title": "Blabla",
                               "instruments": [{"name": "Sax"},
                                               {"name": "Clarinet"}],
                                  "key": {"Clarinet": [{"fifths": 2,
                                                        "mode": "major"}]},
                                  "clef": {"Sax": [{"line": 4,
                                                    "sign": "F"}]}})
        self.assertEqual(
            {
                "Title: Blabla": [
                    ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')], "Exact Matches": [
                    ('Blabla(file.xml)', 'file.xml')], "Instrument in Clefs": [
                    ('Blabla(file.xml)', 'file.xml')], "Instruments in Keys": [
                        ('Blabla(file.xml)', 'file.xml'), ('Blabla(file1.xml)', 'file1.xml')]}, self.manager.runQueries(
                            {
                                "title": ["Blabla"], "key": {
                                    "Clarinet": ["D major"]}, "instrument": ["Clarinet"], "clef": {
                                        "Clarinet": ["treble"]}}))

    def tearDown(self):
        files = ["testcase2.xml", "file5.mxl"]
        val = os.listdir(self.folder)
        for file in val:
            if file not in files:
                os.remove(os.path.join(self.folder, file))
