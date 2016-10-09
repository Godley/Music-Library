import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
import os
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict
import copy


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
        data = {"composer": "blabla", "source": "MuseScore"}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        result_set = mlayer.getFileData(["file.xml"])
        assert result_set == []

    def testGetPieceOnline(self, mlayer, dummy):
        data = {
            "composer": "blabla", "source": "MuseScore"}
        data.update(dummy)
        mlayer.add_piece(
            "file.xml", data)
        result_set = mlayer.getFileData(["file.xml"], online=True)
        assert result_set == [{'composer.id': 1, 'filename': 'file.xml',
                               'name': '',
                               'id': 1,
                               'lyricist.id': -1,
                               'archived': False,
                               'source': 'MuseScore'}]

    def testGetPieceByInstrumentsOffline(self, mlayer, dummy):
        data = {"composer": "blabla",
                "source": "MuseScore",
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "treble"}]},
                "keys": {"Clarinet": [{"name": "C major"}]}
                }
        mlayer.add_piece("file.xml",
                         data)
        result_set = mlayer.get_pieces_by_instruments(["Clarinet"])
        assert result_set == []

    def testGetPieceByInstrumentsOnline(self, mlayer, dummy):
        data = {"composer": "blabla",
                "source": "MuseScore",
                "instruments": [{"name": "Clarinet"}]}
        data['clefs'] = {'Clarinet': [{'name': 'treble'}]}
        data['keys'] = {'Clarinet': [{'name': 'C major'}]}
        mlayer.add_piece("file.xml",
                         data)
        result_set = mlayer.get_pieces_by_instruments(
            ["Clarinet"],
            online=True)
        assert result_set == ['file.xml']

    def testGetPieceByComposerOffline(self, mlayer, dummy):
        data = {
            "composer": "blabla", "source": "MuseScore"}
        data.update(dummy)
        mlayer.add_piece(
            "file.xml", data)
        result_set = mlayer.get_pieces_by_creator("blabla")
        assert result_set == []

    def testGetPieceByComposerOnline(self, mlayer, dummy):
        data = {
            "composer": "blabla", "source": "MuseScore"}
        data.update(dummy)
        mlayer.add_piece(
            "file.xml", data)
        result_set = mlayer.get_pieces_by_creator("blabla", online=True)
        assert result_set == ['file.xml']

    def testGetPieceByLyricistOffline(self, mlayer, dummy):
        data = {
            "lyricist": "blabla", "source": "MuseScore"}
        data.update(dummy)
        mlayer.add_piece(
            "file.xml", data)
        result_set = mlayer.get_pieces_by_creator(
            "blabla", creator_type='lyricist')
        assert result_set == []

    def testGetPieceByLyricistOnline(self, mlayer, dummy):
        data = {"lyricist": "blabla", "source": "MuseScore"}
        data.update(dummy)
        mlayer.add_piece(
            "file.xml", data)
        result_set = mlayer.get_pieces_by_creator(
            "blabla", online=True, creator_type='lyricist')
        expected = ['file.xml']
        assert result_set == expected

    def testGetPieceByTitleOffline(self, mlayer, dummy):
        data = {
            "title": "blabla", "source": "MuseScore"}
        data.update(dummy)
        mlayer.add_piece(
            "file.xml", data)
        result_set = mlayer.getPieceByTitle("blabla")
        expected = []
        assert result_set == expected

    def testGetPieceByTitleOnline(self, mlayer, dummy):
        data = {
            "title": "blabla", "source": "MuseScore"}
        data.update(dummy)
        mlayer.add_piece(
            "file.xml", data)
        result_set = mlayer.getPieceByTitle("blabla", online=True)
        expected = ['file.xml']
        assert result_set == expected

    def testGetPieceByKeysOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "keys": {"Clarinet": [{"mode": "major",
                                       "fifths": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "C major"}]}}
        mlayer.add_piece("file.xml",
                         data)
        result_set = mlayer.get_piece_by_join([{"name": "D major"}], "keys")
        expected = []
        assert result_set == expected

    def testGetPieceByKeysOnline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "keys": {"Clarinet": [{"mode": "major",
                                       "fifths": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "treble"}]}}
        mlayer.add_piece("file.xml",
                         data)
        result_set = mlayer.get_piece_by_join(
            [{"name": "D major"}], "keys", online=True)
        expected = ['file.xml']
        assert result_set == expected

    def testGetPieceByModularityOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "keys": {"Clarinet": [{"mode": "major",
                                       "fifths": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "treble"}]}}
        mlayer.add_piece("file.xml",
                         data)
        result_set = mlayer.getPiecesByModularity("major")
        expected = []
        assert result_set == expected

    def testGetPieceByModularityOnline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "keys": {"Clarinet": [{"mode": "major",
                                       "fifths": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "treble"}]}}
        mlayer.add_piece("file.xml",
                         data)
        result_set = mlayer.getPiecesByModularity("major", online=True)
        expected = ['file.xml']
        assert result_set == expected

    def testGetPiecesByAllKeysOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "keys": {"Clarinet": [{"mode": "major",
                                       "fifths": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "treble"}]}}
        data2 = {"title": "blabla",
                 "source": "MuseScore",
                 "keys": {"Clarinet": [{"mode": "major",
                                        "fifths": 2}]},
                 "instruments": [{"name": "Clarinet"}],
                 "clefs": {"Clarinet": [{"name": "treble"}]}}
        mlayer.add_piece("file.xml",
                         data)
        mlayer.add_piece("file1.xml",
                         data2)
        result_set = mlayer.get_piece_by_all_(elem='keys')
        expected = {}
        assert result_set == expected

    def testGetPieceByAllKeysOnline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "keys": {"Clarinet": [{"mode": "major",
                                       "fifths": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "treble"}]}}
        data2 = {"title": "blabla",
                 "source": "MuseScore",
                 "keys": {"Clarinet": [{"mode": "major",
                                        "fifths": 2}]},
                 "instruments": [{"name": "Clarinet"}],
                 "clefs": {"Clarinet": [{"name": "treble"}]}}
        mlayer.add_piece("file.xml", data)
        mlayer.add_piece("file1.xml", data2)
        result_set = mlayer.get_piece_by_all_(elem='keys', online=True)
        exp = {'D major': ['file.xml', 'file1.xml']}
        assert result_set == exp

    def testGetPieceByAllClefsOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "clefs": {"Clarinet": [{"sign": "G",
                                        "line": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "keys": {"Clarinet": [{"name": "C major"}]}}
        data2 = {"title": "blabla",
                 "source": "MuseScore",
                 "clefs": {"Clarinet": [{"sign": "G",
                                         "line": 2}]},
                 "instruments": [{"name": "Clarinet"}],
                 "keys": {"Clarinet": [{"name": "C major"}]}}
        mlayer.add_piece("file.xml",
                         data)
        mlayer.add_piece("file1.xml",
                         data2)
        result_set = mlayer.get_piece_by_all_(elem='clefs')
        expected = {}
        assert result_set == expected

    def testGetPieceByAllClefsOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                         {"title": "blabla",
                             "source": "MuseScore",
                             "clefs": {"Clarinet": [{"sign": "G",
                                                     "line": 2}]},
                             "instruments": [{"name": "Clarinet"}],
                             "keys": {"Clarinet": [{"name": "C major"}]}})
        mlayer.add_piece("file1.xml",
                         {"title": "blabla",
                             "source": "MuseScore",
                             "clefs": {"Clarinet": [{"sign": "G",
                                                     "line": 2}]},
                             "instruments": [{"name": "Clarinet"}],
                             "keys": {"Clarinet": [{"name": "C major"}]}})
        result_set = mlayer.get_piece_by_all_(elem='clefs', online=True)
        exp = {"treble": ['file.xml', 'file1.xml']}
        assert result_set == exp

    def testGetPieceByAllTimeSigsOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "clefs": {"Clarinet": [{"sign": "G",
                                        "line": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "keys": {"Clarinet": [{"name": "C major"}]}}
        data2 = {"title": "blabla",
                 "source": "MuseScore",
                 "clefs": {"Clarinet": [{"sign": "G",
                                         "line": 2}]},
                 "instruments": [{"name": "Clarinet"}],
                 "keys": {"Clarinet": [{"name": "C major"}]}}
        mlayer.add_piece("file.xml", data)
        mlayer.add_piece("file1.xml", data2)
        result_set = mlayer.get_piece_by_all_(elem='time_signatures')
        exp = {}
        assert result_set == exp

    def testGetPieceByAllTimeSigsOnline(self, mlayer, dummy):
        data = {"title": "blabla", "source": "MuseScore",
                "time_signatures": [{"beat": 4, "beat_type": 4}]}
        data.update(dummy)
        data2 = {"title": "blabla", "source": "MuseScore",
                 "time_signatures": [{"beat": 4, "beat_type": 4}]}
        data2.update(dummy)
        mlayer.add_piece("file.xml", data)
        mlayer.add_piece("file1.xml", data2)
        result_set = mlayer.get_piece_by_all_(
            elem='time_signatures', online=True)
        exp = {"4/4": ['file.xml', 'file1.xml']}
        assert result_set == exp

    def testGetPieceByAllTemposOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "tempos": [{"beat": "quarter",
                            "minute": 100}]}
        data.update(dummy)
        data2 = {"title": "blabla",
                 "source": "MuseScore",
                 "tempos": [{"beat": "quarter",
                             "minute": 100}]}
        data2.update(dummy)
        mlayer.add_piece("file.xml",
                         data)
        mlayer.add_piece("file1.xml",
                         data2)
        result_set = mlayer.get_piece_by_all_(elem='tempos')
        exp = {}
        assert result_set == exp

    def testGetPieceByAllTemposOnline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "tempos": [{"beat": "quarter",
                            "minute": 100}]}
        data.update(dummy)
        data2 = copy.deepcopy(data)
        mlayer.add_piece("file.xml",
                         data)
        mlayer.add_piece("file1.xml",
                         data2)
        result_set = mlayer.get_piece_by_all_(elem='tempos', online=True)
        exp = {'quarter=100': ['file.xml', 'file1.xml']}
        assert result_set == exp

    def testGetPieceByAllInstrumentsOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "instruments": [{"name": "Clarinet"}]}
        data['clefs'] = {"Clarinet": [{"name": "treble"}]}
        data['keys'] = {"Clarinet": [{"name": "C major"}]}
        data2 = copy.deepcopy(data)
        mlayer.add_piece("file.xml",
                         data)
        mlayer.add_piece("file1.xml",
                         data2)
        result_set = mlayer.get_piece_by_all_(elem="instruments")
        exp = {}
        assert result_set == exp

    def testGetPieceByAllInstrumentsOnline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "instruments": [{"name": "Clarinet"}],
                "clefs": {'Clarinet': [{"name": "treble"}]},
                "keys": {'Clarinet': [{"name": "C major"}]}}
        data2 = copy.deepcopy(data)
        mlayer.add_piece("file.xml",
                         data)
        mlayer.add_piece("file1.xml",
                         data2)
        result_set = mlayer.get_piece_by_all_(elem='instruments', online=True)
        exp = {'Clarinet': ['file.xml', 'file1.xml']}
        assert result_set == exp

    def testGetPieceByAllComposersOffline(self, mlayer, dummy):
        data = {
            "title": "blabla", "source": "MuseScore", "composer": "Bark"}
        data.update(dummy)
        data2 = copy.deepcopy(data)
        mlayer.add_piece(
            "file.xml", data)
        mlayer.add_piece("file1.xml", data2)
        result_set = mlayer.get_piece_by_all_creators(elem='composer')
        exp = {}
        assert result_set == exp

    def testGetPieceByAllComposersOnline(self, mlayer, dummy):
        data = {
            "title": "blabla", "source": "MuseScore", "composer": "Motsart"}
        data.update(dummy)
        data2 = copy.deepcopy(data)
        mlayer.add_piece("file.xml", data)
        mlayer.add_piece("file1.xml", data2)
        result_set = mlayer.get_piece_by_all_creators(
            elem='composer', online=True)
        assert result_set == {'Motsart': ['file.xml', 'file1.xml']}

    def testGetPieceByAllLyricistsOffline(self, mlayer, dummy):
        data = {
            "title": "blabla", "source": "MuseScore", "lyricist": "Bark"}
        data.update(dummy)
        data2 = copy.deepcopy(data)
        mlayer.add_piece(
            "file.xml", data)
        mlayer.add_piece(
            "file1.xml", data2)
        result_set = mlayer.get_piece_by_all_creators(elem='lyricist')
        exp = {}
        assert result_set == exp

    def testGetPieceByAllLyricistsOnline(self, mlayer, dummy):
        data = {
            "title": "blabla", "source": "MuseScore", "lyricist": "Motsart"}
        data.update(dummy)
        data2 = copy.deepcopy(data)
        mlayer.add_piece(
            "file.xml", data)
        mlayer.add_piece(
            "file1.xml", data2)
        result_set = mlayer.get_piece_by_all_creators(
            elem='lyricist', online=True)
        assert result_set == {'Motsart': ['file.xml', 'file1.xml']}

    def testGetPieceByClefsOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "clefs": {"Clarinet": [{"sign": "G",
                                        "line": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "keys": {"Clarinet": [{"name": "C major"}]}}
        data2 = copy.deepcopy(data)
        mlayer.add_piece("file.xml",
                         data)
        mlayer.add_piece("file1.xml",
                         data2)
        result_set = mlayer.get_piece_by_join([{"name": "treble"}], "clefs")
        expected = []
        assert result_set == expected

    def testGetPieceByClefsOnline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "clefs": {"Clarinet": [{"sign": "G",
                                        "line": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "keys": {"Clarinet": [{"name": "C major"}]}}
        data2 = copy.deepcopy(data)
        mlayer.add_piece("file.xml", data)
        mlayer.add_piece("file1.xml", data2)
        result_set = mlayer.get_piece_by_join(
            [{"name": "treble"}], table="clefs", online=True)
        exp = ['file.xml', 'file1.xml']
        assert result_set == exp

    def testGetPieceByInstrumentInKeysOffline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "keys": {"Clarinet": [{"mode": "major",
                                       "fifths": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "treble"}]}}
        mlayer.add_piece("file.xml", data)
        result_set = mlayer.getPieceByInstrumentIn_(
            {"Clarinet": [{"name": "D major"}]}, table="keys")
        expected = []
        assert result_set == expected

    def testGetPieceByInstrumentInKeysOnline(self, mlayer, dummy):
        data = {"title": "blabla",
                "source": "MuseScore",
                "keys": {"Clarinet": [{"mode": "major",
                                       "fifths": 2}]},
                "instruments": [{"name": "Clarinet"}],
                "clefs": {"Clarinet": [{"name": "treble"}]}}
        mlayer.add_piece("file.xml",
                         data)
        result_set = mlayer.getPieceByInstrumentIn_(
            {"Clarinet": [{"name": "D major"}]}, table="keys", online=True)
        expected = ['file.xml']
        assert result_set == expected

    def testGetPieceByInstrumentInClefsOffline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                         {"title": "blabla",
                             "source": "MuseScore",
                             "clefs": {"Clarinet": [{"sign": "G",
                                                     "line": 2}]},
                             "instruments": [{"name": "Clarinet"}],
                             "keys": {"Clarinet": [{"name": "C major"}]}})
        result_set = mlayer.getPieceByInstrumentIn_(
            {"Clarinet": [{"name": "treble"}]}, table="clefs")
        expected = []
        assert result_set == expected

    def testGetPieceByInstrumentInClefsOnline(self, mlayer, dummy):
        mlayer.add_piece("file.xml",
                         {"title": "blabla",
                             "source": "MuseScore",
                             "clefs": {"Clarinet": [{"sign": "G",
                                                     "line": 2}]},
                             "instruments": [{"name": "Clarinet"}],
                             "keys": {"Clarinet": [{"name": "C major"}]}})
        result_set = mlayer.getPieceByInstrumentIn_(
            {"Clarinet": [{"name": "treble"}]}, online=True)
        expected = ['file.xml']
        assert result_set == expected

    def testGetPieceByMetersOffline(self, mlayer, dummy):
        data = {"title": "blabla", "source": "MuseScore",
                "time_signatures": [{"beat": 4, "beat_type": 4}]}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        result_set = mlayer.getPieceByMeter(["4/4"])
        expected = []
        assert result_set == expected

    def testGetPieceByMetersOnline(self, mlayer, dummy):
        data = {"title": "blabla", "source": "MuseScore",
                "time_signatures": [{"beat": 4, "beat_type": 4}]}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        result_set = mlayer.getPieceByMeter(["4/4"], online=True)
        expected = ['file.xml']
        assert result_set == expected

    def testGetPieceByTempoOffline(self, mlayer, dummy):
        data = {
            "title": "blabla",
            "source": "MuseScore",
            "tempos": [{"beat": "quarter", "minute": 100}]}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        result_set = mlayer.get_piece_by_tempo(["quarter=100"])
        expected = []
        assert result_set == expected

    def testGetPieceByTempoOnline(self, mlayer, dummy):
        data = {
            "title": "blabla",
            "source": "MuseScore",
            "tempos": [{"beat": "quarter", "minute": 100}]}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        result_set = mlayer.get_piece_by_tempo(["quarter=100"], online=True)
        expected = ['file.xml']
        assert result_set == expected

    def testGetPieceByInstrumentsOrSimilarOffline(self, mlayer, dummy):
        data = {
            "title": "blabla",
            "source": "MuseScore",
            "instruments": [{"name": "Clarinet"}],
            "clefs": {"Clarinet": [{"name": "treble"}]},
            "keys": {"Clarinet": [{"name": "C major"}]}}
        mlayer.add_piece("file.xml", data)
        result_set = mlayer.getPieceByInstrumentsOrSimilar(
            [{"name": "Clarinet"}])
        expected = []
        assert result_set == expected

    def testGetPieceByInstrumentsOrSimilarOnline(self, mlayer, dummy):
        data = {
            "title": "blabla",
            "source": "MuseScore",
            "instruments": [{"name": "Clarinet"}],
            "clefs": {"Clarinet": [{"name": "treble"}]},
            "keys": {"Clarinet": [{"name": "C major"}]}}
        mlayer.add_piece("file.xml", data)
        result_set = mlayer.getPieceByInstrumentsOrSimilar(
            [{"name": "Clarinet"}], online=True)
        expected = ['file.xml']
        assert result_set == expected

    def testGetPieceSource(self, mlayer, dummy):
        data = {
            "title": "blabla",
            "source": "MuseScore",
            "instruments": [{"name": "Clarinet"}],
            "clefs": {"Clarinet": [{"name": "treble"}]},
            "keys": {"Clarinet": [{"name": "C major"}]}}
        mlayer.add_piece("file.xml", data)
        result = mlayer.get_value_for_filename("file.xml", 'source')
        assert result == 'MuseScore'

    def testDownloadPiece(self, mlayer, dummy):
        mlayer.add_piece("file.xml", {
            "title": "blabla",
            "source": "MuseScore",
            "instruments": [{"name": "Clarinet"}],
            "keys": {"Clarinet": [{"name": "C major"}]},
            "clefs": {"Clarinet": [{"name": "treble"}]}})
        mlayer.update_piece("file.xml", {'source': 'local'})
        result = mlayer.get_value_for_filename("file.xml", 'source')
        assert result == 'local'
