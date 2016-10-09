import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
import os
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict


class TestDataLayerOnlineSearching(object):
    def testGetPieceListOffline(self, mlayer, dummy):
        data = {
                "composer": "blabla", "source": "MuseScore"}
        data2 = {"composer": "blabla"}
        data2.update(dummy)
        data.update(dummy)
        mlayer.add_piece(
            "file.xml", data)
        mlayer.add_piece("file1.xml", data2)
        result_set = mlayer.get_file_list()
        assert result_set == ["file1.xml"]

    def testGetPieceListOnline(self, mlayer, dummy):
        data = {"composer": "blabla", "source": "MuseScore"}
        data2 = {"composer": "blabla"}
        data2.update(dummy)
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        mlayer.add_piece("file1.xml", data2)
        result_set = mlayer.get_file_list(online=True)
        assert result_set == ["file.xml"]

    def testGetPieceOffline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = mlayer.getExactPiece("file.xml")
        self.assertEqual(result_set, None)

    def testGetPieceOnline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = mlayer.getExactPiece("file.xml", online=True)
        self.assertEqual(
            result_set,
            hashdict(
                composer_id=1,
                filename='file.xml',
                title='',
                rowid=1,
                lyricist_id=-1))

    def testGetPieceByInstrumentsOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"composer": "blabla",
                             "source": "MuseScore",
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_pieces_by_instruments(["Clarinet"])
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentsOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"composer": "blabla",
                             "source": "MuseScore",
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_pieces_by_instruments(
            ["Clarinet"],
            online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByComposerOffline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = mlayer.get_pieces_by_creator("blabla")
        self.assertEqual(result_set, [])

    def testGetPieceByComposerOnline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = mlayer.get_pieces_by_creator("blabla", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByLyricistOffline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "lyricist": "blabla", "source": "MuseScore"})
        result_set = mlayer.get_pieces_by_creator(
            "blabla", creator_type='lyricist')
        self.assertEqual(result_set, [])

    def testGetPieceByLyricistOnline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "lyricist": "blabla", "source": "MuseScore"})
        result_set = mlayer.get_pieces_by_creator(
            "blabla", online=True, creator_type='lyricist')
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByTitleOffline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore"})
        result_set = mlayer.getPieceByTitle("blabla")
        self.assertEqual(result_set, [])

    def testGetPieceByTitleOnline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore"})
        result_set = mlayer.getPieceByTitle("blabla", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByKeysOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_join(["D major"], "key")
        self.assertEqual(result_set, [])

    def testGetPieceByKeysOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_join(
            ["D major"], "key", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByModularityOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPiecesByModularity("major")
        self.assertEqual(result_set, [])

    def testGetPieceByModularityOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPiecesByModularity("major", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPiecesByAllKeysOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_all_elem(elem='keys')
        self.assertEqual(result_set, {})

    def testGetPieceByAllKeysOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_all_elem(elem='keys', online=True)
        self.assertEqual(result_set, {'D major': ['file.xml', 'file1.xml']})

    def testGetPieceByAllClefsOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_all_elem(elem='clefs')
        self.assertEqual(result_set, {})

    def testGetPieceByAllClefsOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_all_elem(elem='clefs', online=True)
        self.assertEqual(result_set, {"treble": ['file.xml', 'file1.xml']})

    def testGetPieceByAllTimeSigsOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPiecesByAllTimeSigs()
        self.assertEqual(result_set, {})

    def testGetPieceByAllTimeSigsOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        mlayer.add_piece("file1.xml", {
            "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = mlayer.getPiecesByAllTimeSigs(online=True)
        self.assertEqual(result_set, {"4/4": ['file.xml', 'file1.xml']})

    def testGetPieceByAllTemposOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "tempo": [{"beat": "quarter",
                                        "minute": 100}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "tempo": [{"beat": "quarter",
                                        "minute": 100}]})
        result_set = mlayer.getPiecesByAllTempos()
        self.assertEqual(result_set, {})

    def testGetPieceByAllTemposOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "tempo": [{"beat": "quarter",
                                        "minute": 100}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "tempo": [{"beat": "quarter",
                                        "minute": 100}]})
        result_set = mlayer.getPiecesByAllTempos(online=True)
        self.assertEqual(
            result_set, {
                'quarter=100': [
                    'file.xml', 'file1.xml']})

    def testGetPieceByAllInstrumentsOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPiecesByAllInstruments()
        self.assertEqual(result_set, {})

    def testGetPieceByAllInstrumentsOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPiecesByAllInstruments(online=True)
        self.assertEqual(result_set, {'Clarinet': ['file.xml', 'file1.xml']})

    def testGetPieceByAllComposersOffline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Bark"})
        mlayer.add_piece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Bark"})
        result_set = mlayer.get_piece_by_all_elem(elem='composers')
        self.assertEqual(result_set, {})

    def testGetPieceByAllComposersOnline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Motsart"})
        mlayer.add_piece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Motsart"})
        result_set = mlayer.get_piece_by_all_elem(
            elem='composers', online=True)
        self.assertEqual(result_set, {'Motsart': ['file.xml', 'file1.xml']})

    def testGetPieceByAllLyricistsOffline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Bark"})
        mlayer.add_piece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Bark"})
        result_set = mlayer.get_piece_by_all_elem(elem='composers')
        self.assertEqual(result_set, {})

    def testGetPieceByAllLyricistsOnline(self, mlayer, dummy):
        mlayer.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Motsart"})
        mlayer.add_piece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Motsart"})
        result_set = mlayer.get_piece_by_all_elem(
            elem='lyricists', online=True)
        self.assertEqual(result_set, {'Motsart': ['file.xml', 'file1.xml']})

    def testGetPieceByClefsOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_join(["treble"], "clef")
        self.assertEqual(result_set, [])

    def testGetPieceByClefsOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        mlayer.add_piece("file1.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_join(
            ["treble"], "clef", online=True)
        self.assertEqual(result_set, ['file.xml', 'file1.xml'])

    def testGetPieceByInstrumentInKeysOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPieceByInstrumentInKeys(
            {"Clarinet": ["D major"]})
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentInKeysOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "key": {"Clarinet": [{"mode": "major",
                                                   "fifths": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPieceByInstrumentInKeys(
            {"Clarinet": ["D major"]}, online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByInstrumentInClefsOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_instrument_in_clefs(
            {"Clarinet": ["treble"]})
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentInClefsOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                            {"title": "blabla",
                             "source": "MuseScore",
                             "clef": {"Clarinet": [{"sign": "G",
                                                    "line": 2}]},
                             "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.get_piece_by_instrument_in_clefs(
            {"Clarinet": ["treble"]}, online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByMetersOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = mlayer.getPieceByMeter(["4/4"])
        self.assertEqual(result_set, [])

    def testGetPieceByMetersOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = mlayer.getPieceByMeter(["4/4"], online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByTempoOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla",
            "source": "MuseScore",
            "tempo": [{"beat": "quarter", "minute": 100}]})
        result_set = mlayer.get_piece_by_tempo(["quarter=100"])
        self.assertEqual(result_set, [])

    def testGetPieceByTempoOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla",
            "source": "MuseScore",
            "tempo": [{"beat": "quarter", "minute": 100}]})
        result_set = mlayer.get_piece_by_tempo(["quarter=100"], online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByInstrumentsOrSimilarOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla",
            "source": "MuseScore",
            "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPieceByInstrumentsOrSimilar(
            [{"name": "Clarinet"}])
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentsOrSimilarOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla",
            "source": "MuseScore",
            "instruments": [{"name": "Clarinet"}]})
        result_set = mlayer.getPieceByInstrumentsOrSimilar(
            [{"name": "Clarinet"}], online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceSource(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla",
            "source": "MuseScore",
            "instruments": [{"name": "Clarinet"}]})
        result = mlayer.get_value_for_filename("file.xml", 'source')
        self.assertEqual(result['source'], 'MuseScore')

    def testDownloadPiece(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla",
            "source": "MuseScore",
            "instruments": [{"name": "Clarinet"}]})
        mlayer.downloadPiece("file.xml")
        result = mlayer.get_value_for_filename("file.xml", 'source')
        self.assertEqual(result, None)
