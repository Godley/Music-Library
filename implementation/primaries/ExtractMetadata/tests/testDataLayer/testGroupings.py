import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.MusicData import MusicData
import os

class TestDataLayerGeneratePlaylists(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testFindAllPiecesByAllKeys(self):
        self.data.addPiece("file.xml", {"key": {
                           "clari": [{"mode": "major", "fifths": 0}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file2.xml", {"key": {
                           "clari": [{"mode": "major", "fifths": 0}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file1.xml", {"key": {
                           "clari": [{"mode": "major", "fifths": 1}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file3.xml", {"key": {
                           "clari": [{"mode": "major", "fifths": 1}]}, "instruments": [{"name": "clari"}]})
        self.assertEqual({"C major": ["file.xml",
                                      "file2.xml"],
                          "G major": ["file1.xml",
                                      "file3.xml"]},
                         self.data.getPiecesByAllKeys())

    def testFindAllPiecesByAllClefs(self):
        self.data.addPiece("file.xml", {"clef": {
                           "clari": [{"sign": "G", "line": 2}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file3.xml", {"clef": {
                           "clari": [{"sign": "G", "line": 2}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file1.xml", {"clef": {
                           "clari": [{"sign": "F", "line": 4}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file2.xml", {"clef": {
                           "clari": [{"sign": "F", "line": 4}]}, "instruments": [{"name": "clari"}]})
        self.assertEqual({"treble": ["file.xml",
                                     "file3.xml"],
                          "bass": ["file1.xml",
                                   "file2.xml"]},
                         self.data.getPiecesByAllClefs())

    def testFindAllPiecesByAllTimeSigs(self):
        self.data.addPiece("file.xml", {"time": [{"beat": 4, "type": 4}]})
        self.data.addPiece("file1.xml", {"time": [{"beat": 4, "type": 4}]})
        self.assertEqual(
            {"4/4": ["file.xml", "file1.xml"]}, self.data.getPiecesByAllTimeSigs())

    def testFindAllPiecesByAllTempos(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 100}]})
        self.data.addPiece(
            "file3.xml", {"tempo": [{"beat": "quarter", "minute": 100}]})
        self.data.addPiece(
            "file1.xml", {"tempo": [{"beat": "quarter", "beat_2": "eighth"}]})
        self.data.addPiece(
            "file2.xml", {"tempo": [{"beat": "quarter", "beat_2": "eighth"}]})
        self.assertEqual({"quarter=eighth": ["file1.xml", "file2.xml"], "quarter=100": [
                         "file.xml", "file3.xml"]}, self.data.getPiecesByAllTempos())

    def testFindAllPiecesByAllInstruments(self):
        self.data.addPiece(
            "file.xml", {"instruments": [{"name": "clarinet"}, {"name": "flute"}]})
        self.data.addPiece(
            "file1.xml", {"instruments": [{"name": "clarinet"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual({"flute": ["file.xml",
                                    "file2.xml"],
                          "clarinet": ["file.xml",
                                       "file1.xml"]},
                         self.data.getPiecesByAllInstruments())

    def testFindAllPiecesByAllInstrumentsWithTranspositionsAndUniqueNames(
            self):
        self.data.addPiece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "transposition": {
                            "diatonic": 1, "chromatic": 2}}, {
                        "name": "flute"}]})
        self.data.addPiece("file1.xml", {"instruments": [
                           {"name": "clarinet", "transposition": {"diatonic": 1, "chromatic": 2}}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            {
                "flute": [
                    "file.xml",
                    "file2.xml"],
                "clarinet\n(Transposed By 1 Diatonic \n2 Chromatic)": [
                    "file.xml",
                    "file1.xml"]},
            self.data.getPiecesByAllInstruments())

    def testFindAllPiecesByAllInstrumentsWithTranspositions(self):
        self.data.addPiece("file.xml",
                           {"instruments": [{"name": "clarinet"},
                                            {"name": "clarinet",
                                             "transposition": {"diatonic": 1}}]})
        self.data.addPiece(
            "file1.xml", {"instruments": [{"name": "clarinet"}]})
        self.data.addPiece("file2.xml",
                           {"instruments": [{"name": "flute"},
                                            {"name": "clarinet",
                                             "transposition": {"diatonic": 1}}]})
        self.assertEqual(
            {
                "clarinet": [
                    "file.xml",
                    "file1.xml"],
                "clarinet\n(Transposed By 1 Diatonic \n)": [
                    "file.xml",
                    "file2.xml"]},
            self.data.getPiecesByAllInstruments())

    def testFindAllPiecesByAllComposers(self):
        self.data.addPiece("file.xml", {"composer": "Charlotte"})
        self.data.addPiece("file1.xml", {"composer": "Charlie"})
        self.data.addPiece("file2.xml", {"composer": "Charlie"})
        self.assertEqual(
            {"Charlie": ["file1.xml", "file2.xml"]}, self.data.getPiecesByAllComposers())

    def testFindAllPiecesByAllLyricists(self):
        self.data.addPiece("file.xml", {"lyricist": "Charlotte"})
        self.data.addPiece("file1.xml", {"lyricist": "Charlie"})
        self.data.addPiece("file2.xml", {"lyricist": "Charlie"})
        self.assertEqual(
            {"Charlie": ["file1.xml", "file2.xml"]}, self.data.getPiecesByAllLyricists())

    def testFindAllPiecesByAllKeysWithTransposedInstruments(self):
        self.data.addPiece("file.xml",
                           {"key": {"clari": [{"mode": "major",
                                               "fifths": 0}]},
                            "instruments": [{"name": "clari",
                                             "transposition": {"diatonic": 1}}]})
        self.data.addPiece("file1.xml",
                           {"key": {"clarin": [{"mode": "major",
                                                "fifths": 1}]},
                            "instruments": [{"name": "clarin"}]})
        self.data.addPiece("file2.xml",
                           {"key": {"clarin": [{"mode": "major",
                                                "fifths": 1}]},
                            "instruments": [{"name": "clarin"}]})
        self.assertEqual(
            {"G major": ["file1.xml", "file2.xml"]}, self.data.getPiecesByAllKeys())

    def testArchivePiece(self):
        self.data.addPiece("file.xml", {"instruments": [
                           {"name": "clarinet", "transposition": {"diatonic": -1, "chromatic": -2}}]})
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 1)
        self.data.archivePieces(["file.xml"])
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 0)
        self.assertEqual(len(self.data.getArchivedPieces()), 1)

    def testRemovePiece(self):
        self.data.addPiece("file.xml", {"instruments": [
                           {"name": "clarinet", "transposition": {"diatonic": -1, "chromatic": -2}}]})
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 1)
        self.data.removePieces(["file.xml"])
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 0)
        self.assertEqual(len(self.data.getArchivedPieces()), 0)
