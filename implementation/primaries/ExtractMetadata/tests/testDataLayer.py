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

    def testFindPieceByFname(self):
        self.data.addPiece("file.xml",{})
        t = ('file.xml',)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT * FROM pieces WHERE filename=?', t)
        self.assertEqual(c.fetchall(), self.data.getPiece("file.xml"))

    def testFindPieceByInstruments(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet"]})
        t = ('clarinet',)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT ROWID FROM instruments WHERE name=?', t)
        result = c.fetchall()
        c.execute('SELECT piece_id FROM instruments_piece_join WHERE instrument_id=?', result[0])
        result_2 = c.fetchall()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', result_2[0])
        self.assertEqual(c.fetchone()[0], self.data.getPiecesByInstrument("clarinet")[0])

    def testFindPieceByMultipleInstruments(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet", "flute"]})
        t = ('clarinet','flute',)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT ROWID FROM instruments WHERE name=? OR name=?', t)
        result = c.fetchall()
        c.execute('SELECT piece_id FROM instruments_piece_join WHERE instrument_id=?', result[0])
        result_2 = c.fetchall()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', result_2[0])
        self.assertEqual(c.fetchone()[0], self.data.getPiecesByMultipleInstruments(["clarinet", "flute"])[0])

    def testFindPieceByComposer(self):
        self.data.addPiece("file.xml",{"composer":"Bartok"})
        t = ('Bartok',)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT ROWID FROM composers WHERE name=?', t)
        result = c.fetchall()
        c.execute('SELECT piece_id FROM composer_piece_join WHERE composer_id=?', result[0])
        result_2 = c.fetchall()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', result_2[0])
        self.assertEqual(c.fetchone()[0], self.data.getPiecesByComposer("Bartok")[0])

    def testFindPieceByTitle(self):
        self.data.addPiece("file.xml",{"title":"Blabla"})
        t = ('Blabla',)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT * FROM pieces WHERE title=?', t)
        self.assertEqual(c.fetchall(), self.data.getPieceByTitle("Blabla"))

    def testFindPieceByKey(self):
        self.data.addPiece("file.xml",{"key":{"fifths":2,"mode":"major"}})
        t = (2,"major",)
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        c.execute('SELECT ROWID FROM keys WHERE fifths=? AND mode=?', t)
        result = c.fetchone()
        c.execute('SELECT piece_id FROM key_piece_join WHERE key_id=?', result)
        result2 = c.fetchone()
        c.execute('SELECT * FROM pieces WHERE ROWID=?', result2)
        self.assertEqual(c.fetchone()[0], self.data.getPieceByKey("D major")[0])

    def testFindPieceByClef(self):
        pass

    def testFindPieceByMeter(self):
        pass

    def testFindPieceByTempo(self):
        pass

