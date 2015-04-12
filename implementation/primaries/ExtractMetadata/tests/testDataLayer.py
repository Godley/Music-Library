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
import sqlite3
from implementation.primaries.ExtractMetadata.classes.DataLayer import MusicData
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


class testDataLayerUserPlaylists(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testFetchPlaylist(self):
        self.data.addPiece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        result = self.data.getAllUserPlaylists()
        self.assertEqual({"play": ["file.xml"]}, result)

    def testFetchPlaylistByPiece(self):
        self.data.addPiece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        result = self.data.getUserPlaylistsForFile("file.xml")
        self.assertEqual({"play": ["file.xml"]}, result)

    def testFetchPlaylistByPieceWithMultiplePlaylists(self):
        self.data.addPiece("file.xml", {"title": "blabla"})
        self.data.addPlaylist("play", ["file.xml"])
        self.data.addPlaylist("play1", ["file.xml"])
        result = self.data.getUserPlaylistsForFile("file.xml")
        self.assertEqual({"play": ["file.xml"], "play1": ["file.xml"]}, result)

    def testDeletePlaylistFromTable(self):
        self.data.addPiece("file.xml", {"title": "blabla"})
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
        self.data.addPiece("file.xml", {"title": "blabla"})
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


class testDataLayerUserQueries(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testFindPieceByInstruments(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPiecesByInstruments(
                ["clarinet"]))

    def testFindPieceByMultipleInstruments(self):
        self.data.addPiece(
            "file.xml", {"instruments": [{"name": "clarinet"}, {"name": "flute"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml"], self.data.getPiecesByInstruments(["clarinet", "flute"]))

    def testFindPieceByInstrumentWhereTwoItemsExist(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "flute"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByInstruments(["flute"]))

    def testFindPieceByPartialInstrument(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "flute"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByInstruments(["fl"]))

    def testFindPieceByPartialInstrumentWhereTwoExist(self):
        self.data.addPiece(
            "file.xml", {"instruments": [{"name": "flugel Horn"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByInstruments(["fl"]))

    def testFindPieceByComposer(self):
        self.data.addPiece("file.xml", {"composer": "Bartok"})
        self.assertEqual(
            "file.xml",
            self.data.getPiecesByComposer("Bartok")[0])

    def testFindPieceByPartialComposer(self):
        self.data.addPiece("file.xml", {"composer": "Bella Bartok"})
        self.data.addPiece("file2.xml", {"composer": "Bella Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByComposer("Bartok"))

    def testFindPieceByPartialComposerWhereTwoExist(self):
        self.data.addPiece("file.xml", {"composer": "Bella Bartok"})
        self.data.addPiece("file2.xml", {"composer": "Tina Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByComposer("Bartok"))

    def testFindPieceByLyricist(self):
        self.data.addPiece("file.xml", {"lyricist": "Bartok"})
        self.assertEqual(
            "file.xml",
            self.data.getPiecesByLyricist("Bartok")[0])

    def testFindPieceByPartialLyricist(self):
        self.data.addPiece("file.xml", {"lyricist": "Bella Bartok"})
        self.data.addPiece("file2.xml", {"lyricist": "Bella Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByLyricist("Bartok"))

    def testFindPieceByPartialLyricistWhereTwoExist(self):
        self.data.addPiece("file.xml", {"lyricist": "Bella Bartok"})
        self.data.addPiece("file2.xml", {"lyricist": "Tina Bartok"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByLyricist("Bartok"))

    def testFindPieceByTitle(self):
        self.data.addPiece("file.xml", {"title": "Blabla"})
        self.assertEqual("file.xml", self.data.getPieceByTitle("Blabla")[0])

    def testFindPieceByPartialTitle(self):
        self.data.addPiece("file.xml", {"title": "abcdef"})
        self.data.addPiece("file2.xml", {"title": "abcd"})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPieceByTitle("abc"))

    def testFindPieceByKey(self):
        self.data.addPiece(
            "file.xml", {"key": {"clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.assertEqual("file.xml", self.data.getPieceByKeys(["D major"])[0])

    def testFindPieceByInstrumentInKey(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.data.addPiece(
            "file2.xml", {"key": {"flute": [{"fifths": 2, "mode": "major"}]}})
        self.assertEqual(
            "file.xml", self.data.getPieceByInstrumentInKeys({"clarinet": ["D major"]})[0])

    def testFindPieceByInstrumentInKeyWithTwoEntries(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.assertEqual(["file.xml", "file2.xml"], self.data.getPieceByInstrumentInKeys(
            {"clarinet": ["D major"]}))

    def testFindPieceByInstrumentInKeyWithTwoEntriesWhichHaveDifferentKeys(
            self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 2, "mode": "major"}]}})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"fifths": 1, "mode": "major"}]}})
        self.assertEqual(
            ["file.xml"], self.data.getPieceByInstrumentInKeys({"clarinet": ["D major"]}))

    def testFindPieceByClef(self):
        self.data.addPiece("file", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"sign": "G", "line": 2}]}})
        self.assertEqual(["file"], self.data.getPieceByClefs(["treble"]))

    def testFindPieceByInstrumentInClef(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"line": 2, "sign": "G"}]}})
        self.data.addPiece(
            "file2.xml", {"clef": {"flute": [{"line": 2, "sign": "G"}]}})
        self.assertEqual(
            "file.xml", self.data.getPieceByInstrumentInClefs({"clarinet": ["treble"]})[0])

    def testFindPieceByInstrumentInClefWithTwoEntries(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"line": 2, "sign": "G"}]}})
        self.data.addPiece("file2.xml", {"instruments": [
                           {"name": "clarinet"}], "clef": {"clarinet": [{"line": 2, "sign": "G"}]}})
        self.assertEqual(["file.xml", "file2.xml"], self.data.getPieceByInstrumentInClefs(
            {"clarinet": ["treble"]}))

    def testFindPieceByInstrumentInClefWithTwoEntriesWhichHaveDifferentKeys(
            self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"line": 2, "sign": "G"}]}})
        self.data.addPiece("file2.xml", {"instruments": [
                           {"name": "clarinet"}], "clef": {"clarinet": [{"line": 1, "sign": "G"}]}})
        self.assertEqual(
            ["file.xml"], self.data.getPieceByInstrumentInClefs({"clarinet": ["treble"]}))

    def testFindPieceByMeter(self):
        self.data.addPiece("file.xml", {"time": [{"beat": 4, "type": 4}]})
        self.assertEqual(["file.xml"], self.data.getPieceByMeter(["4/4"]))

    def testFindPieceByTempo(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 60}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["crotchet=60"]))

    def testFindInstrumentsByTranspositions(self):
        self.data.addInstruments([{"name": "clarinet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}},
                                  {"name": "trumpet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}}])
        self.assertEqual([(1, "clarinet"), (2, "trumpet")], self.data.getInstrumentByTransposition(
            {"diatonic": -1, "chromatic": -2}))

    def testFindSimilarInstruments(self):
        self.data.addInstruments([{"name": "clarinet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}},
                                  {"name": "trumpet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}}])
        self.assertEqual(
            [(2, "trumpet")], self.data.getInstrumentsBySameTranspositionAs("clarinet"))

    def testFindSimilarInstrumentsWhereOneIsDiff(self):
        self.data.addInstruments([{"name": "clarinet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}},
                                  {"name": "lute",
                                   "transposition": {"diatonic": 0,
                                                     "chromatic": -2}},
                                  {"name": "trumpet",
                                   "transposition": {"diatonic": -1,
                                                     "chromatic": -2}}])
        self.assertEqual(
            [(3, "trumpet")], self.data.getInstrumentsBySameTranspositionAs("clarinet"))

    def testFindPiecesContainingInstrumentsOrSimilar(self):
        self.data.addPiece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "transposition": {
                            "diatonic": 1, "chromatic": 2}}, {
                        "name": "violin", "transposition": {
                            "diatonic": 0, "chromatic": 0}}]})
        self.data.addInstruments(
            [{"name": "flute", "transposition": {"diatonic": 0, "chromatic": 0}}])
        self.assertEqual(["file.xml"], self.data.getPieceByInstrumentsOrSimilar(
            [{"name": "flute"}, {"name": "clarinet"}]))

    def testFindPiecesContainingInstrumentsOrSimilarWhereInstrumentNotInTable(
            self):
        self.data.addPiece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "transposition": {
                            "diatonic": 1, "chromatic": 2}}, {
                        "name": "violin", "transposition": {
                            "diatonic": 0, "chromatic": 0}}]})
        self.data.addInstruments(
            [{"name": "flute", "transposition": {"diatonic": 0, "chromatic": 0}}])
        self.assertEqual(["file.xml"],
                         self.data.getPieceByInstrumentsOrSimilar([{"name": "flute"},
                                                                   {"name": "clarinet"},
                                                                   {"name": "trumpet",
                                                                    "transposition": {"diatonic": 1,
                                                                                      "chromatic": 2,
                                                                                      "octave": 0}}]))

    def testFindByModularity(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"mode": "major", "fifths": 1}]}})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "trumpet"}], "key": {
                           "trumpet": [{"mode": "major", "fifths": 0}]}})
        self.data.addPiece("file3.xnl", {"instruments": [{"name": "flute"}], "key": {
                           "flute": [{"mode": "minor", "fifths": 0}]}})
        self.assertEqual(
            ["file.xml", "file2.xml"], self.data.getPiecesByModularity("major"))

    def testFindPieceByTempoWhereTempoIsTwoBeats(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "beat_2": "half"}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["crotchet=minim"]))

    def testFindPieceByTempoLessThanAQuaver(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "16th", "minute": 60}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["semiquaver=60"]))

    def testFindPieceByDottedTempo(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "16th.", "minute": 60}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["semiquaver.=60"]))

    def testFindPieceByTempoInAmerican(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 60}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["quarter=60"]))

    def testFindPieceByTempoWhereTempoIsTwoBeatsInAmerican(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "beat_2": "half"}]})
        self.assertEqual(
            ["file.xml"],
            self.data.getPieceByTempo(
                ["quarter=half"]))


