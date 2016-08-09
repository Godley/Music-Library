import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.MusicData import MusicData
import os


class TestDataLayerUserQueries(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testGetInstrumentNames(self):
        instruments = ["flute", "clarinet"]
        instrument_query = {"instruments": []}
        for elem in instruments:
            instrument_query["instruments"].append({"name":elem})
        self.data.addPiece("file.xml", instrument_query)
        results = self.data.getInstrumentNames()
        self.assertListEqual(instruments, results)

    def testGetAnyAndAll(self):
        instruments = ["clarinet", "flute"]
        instrument_query = {"instruments": []}
        for elem in instruments:
            instrument_query["instruments"].append({"name":elem})
        self.data.addPiece("file.xml", instrument_query)
        self.data.addPiece("file1.xml", {"instruments": [{"name":"clarinet"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name":"flute"}]})
        expected = {"All Instruments":["file.xml"], "Instrument: clarinet":["file.xml", "file1.xml"], "Instrument: flute":["file.xml", "file2.xml"]}
        results = self.data.getPiecesByAnyAndAllInstruments(instruments)
        self.assertEqual(expected, results)

    def testFindPieceByInstruments(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPiecesByInstruments(
                ["clarinet"]))

    def testFindPieceByMultipleInstruments(self):
        self.data.addPiece(
            "file.xml", {"instruments": [{"name": "clarinet"}, {"name": "flute"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml"], self.data.getPiecesByInstruments(["clarinet", "flute"]))

    def testFindPieceByInstrumentWhereTwoItemsExist(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "flute"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByInstruments(["flute"]))

    def testFindPieceByPartialInstrument(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "flute"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByInstruments(["fl"]))

    def testFindPieceByPartialInstrumentWhereTwoExist(self):
        self.data.addPiece(
            "file.xml", {"instruments": [{"name": "flugel Horn"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByInstruments(["fl"]))

    def testFindPieceByComposer(self):
        self.data.addPiece("file.xml", {"composer": "Bartok"})
        self.assertEqual(
            "file.xml",
            self.data.getPiecesByComposer("Bartok")[0])

    def testFindPieceByPartialComposer(self):
        self.data.addPiece("file.xml", {"composer": "Bella Bartok"})
        self.data.addPiece("file2.xml", {"composer": "Bella Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByComposer("Bartok"))

    def testFindPieceByPartialComposerWhereTwoExist(self):
        self.data.addPiece("file.xml", {"composer": "Bella Bartok"})
        self.data.addPiece("file2.xml", {"composer": "Tina Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByComposer("Bartok"))

    def testFindPieceByLyricist(self):
        self.data.addPiece("file.xml", {"lyricist": "Bartok"})
        self.assertEqual(
            "file.xml",
            self.data.getPiecesByLyricist("Bartok")[0])

    def testFindPieceByPartialLyricist(self):
        self.data.addPiece("file.xml", {"lyricist": "Bella Bartok"})
        self.data.addPiece("file2.xml", {"lyricist": "Bella Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByLyricist("Bartok"))

    def testFindPieceByPartialLyricistWhereTwoExist(self):
        self.data.addPiece("file.xml", {"lyricist": "Bella Bartok"})
        self.data.addPiece("file2.xml", {"lyricist": "Tina Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByLyricist("Bartok"))

    def testFindPieceByTitle(self):
        self.data.addPiece("file.xml", {"title": "Blabla"})
        self.assertEqual("file.xml", self.data.getPieceByTitle("Blabla")[0])

    def testFindPieceByPartialTitle(self):
        self.data.addPiece("file.xml", {"title": "abcdef"})
        self.data.addPiece("file2.xml", {"title": "abcd"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPieceByTitle("abc"))

    def testFindPieceByKey(self):
        self.data.addPiece(
            "file.xml", {"key": {"clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.assertEqual("file.xml", self.data.getPieceByKeys(["D major"])[0])

    def testFindPieceByInstrumentInKey(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.data.addPiece(
            "file2.xml", {"key": {"flute": [{"fifths": 2, "mode": "major"}]}})
        self.assertEqual(
            "file.xml", self.data.getPieceByInstrumentInKeys({"clarinet": ["D major"]})[0])

    def testFindPieceByInstrumentInKeyWithTwoEntries(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.assertEqual(["file.xml", "file2.xml"], self.data.getPieceByInstrumentInKeys(
            {"clarinet": ["D major"]}))

    def testFindPieceByInstrumentInKeyWithTwoEntriesWhichHaveDifferentKeys(
            self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 1, "mode": "major"}]}})
        self.assertEqual(
            ["file.xml"], self.data.getPieceByInstrumentInKeys({"clarinet": ["D major"]}))

    def testFindPieceByClef(self):
        self.data.addPiece("file", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"sign": "G", "line": 2}]}})
        self.assertEqual(["file"], self.data.getPieceByClefs(["treble"]))

    def testFindPieceByInstrumentInClef(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"line": 2, "sign": "G"}]}})
        self.data.addPiece(
            "file2.xml", {"clef": {"flute": [{"line": 2, "sign": "G"}]}})
        self.assertEqual(
            "file.xml", self.data.getPieceByInstrumentInClefs({"clarinet": ["treble"]})[0])

    def testFindPieceByInstrumentInClefWithTwoEntries(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"line": 2, "sign": "G"}]}})
        self.data.addPiece("file2.xml", {"instruments": [
                           {"name": "clarinet"}], "clef": {"clarinet": [{"line": 2, "sign": "G"}]}})
        self.assertEqual(["file.xml", "file2.xml"], self.data.getPieceByInstrumentInClefs(
            {"clarinet": ["treble"]}))

    def testFindPieceByInstrumentInClefWithTwoEntriesWhichHaveDifferentKeys(
            self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"line": 2, "sign": "G"}]}})
        self.data.addPiece("file2.xml", {"instruments": [
                           {"name": "clarinet"}], "clef": {"clarinet": [{"line": 1, "sign": "G"}]}})
        self.assertEqual(
            ["file.xml"], self.data.getPieceByInstrumentInClefs({"clarinet": ["treble"]}))

    def testFindPieceByMeter(self):
        self.data.addPiece("file.xml", {"time": [{"beat": 4, "type": 4}]})
        self.assertEqual(["file.xml"], self.data.getPieceByMeter(["4/4"]))

    def testFindPieceByTempo(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 60}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["crotchet=60"]))

    def testFindInstrumentsByTranspositions(self):
        self.data.addInstruments([{"name": "clarinet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}},
                                  {"name": "trumpet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}}])
        self.assertEqual([(1, "clarinet"), (2, "trumpet")], self.data.getInstrumentByTransposition(
            {"diatonic": -1, "chromatic": -2}))

    def testFindSimilarInstruments(self):
        self.data.addInstruments([{"name": "clarinet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}},
                                  {"name": "trumpet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}}])
        self.assertEqual(
            [(2, "trumpet")], self.data.getInstrumentsBySameTranspositionAs("clarinet"))

    def testFindSimilarInstrumentsWhereOneIsDiff(self):
        self.data.addInstruments([{"name": "clarinet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}},
                                  {"name": "lute",
                                   "transposition": {"diatonic": 0,
                                                     "chromatic": -2}},
                                  {"name": "trumpet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}}])
        self.assertEqual(
            [(3, "trumpet")], self.data.getInstrumentsBySameTranspositionAs("clarinet"))

    def testFindPiecesContainingInstrumentsOrSimilar(self):
        self.data.addPiece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "transposition": {
                            "diatonic": 1, "chromatic": 2}}, {
                        "name": "violin", "transposition": {
                            "diatonic": 0, "chromatic": 0}}]})
        self.data.addInstruments(
            [{"name": "flute", "transposition": {"diatonic": 0, "chromatic": 0}}])
        self.assertEqual(["file.xml"], self.data.getPieceByInstrumentsOrSimilar(
            [{"name": "flute"}, {"name": "clarinet"}]))

    def testFindPiecesContainingInstrumentsOrSimilarWhereInstrumentNotInTable(
            self):
        self.data.addPiece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "transposition": {
                            "diatonic": 1, "chromatic": 2}}, {
                        "name": "violin", "transposition": {
                            "diatonic": 0, "chromatic": 0}}]})
        self.data.addInstruments(
            [{"name": "flute", "transposition": {"diatonic": 0, "chromatic": 0}}])
        self.assertEqual(["file.xml"],
                         self.data.getPieceByInstrumentsOrSimilar([{"name": "flute"},
                                                                   {"name":
                                                                       "clarinet"},
                                                                   {"name": "trumpet",
                                                                    "transposition": {"diatonic": 1,
                                                                                      "chromatic": 2,
                                                                                      "octave": 0}}]))

    def testFindByModularity(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"mode": "major", "fifths": 1}]}})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "trumpet"}], "key": {
                           "trumpet": [{"mode": "major", "fifths": 0}]}})
        self.data.addPiece("file3.xnl", {"instruments": [{"name": "flute"}], "key": {
                           "flute": [{"mode": "minor", "fifths": 0}]}})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByModularity("major"))

    def testFindPieceByTempoWhereTempoIsTwoBeats(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "beat_2": "half"}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["crotchet=minim"]))

    def testFindPieceByTempoLessThanAQuaver(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "16th", "minute": 60}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["semiquaver=60"]))

    def testFindPieceByDottedTempo(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "16th.", "minute": 60}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["semiquaver.=60"]))

    def testFindPieceByTempoInAmerican(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 60}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["quarter=60"]))

    def testFindPieceByTempoWhereTempoIsTwoBeatsInAmerican(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "beat_2": "half"}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["quarter=half"]))

