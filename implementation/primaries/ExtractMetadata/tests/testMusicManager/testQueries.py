import unittest
import os, sys
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MusicManager


class TestMusicManager(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None
        self.folder = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../test_files/manager_tests")
        self.manager = MusicManager.MusicManager(None, folder=self.folder)

    def testFindPieceByTitleAndComposer(self):
        self.manager.addPiece(
            "file.xml", {
                "title": "Blabla", "composer": "Bartok"})
        self.manager.addPiece("file1.xml", {"title": "Blabla"})
        results = self.manager.runQueries({"title": ["Blabla"], "composer": ["Bartok"]})
        expected_results = {'Composer: Bartok': [('title: Blabla composer: Bartok filename: file.xml', 'file.xml')],
                'Exact Matches': [('title: Blabla composer: Bartok filename: file.xml', 'file.xml')],
                'Title: Blabla': [('title: Blabla composer: Bartok filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')]}
        self.assertEqual(
            expected_results,
            results)

    def testFindPieceByTitleAndLyricist(self):
        self.manager.addPiece(
            "file.xml", {
                "title": "Blabla", "lyricist": "Bartok"})
        self.manager.addPiece("file1.xml", {"title": "Blabla"})
        expected_results = {"Exact Matches": [('title: Blabla lyricist: Bartok filename: file.xml', 'file.xml')],
                "Title: Blabla": [('title: Blabla lyricist: Bartok filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')],
                "Lyricist: Bartok": [('title: Blabla lyricist: Bartok filename: file.xml', 'file.xml')]}
        results = self.manager.runQueries({"title": ["Blabla"], "lyricist": ["Bartok"]})
        self.assertEqual(
            expected_results,
            results)

    def testFindPieceByTitleAndKey(self):
        self.manager.addPiece("file.xml", {"title": "Blabla", "instruments": [
                              {"name": "Clarinet"}], "key": {"Clarinet": [{"fifths": 0, "mode": "major"}]}})
        self.manager.addPiece("file1.xml", {"title": "Blabla"})
        expected_results = {"Exact Matches": [('title: Blabla filename: file.xml', 'file.xml')],
                "Title: Blabla": [('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')],
                "Keys": [('title: Blabla filename: file.xml', 'file.xml')]}
        results = self.manager.runQueries(
                        {
                            "title": ["Blabla"], "key": {
                                "other": ["C major"]}})
        self.assertEqual(
            expected_results, results)

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
        expected_results = {"Title: Blabla": [('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')],
                "Keys": [('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')],
                "Clefs": [('title: Blabla filename: file.xml', 'file.xml')], "Exact Matches": [('title: Blabla filename: file.xml', 'file.xml')]}
        results = self.manager.runQueries(
                            {
                                "title": ["Blabla"], "key": {
                                    "other": ["C major"]}, "clef": {
                                        "other": ["treble"]}})
        self.assertEqual(
            expected_results, results)

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
        expected_results = {
                "Title: Blabla": [
                    ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], "Clefs": [
                    ('title: Blabla filename: file.xml', 'file.xml')], "Exact Matches": [
                    ('title: Blabla filename: file.xml', 'file.xml')], "Keys": [
                        ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], "Instruments": [
                            ('title: Blabla filename: file.xml', 'file.xml')]}
        results = self.manager.runQueries(
                                {
                                    "title": ["Blabla"], "key": {
                                        "other": ["C major"]}, "clef": {
                                            "other": ["treble"]}, "instrument": {
                                                "Clarinet": {}}})
        self.assertEqual(expected_results, results)

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
        expected_results = {
                'Instruments in Clefs': [
                    ('title: Blabla filename: file.xml', 'file.xml')], 'Exact Matches': [
                    ('title: Blabla filename: file.xml', 'file.xml')], 'Instruments': [
                    ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], 'Keys': [
                        ('title: Blabla filename: file.xml', 'file.xml')], 'Title: Blabla': [
                            ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')]}

        results = self.manager.runQueries(
                                {
                                    "title": ["Blabla"], "key": {
                                        "other": ["C major"]}, "clef": {
                                            "Clarinet": ["treble"]}, "instrument": {
                                                "Clarinet": {}}})
        for key in expected_results:
            self.assertIn(key, results)
            self.assertAlmostEqual(results[key], expected_results[key])

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
        expected_results = {
                'Exact Matches': [
                    ('title: Blabla filename: file.xml', 'file.xml')], 'Title: Blabla': [
                    ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], 'Instruments in Clefs': [
                    ('title: Blabla filename: file.xml', 'file.xml')], 'Keys': [
                        ('title: Blabla filename: file.xml', 'file.xml')], 'Instruments': [
                            ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], 'Clefs': [
                                ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')]}

        results = self.manager.runQueries(
                                    {
                                        "title": ["Blabla"], "key": {
                                            "other": ["C major"]}, "clef": {
                                                "Clarinet": ["treble"], "other": ["bass"]}, "instrument": {
                                                    "Clarinet": {}}})
        self.assertEqual(
            expected_results, results)

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
        expected_results = {
                "Title: Blabla": [
                    ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], "Exact Matches": [
                    ('title: Blabla filename: file.xml', 'file.xml')], "Instruments in Keys": [
                    ('title: Blabla filename: file.xml', 'file.xml')]}

        results = self.manager.runQueries(
                        {
                            "title": ["Blabla"], "key": {
                                "Clarinet": ["D major"]}, "instrument": {"Clarinet": {}}})
        self.assertEqual(
            expected_results, results)

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
        expected_results = {
                "Title: Blabla": [
                    ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], "Exact Matches": [
                    ('title: Blabla filename: file.xml', 'file.xml')], "Keys": [
                    ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], "Instruments in Keys": [
                        ('title: Blabla filename: file.xml', 'file.xml')]}
        results = self.manager.runQueries(
                            {
                                "title": ["Blabla"], "key": {
                                    "Clarinet": ["D major"], "other": ["C major"]}, "instrument": ["Clarinet"]})
        self.assertEqual(
            expected_results, results)

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
        expected_results = {
                "Title: Blabla": [
                    ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], "Exact Matches": [
                    ('title: Blabla filename: file.xml', 'file.xml')], "Instruments in Clefs": [
                    ('title: Blabla filename: file.xml', 'file.xml')], "Instruments in Keys": [
                        ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')]}
        results = self.manager.runQueries(
                            {
                                "title": ["Blabla"], "key": {
                                    "Clarinet": ["D major"]}, "instrument": ["Clarinet"], "clef": {
                                        "Clarinet": ["treble"]}})
        self.assertEqual(
            expected_results, results)

    def testFindByTextTitle(self):
        title = "hello, world"
        self.manager.addPiece("file.xml", {"title": "hello"})
        self.manager.addPiece("file1.xml", {"title": "hello, world"})
        result = self.manager.runQueries({"text": title.split(" ")})
        expected_result = {"Title": [('title: hello, world filename: file1.xml', 'file1.xml')],
                           "Exact Matches": [('title: hello, world filename: file1.xml', 'file1.xml')]}
        self.assertDictEqual(expected_result, result)


    def testFindByInstrumentsWithNoLabel(self):
        query = {"text": ["clarinet", "flute"]}
        self.manager.addPiece("file1.xml", {"instruments": [{"name": "clarinet"}]})
        self.manager.addInstruments([{"name":"flute"}])
        expected_results = {
                        "Instrument: clarinet": [('filename: file1.xml', 'file1.xml')]}
        results = self.manager.runQueries(query)
        self.assertEqual(expected_results, results)

    def testFindByInstrumentsWithNoLabel2Entries(self):
        query = {"text": ["clarinet", "flute"]}
        self.manager.addPiece("file1.xml", {"instruments": [{"name": "clarinet"}]})
        self.manager.addPiece("file2.xml", {"instruments": [{"name": "clarinet"}, {"name": "flute"}]})
        expected_results = {"All Instruments": [('filename: file2.xml', 'file2.xml')],
                            "Exact Matches": [('filename: file2.xml', 'file2.xml')],
                        "Instrument: clarinet": [('filename: file1.xml', 'file1.xml'), ('filename: file2.xml', 'file2.xml')],
                        "Instrument: flute": [('filename: file2.xml', 'file2.xml')]}
        results = self.manager.runQueries(query)
        self.assertEqual(expected_results, results)


    def tearDown(self):
        files = ["testcase2.xml", "file5.mxl"]
        val = os.listdir(self.folder)
        for file in val:
            if file not in files:
                os.remove(os.path.join(self.folder, file))
