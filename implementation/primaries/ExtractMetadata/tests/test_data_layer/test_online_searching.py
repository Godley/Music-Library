import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
import os
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict

class TestDataLayerOnlineSearching(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testGetPieceListOffline(self):
        self.data.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        self.data.add_piece("file1.xml", {"composer": "blabla"})
        result_set = self.data.getFileList()
        self.assertEqual(result_set, ["file1.xml"])

    def testGetPieceListOnline(self):
        self.data.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        self.data.add_piece("file1.xml", {"composer": "blabla"})
        result_set = self.data.getFileList(online=True)
        self.assertEqual(result_set, ["file.xml"])

    def testGetPieceOffline(self):
        self.data.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = self.data.getExactPiece("file.xml")
        self.assertEqual(result_set, None)

    def testGetPieceOnline(self):
        self.data.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = self.data.getExactPiece("file.xml", online=True)
        self.assertEqual(result_set, hashdict(composer_id=1, filename='file.xml', title='', rowid=1, lyricist_id=-1))

    def testGetPieceByInstrumentsOffline(self):
        self.data.add_piece("file.xml",
                           {"composer": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_pieces_by_instruments(["Clarinet"])
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentsOnline(self):
        self.data.add_piece("file.xml",
                           {"composer": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_pieces_by_instruments(
            ["Clarinet"],
            online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByComposerOffline(self):
        self.data.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = self.data.get_pieces_by_creator("blabla")
        self.assertEqual(result_set, [])

    def testGetPieceByComposerOnline(self):
        self.data.add_piece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = self.data.get_pieces_by_creator("blabla", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByLyricistOffline(self):
        self.data.add_piece(
            "file.xml", {
                "lyricist": "blabla", "source": "MuseScore"})
        result_set = self.data.get_pieces_by_creator("blabla", creator_type='lyricist')
        self.assertEqual(result_set, [])

    def testGetPieceByLyricistOnline(self):
        self.data.add_piece(
            "file.xml", {
                "lyricist": "blabla", "source": "MuseScore"})
        result_set = self.data.get_pieces_by_creator("blabla", online=True, creator_type='lyricist')
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByTitleOffline(self):
        self.data.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore"})
        result_set = self.data.getPieceByTitle("blabla")
        self.assertEqual(result_set, [])

    def testGetPieceByTitleOnline(self):
        self.data.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore"})
        result_set = self.data.getPieceByTitle("blabla", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByKeysOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_join(["D major"], "key")
        self.assertEqual(result_set, [])

    def testGetPieceByKeysOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_join(["D major"], "key", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByModularityOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByModularity("major")
        self.assertEqual(result_set, [])

    def testGetPieceByModularityOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByModularity("major", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPiecesByAllKeysOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_all_elem(elem='keys')
        self.assertEqual(result_set, {})

    def testGetPieceByAllKeysOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_all_elem(elem='keys', online=True)
        self.assertEqual(result_set, {'D major': ['file.xml', 'file1.xml']})

    def testGetPieceByAllClefsOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_all_elem(elem='clefs')
        self.assertEqual(result_set, {})

    def testGetPieceByAllClefsOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_all_elem(elem='clefs', online=True)
        self.assertEqual(result_set, {"treble": ['file.xml', 'file1.xml']})

    def testGetPieceByAllTimeSigsOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllTimeSigs()
        self.assertEqual(result_set, {})

    def testGetPieceByAllTimeSigsOnline(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        self.data.add_piece("file1.xml", {
                           "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = self.data.getPiecesByAllTimeSigs(online=True)
        self.assertEqual(result_set, {"4/4": ['file.xml', 'file1.xml']})

    def testGetPieceByAllTemposOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "tempo": [{"beat": "quarter",
                                       "minute": 100}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "tempo": [{"beat": "quarter",
                                       "minute": 100}]})
        result_set = self.data.getPiecesByAllTempos()
        self.assertEqual(result_set, {})

    def testGetPieceByAllTemposOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "tempo": [{"beat": "quarter",
                                       "minute": 100}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "tempo": [{"beat": "quarter",
                                       "minute": 100}]})
        result_set = self.data.getPiecesByAllTempos(online=True)
        self.assertEqual(
            result_set, {
                'quarter=100': [
                    'file.xml', 'file1.xml']})

    def testGetPieceByAllInstrumentsOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllInstruments()
        self.assertEqual(result_set, {})

    def testGetPieceByAllInstrumentsOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllInstruments(online=True)
        self.assertEqual(result_set, {'Clarinet': ['file.xml', 'file1.xml']})

    def testGetPieceByAllComposersOffline(self):
        self.data.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Bark"})
        self.data.add_piece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Bark"})
        result_set = self.data.get_piece_by_all_elem(elem='composers')
        self.assertEqual(result_set, {})

    def testGetPieceByAllComposersOnline(self):
        self.data.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Motsart"})
        self.data.add_piece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Motsart"})
        result_set = self.data.get_piece_by_all_elem(elem='composers', online=True)
        self.assertEqual(result_set, {'Motsart': ['file.xml', 'file1.xml']})

    def testGetPieceByAllLyricistsOffline(self):
        self.data.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Bark"})
        self.data.add_piece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Bark"})
        result_set = self.data.get_piece_by_all_elem(elem='composers')
        self.assertEqual(result_set, {})

    def testGetPieceByAllLyricistsOnline(self):
        self.data.add_piece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Motsart"})
        self.data.add_piece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Motsart"})
        result_set = self.data.get_piece_by_all_elem(elem='lyricists', online=True)
        self.assertEqual(result_set, {'Motsart': ['file.xml', 'file1.xml']})

    def testGetPieceByClefsOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_join(["treble"], "clef")
        self.assertEqual(result_set, [])

    def testGetPieceByClefsOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.add_piece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_join(["treble"], "clef", online=True)
        self.assertEqual(result_set, ['file.xml', 'file1.xml'])

    def testGetPieceByInstrumentInKeysOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByInstrumentInKeys(
            {"Clarinet": ["D major"]})
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentInKeysOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByInstrumentInKeys(
            {"Clarinet": ["D major"]}, online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByInstrumentInClefsOffline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_instrument_in_clefs(
            {"Clarinet": ["treble"]})
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentInClefsOnline(self):
        self.data.add_piece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.get_piece_by_instrument_in_clefs(
            {"Clarinet": ["treble"]}, online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByMetersOffline(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = self.data.getPieceByMeter(["4/4"])
        self.assertEqual(result_set, [])

    def testGetPieceByMetersOnline(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = self.data.getPieceByMeter(["4/4"], online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByTempoOffline(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla",
                           "source": "MuseScore",
                           "tempo": [{"beat": "quarter", "minute": 100}]})
        result_set = self.data.get_piece_by_tempo(["quarter=100"])
        self.assertEqual(result_set, [])

    def testGetPieceByTempoOnline(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla",
                           "source": "MuseScore",
                           "tempo": [{"beat": "quarter", "minute": 100}]})
        result_set = self.data.get_piece_by_tempo(["quarter=100"], online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByInstrumentsOrSimilarOffline(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla",
                           "source": "MuseScore",
                           "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByInstrumentsOrSimilar(
            [{"name": "Clarinet"}])
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentsOrSimilarOnline(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla",
                           "source": "MuseScore",
                           "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByInstrumentsOrSimilar(
            [{"name": "Clarinet"}], online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceSource(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla",
                           "source": "MuseScore",
                           "instruments": [{"name": "Clarinet"}]})
        result = self.data.get_value_for_filename("file.xml", 'source')
        self.assertEqual(result['source'], 'MuseScore')

    def testDownloadPiece(self):
        self.data.add_piece("file.xml", {
                           "title": "blabla",
                           "source": "MuseScore",
                           "instruments": [{"name": "Clarinet"}]})
        self.data.downloadPiece("file.xml")
        result = self.data.get_value_for_filename("file.xml", 'source')
        self.assertEqual(result, None)