class testDataLayerGeneral(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testGetAllPieces(self):
        self.data.addPiece("file.xml", {})
        self.data.addPiece("file2.xml", {})
        self.assertEqual(["file.xml", "file2.xml"], self.data.getFileList())

    def testGetAllPiecesWhereNoneExist(self):
        self.assertEqual([], self.data.getFileList())

    def testFindPieceByFname(self):
        self.data.addPiece("file.xml", {})
        self.assertEqual(
            [(1, "file.xml", "", -1, -1)], self.data.getPiece("file.xml"))

    def testFindAllInfoForAPiece(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "beat_2": "half"}]})
        self.assertEqual([{"title": "",
                           "composer": -1,
                           "lyricist": -1,
                           "tempos": ["quarter=half"],
                           "filename":"file.xml"}],
                         self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasKeys(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"mode": "major", "fifths": 2}]}})
        self.assertEqual([{"title": "",
                           "composer": -1,
                           "lyricist": -1,
                           "instruments": [{"name": "clarinet"}],
                           "keys": {"clarinet": ["D major"]},
                           "filename":"file.xml"}],
                         self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasClefs(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"sign": "G", "line": 2}]}})
        self.assertEqual([{"title": "",
                           "composer": -1,
                           "lyricist": -1,
                           "instruments": [{"name": "clarinet"}],
                           "clefs": {"clarinet": ["treble"]},
                           "filename":"file.xml"}],
                         self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasTransposedInstruments(self):
        self.data.addPiece("file.xml", {"instruments": [
                           {"name": "clarinet", "transposition": {"diatonic": -1, "chromatic": -2}}]})
        self.assertEqual([{"title": "",
                           "composer": -1,
                           "lyricist": -1,
                           "instruments": [{"name": "clarinet",
                                            "transposition": {"diatonic": -1,
                                                              "chromatic": -2}}],
                           "filename": "file.xml"}],
                         self.data.getAllPieceInfo(["file.xml"]))


class testDataLayerGeneratePlaylists(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testFindAllPiecesByAllKeys(self):
        self.data.addPiece("file.xml", {"key": {
                           "clari": [{"mode": "major", "fifths": 0}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file2.xml", {"key": {
                           "clari": [{"mode": "major", "fifths": 0}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file1.xml", {"key": {
                           "clari": [{"mode": "major", "fifths": 1}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file3.xml", {"key": {
                           "clari": [{"mode": "major", "fifths": 1}]}, "instruments": [{"name": "clari"}]})
        self.assertEqual({"C major": ["file.xml",
                                      "file2.xml"],
                          "G major": ["file1.xml",
                                      "file3.xml"]},
                         self.data.getPiecesByAllKeys())

    def testFindAllPiecesByAllClefs(self):
        self.data.addPiece("file.xml", {"clef": {
                           "clari": [{"sign": "G", "line": 2}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file3.xml", {"clef": {
                           "clari": [{"sign": "G", "line": 2}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file1.xml", {"clef": {
                           "clari": [{"sign": "F", "line": 4}]}, "instruments": [{"name": "clari"}]})
        self.data.addPiece("file2.xml", {"clef": {
                           "clari": [{"sign": "F", "line": 4}]}, "instruments": [{"name": "clari"}]})
        self.assertEqual({"treble": ["file.xml",
                                     "file3.xml"],
                          "bass": ["file1.xml",
                                   "file2.xml"]},
                         self.data.getPiecesByAllClefs())

    def testFindAllPiecesByAllTimeSigs(self):
        self.data.addPiece("file.xml", {"time": [{"beat": 4, "type": 4}]})
        self.data.addPiece("file1.xml", {"time": [{"beat": 4, "type": 4}]})
        self.assertEqual(
            {"4/4": ["file.xml", "file1.xml"]}, self.data.getPiecesByAllTimeSigs())

    def testFindAllPiecesByAllTempos(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "minute": 100}]})
        self.data.addPiece(
            "file3.xml", {"tempo": [{"beat": "quarter", "minute": 100}]})
        self.data.addPiece(
            "file1.xml", {"tempo": [{"beat": "quarter", "beat_2": "eighth"}]})
        self.data.addPiece(
            "file2.xml", {"tempo": [{"beat": "quarter", "beat_2": "eighth"}]})
        self.assertEqual({"quarter=eighth": ["file1.xml", "file2.xml"], "quarter=100": [
                         "file.xml", "file3.xml"]}, self.data.getPiecesByAllTempos())

    def testFindAllPiecesByAllInstruments(self):
        self.data.addPiece(
            "file.xml", {"instruments": [{"name": "clarinet"}, {"name": "flute"}]})
        self.data.addPiece(
            "file1.xml", {"instruments": [{"name": "clarinet"}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual({"flute": ["file.xml",
                                    "file2.xml"],
                          "clarinet": ["file.xml",
                                       "file1.xml"]},
                         self.data.getPiecesByAllInstruments())

    def testFindAllPiecesByAllInstrumentsWithTranspositionsAndUniqueNames(
            self):
        self.data.addPiece(
            "file.xml", {
                "instruments": [
                    {
                        "name": "clarinet", "transposition": {
                            "diatonic": 1, "chromatic": 2}}, {
                        "name": "flute"}]})
        self.data.addPiece("file1.xml", {"instruments": [
                           {"name": "clarinet", "transposition": {"diatonic": 1, "chromatic": 2}}]})
        self.data.addPiece("file2.xml", {"instruments": [{"name": "flute"}]})
        self.assertEqual(
            {
                "flute": [
                    "file.xml",
                    "file2.xml"],
                "clarinet\n(Transposed By 1 Diatonic \n2 Chromatic)": [
                    "file.xml",
                    "file1.xml"]},
            self.data.getPiecesByAllInstruments())

    def testFindAllPiecesByAllInstrumentsWithTranspositions(self):
        self.data.addPiece("file.xml",
                           {"instruments": [{"name": "clarinet"},
                                            {"name": "clarinet",
                                             "transposition": {"diatonic": 1}}]})
        self.data.addPiece(
            "file1.xml", {"instruments": [{"name": "clarinet"}]})
        self.data.addPiece("file2.xml",
                           {"instruments": [{"name": "flute"},
                                            {"name": "clarinet",
                                             "transposition": {"diatonic": 1}}]})
        self.assertEqual(
            {
                "clarinet": [
                    "file.xml",
                    "file1.xml"],
                "clarinet\n(Transposed By 1 Diatonic \n)": [
                    "file.xml",
                    "file2.xml"]},
            self.data.getPiecesByAllInstruments())

    def testFindAllPiecesByAllComposers(self):
        self.data.addPiece("file.xml", {"composer": "Charlotte"})
        self.data.addPiece("file1.xml", {"composer": "Charlie"})
        self.data.addPiece("file2.xml", {"composer": "Charlie"})
        self.assertEqual(
            {"Charlie": ["file1.xml", "file2.xml"]}, self.data.getPiecesByAllComposers())

    def testFindAllPiecesByAllLyricists(self):
        self.data.addPiece("file.xml", {"lyricist": "Charlotte"})
        self.data.addPiece("file1.xml", {"lyricist": "Charlie"})
        self.data.addPiece("file2.xml", {"lyricist": "Charlie"})
        self.assertEqual(
            {"Charlie": ["file1.xml", "file2.xml"]}, self.data.getPiecesByAllLyricists())

    def testFindAllPiecesByAllKeysWithTransposedInstruments(self):
        self.data.addPiece("file.xml",
                           {"key": {"clari": [{"mode": "major",
                                               "fifths": 0}]},
                            "instruments": [{"name": "clari",
                                             "transposition": {"diatonic": 1}}]})
        self.data.addPiece("file1.xml",
                           {"key": {"clarin": [{"mode": "major",
                                                "fifths": 1}]},
                            "instruments": [{"name": "clarin"}]})
        self.data.addPiece("file2.xml",
                           {"key": {"clarin": [{"mode": "major",
                                                "fifths": 1}]},
                            "instruments": [{"name": "clarin"}]})
        self.assertEqual(
            {"G major": ["file1.xml", "file2.xml"]}, self.data.getPiecesByAllKeys())

    def testArchivePiece(self):
        self.data.addPiece("file.xml", {"instruments": [
                           {"name": "clarinet", "transposition": {"diatonic": -1, "chromatic": -2}}]})
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 1)
        self.data.archivePieces(["file.xml"])
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 0)
        self.assertEqual(len(self.data.getArchivedPieces()), 1)

    def testRemovePiece(self):
        self.data.addPiece("file.xml", {"instruments": [
                           {"name": "clarinet", "transposition": {"diatonic": -1, "chromatic": -2}}]})
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 1)
        self.data.removePieces(["file.xml"])
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 0)
        self.assertEqual(len(self.data.getArchivedPieces()), 0)


class testDataLayerOnlineSearching(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testGetPieceListOffline(self):
        self.data.addPiece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        self.data.addPiece("file1.xml", {"composer": "blabla"})
        result_set = self.data.getFileList()
        self.assertEqual(result_set, ["file1.xml"])

    def testGetPieceListOnline(self):
        self.data.addPiece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        self.data.addPiece("file1.xml", {"composer": "blabla"})
        result_set = self.data.getFileList(online=True)
        self.assertEqual(result_set, ["file.xml"])

    def testGetPieceOffline(self):
        self.data.addPiece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = self.data.getPiece("file.xml")
        self.assertEqual(result_set, [])

    def testGetPieceOnline(self):
        self.data.addPiece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = self.data.getPiece("file.xml", online=True)
        self.assertEqual(result_set, [(1, 'file.xml', '', 1, -1)])

    def testGetPieceByInstrumentsOffline(self):
        self.data.addPiece("file.xml",
                           {"composer": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByInstruments(["Clarinet"])
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentsOnline(self):
        self.data.addPiece("file.xml",
                           {"composer": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByInstruments(
            ["Clarinet"],
            online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByComposerOffline(self):
        self.data.addPiece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = self.data.getPiecesByComposer("blabla")
        self.assertEqual(result_set, [])

    def testGetPieceByComposerOnline(self):
        self.data.addPiece(
            "file.xml", {
                "composer": "blabla", "source": "MuseScore"})
        result_set = self.data.getPiecesByComposer("blabla", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByLyricistOffline(self):
        self.data.addPiece(
            "file.xml", {
                "lyricist": "blabla", "source": "MuseScore"})
        result_set = self.data.getPiecesByLyricist("blabla")
        self.assertEqual(result_set, [])

    def testGetPieceByLyricistOnline(self):
        self.data.addPiece(
            "file.xml", {
                "lyricist": "blabla", "source": "MuseScore"})
        result_set = self.data.getPiecesByLyricist("blabla", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByTitleOffline(self):
        self.data.addPiece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore"})
        result_set = self.data.getPieceByTitle("blabla")
        self.assertEqual(result_set, [])

    def testGetPieceByTitleOnline(self):
        self.data.addPiece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore"})
        result_set = self.data.getPieceByTitle("blabla", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByKeysOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByKeys(["D major"])
        self.assertEqual(result_set, [])

    def testGetPieceByKeysOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByKeys(["D major"], online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByModularityOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByModularity("major")
        self.assertEqual(result_set, [])

    def testGetPieceByModularityOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByModularity("major", online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPiecesByAllKeysOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllKeys()
        self.assertEqual(result_set, {})

    def testGetPieceByAllKeysOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllKeys(online=True)
        self.assertEqual(result_set, {'D major': ['file.xml', 'file1.xml']})

    def testGetPieceByAllClefsOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllClefs()
        self.assertEqual(result_set, {})

    def testGetPieceByAllClefsOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllClefs(online=True)
        self.assertEqual(result_set, {"treble": ['file.xml', 'file1.xml']})

    def testGetPieceByAllTimeSigsOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllTimeSigs()
        self.assertEqual(result_set, {})

    def testGetPieceByAllTimeSigsOnline(self):
        self.data.addPiece("file.xml", {
                           "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        self.data.addPiece("file1.xml", {
                           "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = self.data.getPiecesByAllTimeSigs(online=True)
        self.assertEqual(result_set, {"4/4": ['file.xml', 'file1.xml']})

    def testGetPieceByAllTemposOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "tempo": [{"beat": "quarter",
                                       "minute": 100}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "tempo": [{"beat": "quarter",
                                       "minute": 100}]})
        result_set = self.data.getPiecesByAllTempos()
        self.assertEqual(result_set, {})

    def testGetPieceByAllTemposOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "tempo": [{"beat": "quarter",
                                       "minute": 100}]})
        self.data.addPiece("file1.xml",
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
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllInstruments()
        self.assertEqual(result_set, {})

    def testGetPieceByAllInstrumentsOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPiecesByAllInstruments(online=True)
        self.assertEqual(result_set, {'Clarinet': ['file.xml', 'file1.xml']})

    def testGetPieceByAllComposersOffline(self):
        self.data.addPiece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Bark"})
        self.data.addPiece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Bark"})
        result_set = self.data.getPiecesByAllComposers()
        self.assertEqual(result_set, {})

    def testGetPieceByAllComposersOnline(self):
        self.data.addPiece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Motsart"})
        self.data.addPiece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "composer": "Motsart"})
        result_set = self.data.getPiecesByAllComposers(online=True)
        self.assertEqual(result_set, {'Motsart': ['file.xml', 'file1.xml']})

    def testGetPieceByAllLyricistsOffline(self):
        self.data.addPiece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Bark"})
        self.data.addPiece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Bark"})
        result_set = self.data.getPiecesByAllLyricists()
        self.assertEqual(result_set, {})

    def testGetPieceByAllLyricistsOnline(self):
        self.data.addPiece(
            "file.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Motsart"})
        self.data.addPiece(
            "file1.xml", {
                "title": "blabla", "source": "MuseScore", "lyricist": "Motsart"})
        result_set = self.data.getPiecesByAllLyricists(online=True)
        self.assertEqual(result_set, {'Motsart': ['file.xml', 'file1.xml']})

    def testGetPieceByClefsOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByClefs(["treble"])
        self.assertEqual(result_set, [])

    def testGetPieceByClefsOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        self.data.addPiece("file1.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByClefs(["treble"], online=True)
        self.assertEqual(result_set, ['file.xml', 'file1.xml'])

    def testGetPieceByInstrumentInKeysOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByInstrumentInKeys(
            {"Clarinet": ["D major"]})
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentInKeysOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "key": {"Clarinet": [{"mode": "major",
                                                  "fifths": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByInstrumentInKeys(
            {"Clarinet": ["D major"]}, online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByInstrumentInClefsOffline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByInstrumentInClefs(
            {"Clarinet": ["treble"]})
        self.assertEqual(result_set, [])

    def testGetPieceByInstrumentInClefsOnline(self):
        self.data.addPiece("file.xml",
                           {"title": "blabla",
                            "source": "MuseScore",
                            "clef": {"Clarinet": [{"sign": "G",
                                                   "line": 2}]},
                               "instruments": [{"name": "Clarinet"}]})
        result_set = self.data.getPieceByInstrumentInClefs(
            {"Clarinet": ["treble"]}, online=True)
        self.assertEqual(result_set, ['file.xml'])

    def testGetPieceByMetersOffline(self):
        self.data.addPiece("file.xml", {
                           "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = self.data.getPieceByMeter(["4/4"])
        self.assertEqual(result_set, [])

    def testGetPieceByMetersOnline(self):
        self.data.addPiece("file.xml", {
                           "title": "blabla", "source": "MuseScore", "time": [{"beat": 4, "type": 4}]})
        result_set = self.data.getPieceByMeter(["4/4"], online=True)
        self.assertEqual(result_set, ['file.xml'])
