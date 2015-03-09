import unittest
import sqlite3
from implementation.primaries.ExtractMetadata.classes.DataLayer import MusicData

class testDataLayer(unittest.TestCase):
    def setUp(self):
        self.data = MusicData("example.db")

    def testAddPiece(self):
        self.data.addPiece("file.xml",{})
        conn = sqlite3.connect('example.db')
        c = conn.cursor()
        t = ('file.xml',)
        c.execute('SELECT * FROM pieces WHERE filename=?', t)
        self.assertEqual(len(c.fetchall()), 1)

    def testFindPieceByFname(self):
        pass

    def testFindPieceByInstruments(self):
        pass

    def testFindPieceByComposer(self):
        pass

    def testFindPieceByTitle(self):
        pass

    def testFindPieceByKey(self):
        pass

    def testFindPieceByClef(self):
        pass

    def testFindPieceByMeter(self):
        pass

    def testFindPieceByTempo(self):
        pass

