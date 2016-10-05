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

    def testFindAllPiecesByAllTimeSigs(self, mlayer, dummy):
        data = {"time_signatures": [{"beat": 4, "beat_type": 4}]}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        mlayer.add_piece("file1.xml", data)
        expected = {"4/4": ["file.xml", "file1.xml"]}
        assert expected == mlayer.get_piece_by_all_(elem="time_signatures")

    def testFindAllPiecesByAllTempos(self, mlayer, dummy):
        data1 = {"tempos": [{"beat": "quarter", "minute": 100}]}
        data2 = {"tempos": [{"beat": "quarter", "beat_2": "eighth"}]}
        data1.update(dummy)
        data2.update(dummy)
        mlayer.add_piece("file.xml", data1)
        mlayer.add_piece("file3.xml", data1)
        mlayer.add_piece("file1.xml", data2)
        mlayer.add_piece("file2.xml", data2)
        expected = {
            "quarter=eighth": [
                "file1.xml", "file2.xml"], "quarter=100": [
                "file.xml", "file3.xml"]}
        assert expected == mlayer.get_piece_by_all_(elem="tempos")

    def testFindAllPiecesByAllInstruments(self, mlayer, clef_in, key_in):
        fixtures = [{"instruments": [
            {"name": "clarinet"}, {"name": "flute"}]},
            {"instruments": [{"name": "clarinet"}]},
            {"instruments": [{"name": "flute"}]}]
        fixtures = self.mk_clef_key(fixtures, clef_in, key_in)
        mlayer.add_piece("file.xml", fixtures[0])
        mlayer.add_piece("file1.xml", fixtures[1])
        mlayer.add_piece("file2.xml", fixtures[2])
        expected = {"flute": ["file.xml",
                              "file2.xml"],
                    "clarinet": ["file.xml",
                                 "file1.xml"]}
        assert expected == mlayer.get_piece_by_all_(elem="instruments")

    def testFindAllPiecesByAllInstrumentsWithTranspositionsAndUniqueNames(
            self,
            mlayer, clef_in, key_in):
        fixtures = [{
            "instruments": [
                    {
                        "name": "clarinet", "diatonic": 1, "chromatic": 2}, {
                        "name": "flute"}]},
                    {"instruments": [
                        {"name": "clarinet", "diatonic": 1, "chromatic": 2}]},
                    {"instruments": [{"name": "flute"}]}]
        fixtures = self.mk_clef_key(fixtures, clef_in, key_in)
        mlayer.add_piece(
            "file.xml", fixtures[0])
        mlayer.add_piece("file1.xml", fixtures[1])
        mlayer.add_piece("file2.xml", fixtures[2])
        result = mlayer.get_piece_by_all_(elem="instruments")
        expected = {
            "flute": [
                "file.xml",
                "file2.xml"],
            "clarinet transposed 2 chromatic 1 diatonic": [
                "file.xml",
                "file1.xml"]}
        assert result == expected

    def testFindAllPiecesByAllInstrumentsWithTranspositions(
            self, mlayer, clef_in, key_in):
        fixtures = [{"instruments": [{"name": "clarinet"},
                                     {"name": "clarinet",
                                      "diatonic": 1}]},
                    {"instruments": [{"name": "clarinet"}]},
                    {"instruments": [{"name": "clarinet",
                                      "diatonic": 1}]}]
        fixtures = self.mk_clef_key(fixtures, clef_in, key_in)
        mlayer.add_piece("file.xml", fixtures[0])
        mlayer.add_piece(
            "file1.xml", fixtures[1])
        mlayer.add_piece("file2.xml",
                         fixtures[2])
        result = mlayer.get_piece_by_all_("instruments")
        exp = {
            "clarinet": [
                "file.xml",
                "file1.xml"],
            "clarinet transposed 1 diatonic": [
                "file.xml",
                "file2.xml"]}
        assert result == exp

    def testFindAllPiecesByAllComposers(self, mlayer, clef_in, key_in):
        fixtures = [
            {"composer": "Charlie", "instruments": [{"name": "clarinet"}]},
            {"composer": "Charlie", "instruments": [{"name": "clarinet"}]}]
        fixtures = self.mk_clef_key(fixtures, clef_in, key_in)
        mlayer.add_piece("file1.xml", fixtures[0])
        mlayer.add_piece("file2.xml", fixtures[1])
        expected = {"Charlie": ["file1.xml", "file2.xml"]}
        assert mlayer.get_piece_by_all_creators(elem='composer') == expected

    def testFindAllPiecesByAllLyricists(self, mlayer, clef_in, key_in):
        fixtures = [
            {"lyricist": "Charlie", "instruments": [{"name": "clarinet"}]},
            {"lyricist": "Charlie", "instruments": [{"name": "clarinet"}]}]
        fixtures = self.mk_clef_key(fixtures, clef_in, key_in)
        mlayer.add_piece("file1.xml", fixtures[0])
        mlayer.add_piece("file2.xml", fixtures[1])
        exp = {"Charlie": ["file1.xml", "file2.xml"]}
        assert mlayer.get_piece_by_all_creators(elem='lyricist') == exp

    def testFindAllPiecesByAllKeysWithTransposedInstruments(
            self, mlayer, clef_in):
        fixtures = [
                    {"keys": {"clarin": [{"mode": "major",
                                          "fifths": 1}]},
                     "instruments": [{"name": "clarin"}]},
                    {"keys": {"clarin": [{"mode": "major",
                                          "fifths": 1}]},
                     "instruments": [{"name": "clarin"}]}]
        fixtures = self.mk_clef_key(fixtures, clef_in)
        mlayer.add_piece("file1.xml",
                         fixtures[0])
        mlayer.add_piece("file2.xml",
                         fixtures[1])
        exp = {"G major": ["file1.xml", "file2.xml"]}
        assert mlayer.get_piece_by_all_(elem='keys') == exp

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

    def mk_clef_key(self, fixtures, clef_in=None, key_in=None):
        for fix in fixtures:
            if "clefs" not in fix:
                fix["clefs"] = {}
            if "keys" not in fix:
                fix["keys"] = {}
            for ins in fix["instruments"]:
                if clef_in is not None:
                    fix["clefs"][ins["name"]] = [clef_in]
                if key_in is not None:
                    fix["keys"][ins["name"]] = [key_in]
        return fixtures
