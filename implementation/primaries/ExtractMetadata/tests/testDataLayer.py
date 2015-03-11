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

    def testAddPieceWithComposer(self):
        self.data.addPiece("file.xml",{"composer":"blabla"})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('blabla',)
        c.execute('SELECT ROWID FROM composers WHERE name=?', t)
        result = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE composer_id=?', result)
        self.assertEqual("file.xml", c.fetchone()[0])

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
        self.assertEqual([("file.xml","",-1)], c.fetchall())

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
        self.assertEqual([("file.xml","",-1)], c.fetchall())

    def testFindPieceByFname(self):
        self.data.addPiece("file.xml",{})
        self.assertEqual([(1, "file.xml","",-1)], self.data.getPiece("file.xml"))

    def testAddPieceWithInstrumentsWithTranspositions(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"Bflat clarinet","transposition":{"octave":0,"diatonic":-1,"chromatic":-2}}]})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('Bflat clarinet',)
        c.execute('SELECT ROWID, octave, diatonic, chromatic FROM instruments WHERE name=?', t)
        row = c.fetchone()
        self.assertEqual(row[1],0)
        self.assertEqual(row[2],-1)
        self.assertEqual(row[3],-2)
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

    def testFindPieceByTitle(self):
        self.data.addPiece("file.xml",{"title":"Blabla"})
        self.assertEqual("file.xml", self.data.getPieceByTitle("Blabla")[0])

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
        self.assertEqual([{"title":"","composer":-1,"tempos":["quarter=half"],"instruments":[], "clefs":{}, "keys":{}, "time_signatures":[], "filename":"file.xml"}], self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasKeys(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}], "key":{"clarinet":[{"mode":"major","fifths":2}]}})
        self.assertEqual([{"title":"","composer":-1,"tempos":[],"instruments":["clarinet"], "clefs":{}, "keys":{"clarinet":["D major"]}, "time_signatures":[], "filename":"file.xml"}], self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasClefs(self):
        self.data.addPiece("file.xml",{"instruments":[{"name":"clarinet"}], "clef":{"clarinet":[{"sign":"G","line":2}]}})
        self.assertEqual([{"title":"","composer":-1,"tempos":[],"instruments":["clarinet"], "clefs":{"clarinet":["treble"]}, "keys":{}, "time_signatures":[], "filename":"file.xml"}], self.data.getAllPieceInfo(["file.xml"]))

