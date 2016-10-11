import unittest
import sqlite3
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
import os


class TestDataLayerUserPlaylists(object):

    def testFetchPlaylist(self, mlayer, dummy):
        data = {"title": "blabla"}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        mlayer.add_playlist("play", ["file.xml"])
        result = mlayer.get_all_user_playlists()
        assert {"play": ["file.xml"]} == result

    def testFetchPlaylistByPiece(self, mlayer, dummy):
        data = {"title": "blabla"}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        mlayer.add_playlist("play", ["file.xml"])
        result = mlayer.get_user_playlists_by_filename("file.xml")
        assert {"play": ["file.xml"]} == result

    def testFetchPlaylistByPieceWithMultiplePlaylists(self, mlayer, dummy):
        data = {"title": "blabla"}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        mlayer.add_playlist("play", ["file.xml"])
        mlayer.add_playlist("play1", ["file.xml"])
        result = mlayer.get_user_playlists_by_filename("file.xml")
        assert {"play": ["file.xml"], "play1": ["file.xml"]} == result

    def testDeletePlaylistFromTable(self, mlayer, dummy):
        data = {"title": "blabla"}
        data.update(dummy)
        mlayer.add_piece("file.xml", data)
        mlayer.add_playlist("play", ["file.xml"])
        mlayer.delete_playlist("play")
        result = mlayer.get_playlist("play")
        assert result == []
