"""
there's a lot of tests in here, so I've sorted them a bit:
testDataLayerAdd: as the title suggests, checks adding pieces puts stuff in the right tables
testDataLayerUserPlaylists: anything relating to user created playlists, so stuff in the playlist and playlist join table
testDataLayerUserQueries: anything which will be used when a user types something into the search bar
testDataLayerGeneratePlaylists: anything which will be used to generate playlists of related data
testDataLayerGeneral: anything which doesn't fit into the other class categories so generally searching for specific pieces
testDataLayerOnlineSearching: anything relating to the diff between each method when online is set to false or true.
                                This is to confirm that API searching does not get mixed up with local searching
"""
import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
import os
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict
import pytest


class TestSuiteDataLayerGeneral(object):

    def test_get_all_pieces(self, mlayer, dummy):
        mlayer.add_piece("file.xml", dummy)
        mlayer.add_piece("file2.xml", dummy)
        expecting = ["file.xml", "file2.xml"]
        result = mlayer.get_file_list()
        for item in expecting:
            assert item in result

    def test_get_all_pieces_where_none_exists(self, mlayer):
        assert mlayer.get_file_list() == []

    def testFindAllInfoForAPiece(self, mlayer, dummy, dummy_res):
        data = {"tempos": [{"beat": "quarter", "beat_2": "half"}]}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        entry = {"tempos": ["quarter=half"],
                 "filename": "file.xml",
                 }
        entry.update(dummy_res)
        result = mlayer.get_all_piece_info(["file.xml"])
        assert entry == result[0]

    def testFindAllInfoForAPieceWhereHasKeys(self, mlayer, dummy, dummy_res):
        data = {"instruments": [{"name": "wibble"}], "keys": {
            "wibble": [{"mode": "major", "fifths": 2, "name": 'D major'}]}}
        data['clefs'] = dummy['clefs']
        mlayer.add_piece("file.xml", data)

        results = mlayer.get_all_piece_info(["file.xml"])
        exp = {"instruments": dummy_res['instruments'],
               "keys": {"wibble": ["D major"]},
               "filename": "file.xml"}
        exp['clefs'] = dummy_res['clefs']
        assert results[0] == exp

    def testFindAllInfoForAPieceWhereHasClefs(self, mlayer, dummy, dummy_res):
        data = {"instruments": [{"name": "wibble"}], "clefs": {
            "wibble": [{"sign": "G", "line": 2}]}}
        data['keys'] = dummy['keys']
        mlayer.add_piece("file.xml", data)

        exp = {"instruments": dummy_res['instruments'],
               "clefs": {"wibble": ["treble"]},
               "filename": "file.xml"}
        exp['keys'] = dummy_res['keys']
        result = mlayer.get_all_piece_info(["file.xml"])
        assert exp == result[0]

    def testFindAllInfoForAPieceWhereHasTransposedInstruments(
            self, mlayer, dummy, dummy_res):
        data = {"instruments": [
            {"name": "wibble", "diatonic": -1, "chromatic": -2}]}
        data['keys'] = dummy['keys']
        data['clefs'] = dummy['clefs']
        mlayer.add_piece("file.xml", data)
        exp = {"instruments": [hashdict(name="wibble",
                                        diatonic=-1,
                                        chromatic=-2)],
               'filename': 'file.xml'}
        exp['keys'] = dummy_res['keys']
        exp['clefs'] = dummy_res['clefs']
        result = mlayer.get_all_piece_info(["file.xml"])
        assert result[0] == exp
