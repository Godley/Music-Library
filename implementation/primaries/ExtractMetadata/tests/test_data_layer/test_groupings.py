import unittest
import os


class TestSuiteDataLayerGeneratePlaylists(object):

    def testFindAllPiecesByAllKeys(self, mlayer, clef_in):
        mlayer.add_piece("file.xml", {"keys": {
            "clari": [{"mode": "major", "fifths": 0}]}, "instruments": [{"name": "clari"}],
                                      "clefs": {"clari": [clef_in]}})
        mlayer.add_piece("file2.xml", {"keys": {
            "clari": [{"mode": "major", "fifths": 0}]}, "instruments": [{"name": "clari"}],
                                       "clefs": {"clari": [clef_in]}})
        mlayer.add_piece("file1.xml", {"keys": {
            "clari": [{"mode": "major", "fifths": 1}]}, "instruments": [{"name": "clari"}],
                                       "clefs": {"clari": [clef_in]}})
        mlayer.add_piece("file3.xml", {"keys": {
            "clari": [{"mode": "major", "fifths": 1}]}, "instruments": [{"name": "clari"}],
                                       "clefs": {"clari": [clef_in]}})
        expected = {"C major": ["file.xml",
                                "file2.xml"],
                    "G major": ["file1.xml",
                                "file3.xml"]}
        assert mlayer.get_piece_by_all_(elem='keys') == expected

    def testFindAllPiecesByAllClefs(self, mlayer):
        mlayer.add_piece("file.xml", {"clefs": {
            "clari": [{"sign": "G", "line": 2}]},
                                      "keys": {
            "clari": [{"mode": "major", "fifths": 0}]},
                                      "instruments": [{"name": "clari"}]})
        mlayer.add_piece("file3.xml", {"clefs": {
            "clari": [{"sign": "G", "line": 2}]},
                                       "keys": {
            "clari": [{"mode": "major", "fifths": 0}]},
                                       "instruments": [{"name": "clari"}]})
        mlayer.add_piece("file1.xml", {"clefs": {
            "clari": [{"sign": "F", "line": 4}]},
                                       "keys": {
            "clari": [{"mode": "major", "fifths": 0}]},
                                       "instruments": [{"name": "clari"}]})
        mlayer.add_piece("file2.xml", {"clefs": {
            "clari": [{"sign": "F", "line": 4}]},
                                       "keys": {
            "clari": [{"mode": "major", "fifths": 0}]},
                                       "instruments": [{"name": "clari"}]})
        expected = {"treble": ["file.xml",
                               "file3.xml"],
                    "bass": ["file1.xml",
                             "file2.xml"]}
        assert mlayer.get_piece_by_all_(elem='clefs') == expected

    def testFindAllPiecesByAllTimeSigs(self, mlayer):
        mlayer.add_piece("file.xml", {"time": [{"beat": 4, "type": 4}]})
        mlayer.add_piece("file1.xml", {"time": [{"beat": 4, "type": 4}]})
        expected = {"4/4": ["file.xml", "file1.xml"]}
        assert expected == mlayer.getPiecesByAllTimeSigs()

    def testFindAllPiecesByAllTempos(self, mlayer):
        mlayer.add_piece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 100}]})
        mlayer.add_piece(
            "file3.xml", {"tempo": [{"beat": "quarter", "minute": 100}]})
        mlayer.add_piece(
            "file1.xml", {"tempo": [{"beat": "quarter", "beat_2": "eighth"}]})
        mlayer.add_piece(
            "file2.xml", {"tempo": [{"beat": "quarter", "beat_2": "eighth"}]})
        expected = {
            "quarter=eighth": [
                "file1.xml", "file2.xml"], "quarter=100": [
                "file.xml", "file3.xml"]}
        assert expected == mlayer.getPiecesByAllTempos()

    def testFindAllPiecesByAllInstruments(self, mlayer):
        mlayer.add_piece("file.xml", {"instruments": [
            {"name": "clarinet"}, {"name": "flute"}]})
        mlayer.add_piece(
            "file1.xml", {"instruments": [{"name": "clarinet"}]})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "flute"}]})
        expected = {"flute": ["file.xml",
                              "file2.xml"],
                    "clarinet": ["file.xml",
                                 "file1.xml"]}
        assert expected == mlayer.getPiecesByAllInstruments()

    def testFindAllPiecesByAllInstrumentsWithTranspositionsAndUniqueNames(
            self,
            mlayer):
        mlayer.add_piece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "diatonic": 1, "chromatic": 2}, {
                        "name": "flute"}]})
        mlayer.add_piece("file1.xml", {"instruments": [
            {"name": "clarinet", "diatonic": 1, "chromatic": 2}]})
        mlayer.add_piece("file2.xml", {"instruments": [{"name": "flute"}]})
        result = mlayer.getPiecesByAllInstruments()
        expected = {
            "flute": [
                "file.xml",
                "file2.xml"],
            "clarinet transposed 1 diatonic 2 chromatic": [
                "file.xml",
                "file1.xml"]}
        assert result == expected

    def testFindAllPiecesByAllInstrumentsWithTranspositions(self, mlayer):
        mlayer.add_piece("file.xml",
                         {"instruments": [{"name": "clarinet"},
                                          {"name": "clarinet",
                                           "diatonic": 1}]})
        mlayer.add_piece(
            "file1.xml", {"instruments": [{"name": "clarinet"}]})
        mlayer.add_piece("file2.xml",
                         {"instruments": [{"name": "flute"},
                                          {"name": "clarinet",
                                           "diatonic": 1}]})
        result = mlayer.getPiecesByAllInstruments()
        exp = {
            "clarinet": [
                "file.xml",
                "file1.xml"],
            "clarinet transposed 1 diatonic 0 chromatic": [
                "file.xml",
                "file2.xml"]}
        assert result == exp

    def testFindAllPiecesByAllComposers(self, mlayer):
        mlayer.add_piece("file.xml", {"composer": "Charlotte"})
        mlayer.add_piece("file1.xml", {"composer": "Charlie"})
        mlayer.add_piece("file2.xml", {"composer": "Charlie"})
        expected = {"Charlie": ["file1.xml", "file2.xml"]}
        assert mlayer.get_piece_by_all_elem(elem='composers') == expected

    def testFindAllPiecesByAllLyricists(self, mlayer):
        mlayer.add_piece("file.xml", {"lyricist": "Charlotte"})
        mlayer.add_piece("file1.xml", {"lyricist": "Charlie"})
        mlayer.add_piece("file2.xml", {"lyricist": "Charlie"})
        exp = {"Charlie": ["file1.xml", "file2.xml"]}
        assert mlayer.get_piece_by_all_elem(elem='lyricists') == exp

    def testFindAllPiecesByAllKeysWithTransposedInstruments(self, mlayer):
        mlayer.add_piece("file.xml",
                         {"key": {"clari": [{"mode": "major",
                                             "fifths": 0}]},
                          "instruments": [{"name": "clari",
                                           "diatonic": 1}]})
        mlayer.add_piece("file1.xml",
                         {"key": {"clarin": [{"mode": "major",
                                              "fifths": 1}]},
                          "instruments": [{"name": "clarin"}]})
        mlayer.add_piece("file2.xml",
                         {"key": {"clarin": [{"mode": "major",
                                              "fifths": 1}]},
                          "instruments": [{"name": "clarin"}]})
        exp = {"G major": ["file1.xml", "file2.xml"]}
        assert mlayer.get_piece_by_all_elem(elem='keys') == exp

    def test_archive_piece(self, mlayer):
        mlayer.add_piece("file.xml", {"instruments": [
            {"name": "clarinet", "diatonic": -1, "chromatic": -2}]})
        self.assertEqual(len(mlayer.get_all_piece_info(["file.xml"])), 1)
        mlayer.archivePieces(["file.xml"])
        self.assertEqual(len(mlayer.get_all_piece_info(["file.xml"])), 0)
        self.assertEqual(len(mlayer.getArchivedPieces()), 1)

    def testRemovePiece(self, mlayer):
        mlayer.add_piece("file.xml", {"instruments": [
            {"name": "clarinet", "diatonic": -1, "chromatic": -2}]})
        self.assertEqual(len(mlayer.get_all_piece_info(["file.xml"])), 1)
        mlayer.removePieces(["file.xml"])
        self.assertEqual(len(mlayer.get_all_piece_info(["file.xml"])), 0)
        self.assertEqual(len(mlayer.getArchivedPieces()), 0)
