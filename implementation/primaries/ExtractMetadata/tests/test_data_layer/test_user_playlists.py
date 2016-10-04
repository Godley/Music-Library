import unittest
import sqlite3
from implementation.primaries.ExtractMetadata.classes.DataLayer.musicdata import MusicData
import os


class TestDataLayerUserPlaylists(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testFetchPlaylist(self):
        self.data.add_piece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        result = self.data.getAllUserPlaylists()
        self.assertEqual({"play": ["file.xml"]}, result)

    def testFetchPlaylistByPiece(self):
        self.data.add_piece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        result = self.data.getUserPlaylistsForFile("file.xml")
        self.assertEqual({"play": ["file.xml"]}, result)

    def testFetchPlaylistByPieceWithMultiplePlaylists(self):
        self.data.add_piece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        self.data.addPlaylist("play1", ["file.xml"])
        result = self.data.getUserPlaylistsForFile("file.xml")
        self.assertEqual({"play": ["file.xml"], "play1": ["file.xml"]}, result)

    def testDeletePlaylistFromTable(self):
        self.data.add_piece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        self.data.deletePlaylist("play")
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        query = 'SELECT * FROM playlists WHERE name = ?'
        c.execute(query, ('play',))
        result = c.fetchall()
        conn.close()
        self.assertEqual(result, [])

    def testDeletePlaylistFromJoinTable(self):
        self.data.add_piece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        query = 'SELECT ROWID FROM playlists WHERE name = ?'
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute(query, ('play',))
        row_id = c.fetchone()
        self.data.deletePlaylist("play")
        join_query = 'SELECT * FROM playlist_join WHERE playlist_id = ?'
        c.execute(join_query, row_id)
        result = c.fetchall()
        conn.close()
        self.assertEqual(result, [])
