import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
import pytest
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict

class TestSuiteDataLayerUserQueries(object):

    def testGetInstrumentNames(self, mlayer, dummy, dummy_res):
        instruments = ["flute", "clarinet"]
        instrument_query = {"instruments": [], "keys": {}, "clefs": {}}
        for elem in instruments:
            instrument_query["instruments"].append({"name":elem})
            instrument_query["keys"][elem] = [{"name": "C major"}]
            instrument_query["clefs"][elem] = [{"name": "treble"}]
        mlayer.add_piece("file.xml", instrument_query)
        results = mlayer.get_instrument_names()
        assert sorted(instruments) == sorted(results)

    def testGetAnyAndAll(self, mlayer, dummy, dummy_res):
        instruments = ["clarinet", "flute"]
        instrument_query = {"instruments": []}
        for elem in instruments:
            instrument_query["instruments"].append({"name":elem})
        mlayer.add_piece("file.xml", instrument_query)
        mlayer.add_piece("file1.xml", {"instruments": [{"name":"clarinet"}]})
        mlayer.add_piece("file2.xml", {"instruments": [{"name":"flute"}]})
        expected = {"All Instruments":["file.xml"], "Instrument: clarinet":["file.xml", "file1.xml"], "Instrument: flute":["file.xml", "file2.xml"]}
        results = mlayer.get_pieces_by_any_all_instruments(instruments)
        assert results == expected

    def testFindPieceByInstruments(self, mlayer, dummy):
        data = {}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        assert ["file.xml"] == mlayer.get_pieces_by_instruments(["wibble"])

    def testFindPieceByMultipleInstruments(self, mlayer, dummy, dummy_res):
        mlayer.add_piece(
            "file.xml", {"instruments": [{"name": "clarinet"}, {"name": "flute"}]})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml"], mlayer.get_pieces_by_instruments(["clarinet", "flute"]))

    def testFindPieceByInstrumentWhereTwoItemsExist(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "flute"}]})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], mlayer.get_pieces_by_instruments(["flute"]))

    def testFindPieceByPartialInstrument(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "flute"}]})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], mlayer.get_pieces_by_instruments(["fl"]))

    def testFindPieceByPartialInstrumentWhereTwoExist(self, mlayer, dummy, dummy_res):
        mlayer.add_piece(
            "file.xml", {"instruments": [{"name": "flugel Horn"}]})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], mlayer.get_pieces_by_instruments(["fl"]))

    def testFindPieceByComposer(self, mlayer, dummy, dummy_res):
        data = {"composer": "Bartok"}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        assert "file.xml" == mlayer.get_pieces_by_creator("Bartok")[0]

    def testFindPieceByPartialComposer(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"composer": "Bella Bartok"})
        mlayer.add_piece("file2.xml", {"composer": "Bella Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], mlayer.get_pieces_by_creator("Bartok"))

    def testFindPieceByPartialComposerWhereTwoExist(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"composer": "Bella Bartok"})
        mlayer.add_piece("file2.xml", {"composer": "Tina Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], mlayer.get_pieces_by_creator("Bartok"))

    def testFindPieceByLyricist(self, mlayer, dummy, dummy_res):
        data = {"lyricist": "Bartok"}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        assert "file.xml" == mlayer.get_pieces_by_creator("Bartok", creator_type='lyricist')[0]

    def testFindPieceByPartialLyricist(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"lyricist": "Bella Bartok"})
        mlayer.add_piece("file2.xml", {"lyricist": "Bella Bartok"})
        assert ["file.xml", "file2.xml"] == mlayer.get_pieces_by_creator("Bartok", creator_type='lyricist')

    def testFindPieceByPartialLyricistWhereTwoExist(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"lyricist": "Bella Bartok"})
        mlayer.add_piece("file2.xml", {"lyricist": "Tina Bartok"})
        assert ["file.xml", "file2.xml"] == mlayer.get_pieces_by_creator("Bartok", creator_type='lyricist')

    def testFindPieceByTitle(self, mlayer, dummy, dummy_res):
        data = {"title": "Blabla"}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        assert "file.xml" == mlayer.getPieceByTitle("Blabla")[0]

    def testFindPieceByPartialTitle(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"title": "abcdef"})
        mlayer.add_piece("file2.xml", {"title": "abcd"})
        assert ["file.xml", "file2.xml"] == mlayer.getPieceByTitle("abc")

    def testFindPieceByKey(self, mlayer, clef_in):
        data = {"instruments": [{"name": "clarinet"}],
                "keys": {"clarinet": [{"fifths": 2, "mode": "major"}]},
                "clefs": {"clarinet": [clef_in]}}
        mlayer.add_piece(
            "file.xml", data)
        assert "file.xml" == mlayer.get_piece_by_join([{"name":"D major"}], "keys")[0]

    def testFindPieceByInstrumentInKey(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        mlayer.add_piece(
            "file2.xml", {"key": {"flute": [{"fifths": 2, "mode": "major"}]}})
        assert "file.xml" == mlayer.getPieceByInstrumentInKeys({"clarinet": ["D major"]})[0]

    def testFindPieceByInstrumentInKeyWithTwoEntries(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        assert ["file.xml", "file2.xml"] == mlayer.getPieceByInstrumentInKeys(
            {"clarinet": ["D major"]})

    def testFindPieceByInstrumentInKeyWithTwoEntriesWhichHaveDifferentKeys(
            self, mlayer):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 1, "mode": "major"}]}})
        assert ["file.xml"] == mlayer.getPieceByInstrumentInKeys({"clarinet": ["D major"]})

    def testFindPieceByClef(self, mlayer, dummy, dummy_res, key_in):
        mlayer.add_piece("file", {"instruments": [{"name": "clarinet"}], "clefs": {
                           "clarinet": [{"sign": "G", "line": 2}]},
                                  "keys": {"clarinet": [key_in]}})
        assert ["file"] == mlayer.get_piece_by_join([{"name":"treble"}], table="clefs")

    def testFindPieceByInstrumentInClef(self, mlayer, dummy, dummy_res, key_in):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "clarinet"}], "clefs": {
                           "clarinet": [{"line": 2, "sign": "G"}]},
                                      "keys": {"clarinet": [key_in]}})
        mlayer.add_piece(
            "file2.xml", {"instruments": [{"name": "flute"}],
                          "clefs": {"flute": [{"line": 2, "sign": "G"}]},
                          "keys": {"flute": [key_in]}})
        assert "file.xml" == mlayer.get_piece_by_instrument_in_clefs({"clarinet": ["treble"]})[0]

    def testFindPieceByInstrumentInClefWithTwoEntries(self, mlayer, dummy, dummy_res):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"line": 2, "sign": "G"}]}})
        mlayer.add_piece("file2.xml", {"instruments": [
                           {"name": "clarinet"}], "clef": {"clarinet": [{"line": 2, "sign": "G"}]}})
        self.assertEqual(["file.xml", "file2.xml"], mlayer.get_piece_by_instrument_in_clefs(
            {"clarinet": ["treble"]}))

    def testFindPieceByInstrumentInClefWithTwoEntriesWhichHaveDifferentKeys(
            self, mlayer):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"line": 2, "sign": "G"}]}})
        mlayer.add_piece("file2.xml", {"instruments": [
                           {"name": "clarinet"}], "clef": {"clarinet": [{"line": 1, "sign": "G"}]}})
        assert ["file.xml"] == mlayer.get_piece_by_instrument_in_clefs({"clarinet": ["treble"]})

    def testFindPieceByMeter(self, mlayer, dummy, dummy_res):
        data = {"time_signatures": [{"beat": 4, "beat_type": 4}]}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        assert ["file.xml"] == mlayer.getPieceByMeter(["4/4"])

    def testFindPieceByTempo(self, mlayer, dummy, dummy_res):
        mlayer.add_piece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 60}]})
        assert ["file.xml"] == mlayer.get_piece_by_tempo(
                ["crotchet=60"])

    def testFindInstrumentsByTranspositions(self, mlayer, dummy, dummy_res):
        mlayer.add_multiple([{"name": "clarinet",
                                   "diatonic": -1,
                                    "chromatic": -2},
                                  {"name": "trumpet",
                                   "diatonic": -1,
                                 "chromatic": -2}], table="instruments")
        assert [{"name": "clarinet", "id": 1, "diatonic": -1, "chromatic": -2},
                          {"name": "trumpet",
                                   "diatonic": -1,
                                 "chromatic": -2, "id": 2}] == mlayer.getInstrumentsByTransposition(
            {"diatonic": -1, "chromatic": -2})

    def testFindSimilarInstruments(self, mlayer, dummy, dummy_res):
        mlayer.addInstruments([{"name": "clarinet",
                                   "diatonic": -1,
                                   "chromatic": -2},
                                  {"name": "trumpet",
                                   "diatonic": -1,
                                   "chromatic": -2}])
        assert [hashdict(name='trumpet', rowid=2)] == mlayer.getInstrumentsBySameTranspositionAs("clarinet")

    def testFindSimilarInstrumentsWhereOneIsDiff(self, mlayer, dummy, dummy_res):
        mlayer.addInstruments([{"name": "clarinet",
                                   "diatonic": -1,
                                    "chromatic": -2},
                                  {"name": "lute",
                                   "diatonic": 0,
                                   "chromatic": -2},
                                  {"name": "trumpet",
                                   "diatonic": -1,
                                   "chromatic": -2}])
        assert [hashdict(name='trumpet', rowid=3)] == mlayer.getInstrumentsBySameTranspositionAs("clarinet")

    def testFindPiecesContainingInstrumentsOrSimilar(self, mlayer, dummy, dummy_res):
        mlayer.add_piece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "diatonic": 1, "chromatic": 2}, {
                        "name": "violin", "diatonic": 0, "chromatic": 0}]})
        mlayer.addInstruments(
            [{"name": "flute", "diatonic": 0, "chromatic": 0}])
        assert ["file.xml"] == mlayer.getPieceByInstrumentsOrSimilar(
            [{"name": "flute"}, {"name": "clarinet"}])

    def testFindPiecesContainingInstrumentsOrSimilarWhereInstrumentNotInTable(
            self, mlayer):
        mlayer.add_piece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "diatonic": 1, "chromatic": 2}, {
                        "name": "violin", "diatonic": 0, "chromatic": 0}]})
        mlayer.addInstruments(
            [{"name": "flute", "diatonic": 0, "chromatic": 0}])
        result = mlayer.getPieceByInstrumentsOrSimilar([{"name": "flute"},
                                                                   {"name":
                                                                       "clarinet"},
                                                                   {"name": "trumpet",
                                                                    "diatonic": 1,
                                                                    "chromatic": 2,
                                                                    "octave": 0}])
        assert ["file.xml"] == result

    def testFindByModularity(self, mlayer, dummy, dummy_res, clef_in, clef_out):
        mlayer.add_piece("file.xml", {"instruments": [{"name": "clarinet"}], "keys": {
                           "clarinet": [{"mode": "major", "fifths": 1}]},
                                      "clefs": {"clarinet": [clef_in]}})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "trumpet"}], "keys": {
                           "trumpet": [{"mode": "major", "fifths": 0}]}, "clefs": {"trumpet": [clef_in]}})
        mlayer.add_piece("file3.xnl", {"instruments": [{"name": "flute"}], "keys": {
                           "flute": [{"mode": "minor", "fifths": 0}]}, "clefs": {"flute": [clef_in]}})
        assert mlayer.getPiecesByModularity("major") == ["file.xml", "file2.xml"]

    def testFindPieceByTempoWhereTempoIsTwoBeats(self, mlayer, dummy, dummy_res):
        mlayer.add_piece(
            "file.xml", {"tempo": [{"beat": "quarter", "beat_2": "half"}]})
        assert mlayer.get_piece_by_tempo(["crotchet=minim"]) == ["file.xml"]

    def testFindPieceByTempoLessThanAQuaver(self, mlayer, dummy, dummy_res):
        mlayer.add_piece(
            "file.xml", {"tempo": [{"beat": "16th", "minute": 60}]})
        assert mlayer.get_piece_by_tempo(["semiquaver=60"]) == ["file.xml"]

    def testFindPieceByDottedTempo(self, mlayer, dummy, dummy_res):
        data = {"tempos": [{"beat": "16th.", "minute": 60}]}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        result = mlayer.get_piece_by_tempo(["semiquaver.=60"])
        assert result == ["file.xml"]

    def testFindPieceByTempoInAmerican(self, mlayer, dummy, dummy_res):
        mlayer.add_piece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 60}]})
        assert ["file.xml"] == mlayer.get_piece_by_tempo(["quarter=60"])

    def testFindPieceByTempoWhereTempoIsTwoBeatsInAmerican(self, mlayer, dummy, dummy_res):
        mlayer.add_piece(
            "file.xml", {"tempo": [{"beat": "quarter", "beat_2": "half"}]})
        assert ["file.xml"] == mlayer.get_piece_by_tempo(["quarter=half"])

