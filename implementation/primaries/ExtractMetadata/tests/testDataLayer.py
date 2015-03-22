import unittest
import sqlite3
from implementation.primaries.ExtractMetadata.classes.DataLayer import MusicData
import os

class testDataLayer(unittest.TestCase):
    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testAddPiece(self):
        self.data.addPiece("file.xml",{})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('file.xml',)
        c.execute('SELECT * FROM pieces WHERE filename=?', t)
        self.assertEqual(len(c.fetchall()), 1)

    def testAddPieceWithTitle(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT * FROM pieces WHERE title=?', t)
        self.assertEqual("file.xml", c.fetchone()[0])

    def testAddPlaylist(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        self.data.addPlaylist("play",["file.xml"])
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT * FROM playlists')
        self.assertEqual("play", c.fetchone()[0])
        conn.close()

    def testAddPlaylistFiles(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        self.data.addPlaylist("play",["file.xml"])
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('play',)
        c.execute('''SELECT playlist.name, piece.filename FROM playlists playlist, pieces piece, playlist_join play
                  WHERE playlist.name = ? AND play.playlist_id = playlist.ROWID AND piece.ROWID = play.piece_id''', t)
        result = c.fetchall()
        self.assertEqual([("play","file.xml")], result)
        conn.close()

    def testAddPlaylistFilesMultiPlaylists(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        self.data.addPlaylist("play",["file.xml"])
        self.data.addPlaylist("play1",["file.xml"])
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = [('play',),('play1',)]
        combined = []
        for p in t:
            c.execute('''SELECT playlist.name, piece.filename FROM playlists playlist, pieces piece, playlist_join play
                  WHERE playlist.name = ? AND play.playlist_id = playlist.ROWID AND piece.ROWID = play.piece_id''', p)
            result = c.fetchall()
            combined.extend(result)
        self.assertEqual([("play","file.xml"),("play1","file.xml")], combined)
        conn.close()

    def testFetchPlaylist(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        self.data.addPlaylist("play",["file.xml"])
        result = self.data.getAllUserPlaylists()
        self.assertEqual({"play":["file.xml"]}, result)

    def testFetchPlaylistByPiece(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        self.data.addPlaylist("play",["file.xml"])
        result = self.data.getUserPlaylistsForFile("file.xml")
        self.assertEqual({"play":["file.xml"]}, result)

    def testFetchPlaylistByPieceWithMultiplePlaylists(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        self.data.addPlaylist("play",["file.xml"])
        self.data.addPlaylist("play1",["file.xml"])
        result = self.data.getUserPlaylistsForFile("file.xml")
        self.assertEqual({"play":["file.xml"], "play1":["file.xml"]}, result)

    def testDeletePlaylistFromTable(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        self.data.addPlaylist("play",["file.xml"])
        self.data.deletePlaylist("play")
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        query = 'SELECT * FROM playlists WHERE name = ?'
        c.execute(query, ('play',))
        result = c.fetchall()
        conn.close()
        self.assertEqual(result, [])

    def testDeletePlaylistFromJoinTable(self):
        self.data.addPiece("file.xml",{"title":"blabla"})
        self.data.addPlaylist("play",["file.xml"])
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

    def testAddPieceWithComposer(self):
        self.data.addPiece("file.xml",{"composer":"blabla"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT ROWID FROM composers WHERE name=?', t)
        result = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE composer_id=?', result)
        self.assertEqual("file.xml", c.fetchone()[0])

    def testAddPieceWithLyricist(self):
        self.data.addPiece("file.xml",{"lyricist":"blabla"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT ROWID FROM lyricists WHERE name=?', t)
        result = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE lyricist_id=?', result)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

    def testAddPieceWithMeter(self):
        self.data.addPiece("file.xml",{"time":[{"beat":4,"type":4}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = (4,4)
        c.execute('SELECT ROWID FROM timesigs WHERE beat=? and b_type=?', t)
        result = c.fetchone()
        c.execute('SELECT piece_id FROM time_piece_join WHERE time_id=?',result)
        piece_id = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', piece_id)
        self.assertEqual("file.xml", c.fetchone()[0])
        conn.close()

    def testAddPieceWithTempo(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"quarter","minute":60}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ("quarter",60)
        c.execute('SELECT ROWID FROM tempos WHERE beat=? and minute=?', t)
        result = c.fetchone()
        c.execute('SELECT piece_id FROM tempo_piece_join WHERE tempo_id=?',result)
        piece_id = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', piece_id)
        self.assertEqual([("file.xml","",-1,-1,0)], c.fetchall())
        conn.close()

    def testAddPieceWithTempoOfTwoBeats(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":4,"beat_2":4}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = (4,4)
        c.execute('SELECT ROWID FROM tempos WHERE beat=? and beat_2=?', t)
        result = c.fetchone()
        c.execute('SELECT piece_id FROM tempo_piece_join WHERE tempo_id=?',result)
        piece_id = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', piece_id)
        self.assertEqual([("file.xml","",-1,-1,0)], c.fetchall())

    def testGetAllPieces(self):
        self.data.addPiece("file.xml",{})
        self.data.addPiece("file2.xml",{})
        self.assertEqual(["file.xml","file2.xml"], self.data.getFileList())

    def testGetAllPiecesWhereNoneExist(self):
        self.assertEqual([], self.data.getFileList())

    def testFindPieceByFname(self):
        self.data.addPiece("file.xml",{})
        self.assertEqual([(1, "file.xml","",-1,-1)], self.data.getPiece("file.xml"))

    def testAddPieceWithInstrumentsWithTranspositions(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"Bflat clarinet","transposition":{"diatonic":-1,"chromatic":-2}}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('Bflat clarinet',)
        c.execute('SELECT ROWID, diatonic, chromatic FROM instruments WHERE name=?', t)
        row = c.fetchone()
        self.assertEqual(row[1],-1)
        self.assertEqual(row[2],-2)
        c.execute('SELECT piece_id FROM instruments_piece_join WHERE instrument_id=?', (row[0],))
        piece_row = c.fetchone()
        c.execute('SELECT filename FROM pieces WHERE ROWID=?', piece_row)
        self.assertEqual([("file.xml",)], c.fetchall())

    def testAddPieceWithInstruments(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('clarinet',)
        c.execute('SELECT ROWID FROM instruments WHERE name=?', t)
        row = c.fetchone()
        c.execute('SELECT piece_id FROM instruments_piece_join WHERE instrument_id=?', row)
        piece_row = c.fetchone()
        c.execute('SELECT filename FROM pieces WHERE ROWID=?', piece_row)
        self.assertEqual("file.xml", c.fetchone()[0])

    def testAddPieceWithKeys(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}], "key":{"clarinet":[{"mode":"major","fifths":0}]}})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('C major',)
        c.execute('SELECT ROWID FROM keys WHERE name=?', t)
        row = c.fetchone()
        c.execute('SELECT piece_id FROM key_piece_join WHERE key_id=?', row)
        piece_row = c.fetchone()
        c.execute('SELECT filename FROM pieces WHERE ROWID=?', piece_row)
        self.assertEqual("file.xml", c.fetchone()[0])

    def testAddPieceWithClefs(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}], "clef":{"clarinet":[{"sign":"G","line":2}]}})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('treble',)
        c.execute('SELECT ROWID FROM clefs WHERE name=?', t)
        row = c.fetchone()
        c.execute('SELECT piece_id FROM clef_piece_join WHERE clef_id=?', row)
        piece_row = c.fetchone()
        c.execute('SELECT filename FROM pieces WHERE ROWID=?', piece_row)
        self.assertEqual("file.xml", c.fetchone()[0])

    def testFindPieceByInstruments(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}]})
        self.assertEqual(["file.xml"], self.data.getPiecesByInstruments(["clarinet"]))

    def testFindPieceByMultipleInstruments(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"},{"name":"flute"}]})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"flute"}]})
        self.assertEqual(["file.xml"], self.data.getPiecesByInstruments(["clarinet", "flute"]))

    def testFindPieceByInstrumentWhereTwoItemsExist(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"flute"}]})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"flute"}]})
        self.assertEqual(["file.xml","file2.xml"], self.data.getPiecesByInstruments(["flute"]))

    def testFindPieceByComposer(self):
        self.data.addPiece("file.xml",{"composer":"Bartok"})
        self.assertEqual("file.xml", self.data.getPiecesByComposer("Bartok")[0])

    def testFindPieceByLyricist(self):
        self.data.addPiece("file.xml",{"lyricist":"Bartok"})
        self.assertEqual("file.xml", self.data.getPiecesByLyricist("Bartok")[0])

    def testFindPieceByTitle(self):
        self.data.addPiece("file.xml",{"title":"Blabla"})
        self.assertEqual("file.xml", self.data.getPieceByTitle("Blabla")[0])

    def testFindAllPiecesByAllKeys(self):
        self.data.addPiece("file.xml",{"key":{"clari":[{"mode":"major","fifths":0}]}, "instruments":[{"name":"clari"}]})
        self.data.addPiece("file2.xml",{"key":{"clari":[{"mode":"major","fifths":0}]}, "instruments":[{"name":"clari"}]})
        self.data.addPiece("file1.xml",{"key":{"clari":[{"mode":"major","fifths":1}]}, "instruments":[{"name":"clari"}]})
        self.data.addPiece("file3.xml",{"key":{"clari":[{"mode":"major","fifths":1}]}, "instruments":[{"name":"clari"}]})
        self.assertEqual({"C major":["file.xml","file2.xml"],"G major":["file1.xml","file3.xml"]}, self.data.getPiecesByAllKeys())

    def testFindAllPiecesByAllClefs(self):
        self.data.addPiece("file.xml",{"clef":{"clari":[{"sign":"G","line":2}]}, "instruments":[{"name":"clari"}]})
        self.data.addPiece("file3.xml",{"clef":{"clari":[{"sign":"G","line":2}]}, "instruments":[{"name":"clari"}]})
        self.data.addPiece("file1.xml",{"clef":{"clari":[{"sign":"F","line":4}]}, "instruments":[{"name":"clari"}]})
        self.data.addPiece("file2.xml",{"clef":{"clari":[{"sign":"F","line":4}]}, "instruments":[{"name":"clari"}]})
        self.assertEqual({"treble":["file.xml","file3.xml"],"bass":["file1.xml","file2.xml"]}, self.data.getPiecesByAllClefs())

    def testFindAllPiecesByAllTimeSigs(self):
        self.data.addPiece("file.xml",{"time":[{"beat":4,"type":4}]})
        self.data.addPiece("file1.xml",{"time":[{"beat":4,"type":4}]})
        self.assertEqual({"4/4":["file.xml","file1.xml"]}, self.data.getPiecesByAllTimeSigs())

    def testFindAllPiecesByAllTempos(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"quarter","minute":100}]})
        self.data.addPiece("file3.xml",{"tempo":[{"beat":"quarter","minute":100}]})
        self.data.addPiece("file1.xml",{"tempo":[{"beat":"quarter","beat_2":"eighth"}]})
        self.data.addPiece("file2.xml",{"tempo":[{"beat":"quarter","beat_2":"eighth"}]})
        self.assertEqual({"quarter=eighth":["file1.xml","file2.xml"],"quarter=100":["file.xml","file3.xml"]}, self.data.getPiecesByAllTempos())

    def testFindAllPiecesByAllInstruments(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}, {"name":"flute"}]})
        self.data.addPiece("file1.xml",{"instruments":[{"name":"clarinet"}]})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"flute"}]})
        self.assertEqual({"flute":["file.xml", "file2.xml"],"clarinet":["file.xml", "file1.xml"]}, self.data.getPiecesByAllInstruments())


    def testFindAllPiecesByAllInstrumentsWithTranspositionsAndUniqueNames(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet","transposition":{"diatonic":1,"chromatic":2}}, {"name":"flute"}]})
        self.data.addPiece("file1.xml",{"instruments":[{"name":"clarinet","transposition":{"diatonic":1,"chromatic":2}}]})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"flute"}]})
        self.assertEqual({"flute":["file.xml", "file2.xml"],"clarinet\n(Transposed By 1 Diatonic \n2 Chromatic)":["file.xml", "file1.xml"]}, self.data.getPiecesByAllInstruments())


    def testFindAllPiecesByAllInstrumentsWithTranspositions(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}, {"name":"clarinet","transposition":{"diatonic":1}}]})
        self.data.addPiece("file1.xml",{"instruments":[{"name":"clarinet"}]})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"flute"}, {"name":"clarinet","transposition":{"diatonic":1}}]})
        self.assertEqual({"clarinet":["file.xml", "file1.xml"], "clarinet\n(Transposed By 1 Diatonic \n)":["file.xml","file2.xml"]}, self.data.getPiecesByAllInstruments())

    def testFindAllPiecesByAllComposers(self):
        self.data.addPiece("file.xml",{"composer":"Charlotte"})
        self.data.addPiece("file1.xml",{"composer":"Charlie"})
        self.data.addPiece("file2.xml",{"composer":"Charlie"})
        self.assertEqual({"Charlie":["file1.xml","file2.xml"]}, self.data.getPiecesByAllComposers())

    def testFindAllPiecesByAllLyricists(self):
        self.data.addPiece("file.xml",{"lyricist":"Charlotte"})
        self.data.addPiece("file1.xml",{"lyricist":"Charlie"})
        self.data.addPiece("file2.xml",{"lyricist":"Charlie"})
        self.assertEqual({"Charlie":["file1.xml","file2.xml"]}, self.data.getPiecesByAllLyricists())

    def testFindAllPiecesByAllKeysWithTransposedInstruments(self):
        self.data.addPiece("file.xml",{"key":{"clari":[{"mode":"major","fifths":0}]}, "instruments":[{"name":"clari","transposition":{"diatonic":1}}]})
        self.data.addPiece("file1.xml",{"key":{"clarin":[{"mode":"major","fifths":1}]}, "instruments":[{"name":"clarin"}]})
        self.data.addPiece("file2.xml",{"key":{"clarin":[{"mode":"major","fifths":1}]}, "instruments":[{"name":"clarin"}]})
        self.assertEqual({"G major":["file1.xml","file2.xml"]}, self.data.getPiecesByAllKeys())

    def testFindPieceByKey(self):
        self.data.addPiece("file.xml",{"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.assertEqual("file.xml", self.data.getPieceByKeys(["D major"])[0])

    def testFindPieceByInstrumentInKey(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}],"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.data.addPiece("file2.xml",{"key":{"flute":[{"fifths":2,"mode":"major"}]}})
        self.assertEqual("file.xml", self.data.getPieceByInstrumentInKey({"clarinet":"D major"})[0])

    def testFindPieceByInstrumentInKeyWithTwoEntries(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}],"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"clarinet"}],"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.assertEqual(["file.xml","file2.xml"], self.data.getPieceByInstrumentInKey({"clarinet":"D major"}))

    def testFindPieceByInstrumentInKeyWithTwoEntriesWhichHaveDifferentKeys(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}],"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"clarinet"}],"key":{"clarinet":[{"fifths":1,"mode":"major"}]}})
        self.assertEqual(["file.xml"], self.data.getPieceByInstrumentInKey({"clarinet":"D major"}))

    def testFindPieceByClef(self):
        self.data.addPiece("file", {"instruments":[{"name":"clarinet"}],"clef":{"clarinet":[{"sign":"G","line":2}]}})
        self.assertEqual(["file"], self.data.getPieceByClefs(["treble"]))

    def testFindPieceByInstrumentInClef(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}],"clef":{"clarinet":[{"line":2,"sign":"G"}]}})
        self.data.addPiece("file2.xml",{"clef":{"flute":[{"line":2,"sign":"G"}]}})
        self.assertEqual("file.xml", self.data.getPieceByInstrumentInClef({"clarinet":"treble"})[0])

    def testFindPieceByInstrumentInClefWithTwoEntries(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}],"clef":{"clarinet":[{"line":2,"sign":"G"}]}})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"clarinet"}],"clef":{"clarinet":[{"line":2,"sign":"G"}]}})
        self.assertEqual(["file.xml","file2.xml"], self.data.getPieceByInstrumentInClef({"clarinet":"treble"}))

    def testFindPieceByInstrumentInClefWithTwoEntriesWhichHaveDifferentKeys(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}],"clef":{"clarinet":[{"line":2,"sign":"G"}]}})
        self.data.addPiece("file2.xml",{"instruments":[{"name":"clarinet"}],"clef":{"clarinet":[{"line":1,"sign":"G"}]}})
        self.assertEqual(["file.xml"], self.data.getPieceByInstrumentInClef({"clarinet":"treble"}))

    def testFindPieceByMeter(self):
        self.data.addPiece("file.xml",{"time":[{"beat":4,"type":4}]})
        self.assertEqual(["file.xml"], self.data.getPieceByMeter(["4/4"]))

    def testFindPieceByTempo(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"quarter","minute":60}]})
        self.assertEqual(["file.xml"], self.data.getPieceByTempo(["crotchet=60"]))

    def testFindInstrumentsByTranspositions(self):
        self.data.addInstruments([{"name":"clarinet","transposition":{"diatonic":-1,"chromatic":-2}}, {"name":"trumpet", "transposition":{"diatonic":-1,"chromatic":-2}}])
        self.assertEqual([(1, "clarinet"),(2, "trumpet")], self.data.getInstrumentByTransposition({"diatonic":-1,"chromatic":-2}))

    def testFindSimilarInstruments(self):
        self.data.addInstruments([{"name":"clarinet","transposition":{"diatonic":-1,"chromatic":-2}}, {"name":"trumpet", "transposition":{"diatonic":-1,"chromatic":-2}}])
        self.assertEqual([(2, "trumpet")], self.data.getInstrumentsBySameTranspositionAs("clarinet"))

    def testFindSimilarInstrumentsWhereOneIsDiff(self):
        self.data.addInstruments([{"name":"clarinet","transposition":{"diatonic":-1,"chromatic":-2}},
                                  {"name":"lute", "transposition":{"diatonic":0,"chromatic":-2}},
                                  {"name":"trumpet", "transposition":{"diatonic":-1,"chromatic":-2}}
                                  ]
                                )
        self.assertEqual([(3, "trumpet")], self.data.getInstrumentsBySameTranspositionAs("clarinet"))

    def testFindPiecesContainingInstrumentsOrSimilar(self):
        self.data.addPiece("file.xml", {"instruments":
                                            [{"name":"clarinet","transposition":{"diatonic":1,"chromatic":2}},
                                                {"name":"violin","transposition":{"diatonic":0,"chromatic":0}}
                                              ]
                                             })
        self.data.addInstruments([{"name":"flute","transposition":{"diatonic":0,"chromatic":0}}])
        self.assertEqual(["file.xml"], self.data.getPieceByInstrumentsOrSimilar([{"name":"flute"},
                                                                                 {"name":"clarinet"}]))

    def testFindPiecesContainingInstrumentsOrSimilarWhereInstrumentNotInTable(self):
        self.data.addPiece("file.xml", {"instruments":
                                            [{"name":"clarinet","transposition":{"diatonic":1,"chromatic":2}},
                                                {"name":"violin","transposition":{"diatonic":0,"chromatic":0}}
                                              ]
                                             })
        self.data.addInstruments([{"name":"flute","transposition":{"diatonic":0,"chromatic":0}}])
        self.assertEqual(["file.xml"], self.data.getPieceByInstrumentsOrSimilar([{"name":"flute"},
                                                                                 {"name":"clarinet"},
                                                                                {"name":"trumpet","transposition":{"diatonic":1,"chromatic":2,"octave":0}}]))

    def testFindByModularity(self):
        self.data.addPiece("file.xml", {"instruments":[{"name":"clarinet"}], "key":{"clarinet":[{"mode":"major","fifths":1}]}})
        self.data.addPiece("file2.xml", {"instruments":[{"name":"trumpet"}], "key":{"trumpet":[{"mode":"major","fifths":0}]}})
        self.data.addPiece("file3.xnl", {"instruments":[{"name":"flute"}], "key":{"flute":[{"mode":"minor","fifths":0}]}})
        self.assertEqual(["file.xml","file2.xml"], self.data.getPiecesByModularity("major"))



    def testFindPieceByTempoWhereTempoIsTwoBeats(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"quarter","beat_2":"half"}]})
        self.assertEqual(["file.xml"], self.data.getPieceByTempo(["crotchet=minim"]))

    def testFindPieceByTempoLessThanAQuaver(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"16th","minute":60}]})
        self.assertEqual(["file.xml"], self.data.getPieceByTempo(["semiquaver=60"]))

    def testFindPieceByDottedTempo(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"16th.","minute":60}]})
        self.assertEqual(["file.xml"], self.data.getPieceByTempo(["semiquaver.=60"]))

    def testFindPieceByTempoInAmerican(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"quarter","minute":60}]})
        self.assertEqual(["file.xml"], self.data.getPieceByTempo(["quarter=60"]))

    def testFindPieceByTempoWhereTempoIsTwoBeatsInAmerican(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"quarter","beat_2":"half"}]})
        self.assertEqual(["file.xml"], self.data.getPieceByTempo(["quarter=half"]))

    def testFindAllInfoForAPiece(self):
        self.data.addPiece("file.xml",{"tempo":[{"beat":"quarter","beat_2":"half"}]})
        self.assertEqual([{"title":"","composer":-1,"lyricist":-1,"tempos":["quarter=half"], "filename":"file.xml"}], self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasKeys(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}], "key":{"clarinet":[{"mode":"major","fifths":2}]}})
        self.assertEqual([{"title":"","composer":-1,"lyricist":-1,"instruments":[{"name":"clarinet"}], "keys":{"clarinet":["D major"]}, "filename":"file.xml"}], self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasClefs(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}], "clef":{"clarinet":[{"sign":"G","line":2}]}})
        self.assertEqual([{"title":"","composer":-1,"lyricist":-1,"instruments":[{"name":"clarinet"}], "clefs":{"clarinet":["treble"]}, "filename":"file.xml"}], self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasTransposedInstruments(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet","transposition":{"diatonic":-1,"chromatic":-2}}]})
        self.assertEqual([{"title":"","composer":-1,"lyricist":-1,"instruments":[{"name":"clarinet", "transposition":{"diatonic":-1,"chromatic":-2}}], "filename":"file.xml"}], self.data.getAllPieceInfo(["file.xml"]))

    def testArchivePiece(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet","transposition":{"diatonic":-1,"chromatic":-2}}]})
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 1)
        self.data.archivePieces(["file.xml"])
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 0)
        self.assertEqual(len(self.data.getArchivedPieces()), 1)

    def testRemovePiece(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet","transposition":{"diatonic":-1,"chromatic":-2}}]})
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 1)
        self.data.removePieces(["file.xml"])
        self.assertEqual(len(self.data.getAllPieceInfo(["file.xml"])), 0)
        self.assertEqual(len(self.data.getArchivedPieces()), 0)