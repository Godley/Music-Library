import unittest
import sqlite3
from implementation.primaries.ExtractMetadata.classes.DataLayer.MusicData import MusicData
import os

class TestDataLayerAdd(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testAddPiece(self):
        self.data.addPiece("file.xml", {})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('file.xml',)
        c.execute('SELECT * FROM pieces WHERE filename=?', t)
        self.assertEqual(len(c.fetchall()), 1)
        conn.close()

    def testAddPieceWithTitle(self):
        self.data.addPiece("file.xml", {"title": "blabla"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT * FROM pieces WHERE title=?', t)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

    def testAddPlaylist(self):
        self.data.addPiece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT * FROM playlists')
        self.assertEqual("play", c.fetchone()[0])
        conn.close()

    def testAddPlaylistFiles(self):
        self.data.addPiece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('play',)
        c.execute(
            '''SELECT playlist.name, piece.filename FROM playlists playlist, pieces piece, playlist_join play
                  WHERE playlist.name = ? AND play.playlist_id = playlist.ROWID AND piece.ROWID = play.piece_id''',
            t)
        result = c.fetchall()
        self.assertEqual([("play", "file.xml")], result)
        conn.close()

    def testAddPlaylistFilesMultiPlaylists(self):
        self.data.addPiece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        self.data.addPlaylist("play1", ["file.xml"])
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = [('play',), ('play1',)]
        combined = []
        for p in t:
            c.execute(
                '''SELECT playlist.name, piece.filename FROM playlists playlist, pieces piece, playlist_join play
                  WHERE playlist.name = ? AND play.playlist_id = playlist.ROWID AND piece.ROWID = play.piece_id''',
                p)
            result = c.fetchall()
            combined.extend(result)
        self.assertEqual(
            [("play", "file.xml"), ("play1", "file.xml")], combined)
        conn.close()

    def testAddPieceWithSource(self):
        self.data.addPiece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT ROWID FROM pieces')
        rowid = c.fetchone()
        t = ('MuseScore',)
        c.execute('SELECT piece_id FROM sources WHERE source=?', t)
        found = c.fetchone()
        self.assertEqual(found, rowid)
        conn.close()

    def testAddPieceWithComposer(self):
        self.data.addPiece("file.xml", {"composer": "blabla"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT ROWID FROM composers WHERE name=?', t)
        result = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE composer_id=?', result)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

    def testAddPieceWithLyricist(self):
        self.data.addPiece("file.xml", {"lyricist": "blabla"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT ROWID FROM lyricists WHERE name=?', t)
        result = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE lyricist_id=?', result)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

    def testAddPieceWithMeter(self):
        self.data.addPiece("file.xml", {"time": [{"beat": 4, "type": 4}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = (4, 4)
        c.execute('SELECT ROWID FROM timesigs WHERE beat=? and b_type=?', t)
        result = c.fetchone()
        c.execute(
            'SELECT piece_id FROM time_piece_join WHERE time_id=?',
            result)
        piece_id = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', piece_id)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

    def testAddPieceWithTempo(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 60}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ("quarter", 60)
        c.execute('SELECT ROWID FROM tempos WHERE beat=? and minute=?', t)
        result = c.fetchone()
        c.execute(
            'SELECT piece_id FROM tempo_piece_join WHERE tempo_id=?',
            result)
        piece_id = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', piece_id)
        self.assertEqual([("file.xml", "", -1, -1, 0)], c.fetchall())
        conn.close()

    def testAddPieceWithTempoOfTwoBeats(self):
        self.data.addPiece("file.xml", {"tempo": [{"beat": 4, "beat_2": 4}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = (4, 4)
        c.execute('SELECT ROWID FROM tempos WHERE beat=? and beat_2=?', t)
        result = c.fetchone()
        c.execute(
            'SELECT piece_id FROM tempo_piece_join WHERE tempo_id=?',
            result)
        piece_id = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', piece_id)
        self.assertEqual([("file.xml", "", -1, -1, 0)], c.fetchall())
        conn.close()

    def testAddPieceWithInstrumentsWithTranspositions(self):
        self.data.addPiece("file.xml",
                           {"instruments": [{"name": "Bflat clarinet",
                                             "transposition": {"diatonic": -1,
                                                               "chromatic": -2}}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('Bflat clarinet',)
        c.execute(
            'SELECT ROWID, diatonic, chromatic FROM instruments WHERE name=?',
            t)
        row = c.fetchone()
        self.assertEqual(row[1], -1)
        self.assertEqual(row[2], -2)
        c.execute(
            'SELECT piece_id FROM instruments_piece_join WHERE instrument_id=?', (row[0],))
        piece_row = c.fetchone()
        c.execute('SELECT filename FROM pieces WHERE ROWID=?', piece_row)
        self.assertEqual([("file.xml",)], c.fetchall())

    def testAddOnlinePiece(self):
        self.data.addPiece("file.xml", {"source": "MuseScore"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT source FROM sources WHERE piece_id = 1')
        row = c.fetchone()
        conn.close()
        self.assertEqual(('MuseScore',), row)

    def testAddPieceWithInstruments(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('clarinet',)
        c.execute('SELECT ROWID FROM instruments WHERE name=?', t)
        row = c.fetchone()
        c.execute(
            'SELECT piece_id FROM instruments_piece_join WHERE instrument_id=?',
            row)
        piece_row = c.fetchone()
        c.execute('SELECT filename FROM pieces WHERE ROWID=?', piece_row)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

    def testAddPieceWithKeys(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"mode": "major", "fifths": 0}]}})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('C major',)
        c.execute('SELECT ROWID FROM keys WHERE name=?', t)
        row = c.fetchone()
        c.execute('SELECT piece_id FROM key_piece_join WHERE key_id=?', row)
        piece_row = c.fetchone()
        c.execute('SELECT filename FROM pieces WHERE ROWID=?', piece_row)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

    def testAddPieceWithClefs(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"sign": "G", "line": 2}]}})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('treble',)
        c.execute('SELECT ROWID FROM clefs WHERE name=?', t)
        row = c.fetchone()
        c.execute('SELECT piece_id FROM clef_piece_join WHERE clef_id=?', row)
        piece_row = c.fetchone()
        c.execute('SELECT filename FROM pieces WHERE ROWID=?', piece_row)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

