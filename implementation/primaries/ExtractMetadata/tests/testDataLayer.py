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
        self.assertEqual("file.xml", self.data.getPiece("file.xml")[0])

    def testFindPieceByInstruments(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet"]})
        self.assertEqual(["file.xml"], self.data.getPiecesByInstruments(["clarinet"]))

    def testFindPieceByMultipleInstruments(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet", "flute"]})
        self.data.addPiece("file2.xml",{"instruments":["flute"]})
        self.assertEqual(["file.xml"], self.data.getPiecesByInstruments(["clarinet", "flute"]))

    def testFindPieceByInstrumentWhereTwoItemsExist(self):
        self.data.addPiece("file.xml",{"instruments":["flute"]})
        self.data.addPiece("file2.xml",{"instruments":["flute"]})
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
        self.data.addPiece("file.xml",{"instruments":["clarinet"],"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.data.addPiece("file2.xml",{"key":{"flute":[{"fifths":2,"mode":"major"}]}})
        self.assertEqual("file.xml", self.data.getPieceByInstrumentInKey({"clarinet":"D major"})[0])

    def testFindPieceByInstrumentInKeyWithTwoEntries(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet"],"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.data.addPiece("file2.xml",{"instruments":["clarinet"],"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.assertEqual(["file.xml","file2.xml"], self.data.getPieceByInstrumentInKey({"clarinet":"D major"}))

    def testFindPieceByInstrumentInKeyWithTwoEntriesWhichHaveDifferentKeys(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet"],"key":{"clarinet":[{"fifths":2,"mode":"major"}]}})
        self.data.addPiece("file2.xml",{"instruments":["clarinet"],"key":{"clarinet":[{"fifths":1,"mode":"major"}]}})
        self.assertEqual(["file.xml"], self.data.getPieceByInstrumentInKey({"clarinet":"D major"}))

    def testFindPieceByClef(self):
        self.data.addPiece("file", {"instruments":["clarinet"],"clef":{"clarinet":[{"sign":"G","line":2}]}})
        self.assertEqual(["file"], self.data.getPieceByClefs(["treble"]))

    def testFindPieceByInstrumentInClef(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet"],"clef":{"clarinet":[{"line":2,"sign":"G"}]}})
        self.data.addPiece("file2.xml",{"clef":{"flute":[{"line":2,"sign":"G"}]}})
        self.assertEqual("file.xml", self.data.getPieceByInstrumentInClef({"clarinet":"treble"})[0])

    def testFindPieceByInstrumentInClefWithTwoEntries(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet"],"clef":{"clarinet":[{"line":2,"sign":"G"}]}})
        self.data.addPiece("file2.xml",{"instruments":["clarinet"],"clef":{"clarinet":[{"line":2,"sign":"G"}]}})
        self.assertEqual(["file.xml","file2.xml"], self.data.getPieceByInstrumentInClef({"clarinet":"treble"}))

    def testFindPieceByInstrumentInClefWithTwoEntriesWhichHaveDifferentKeys(self):
        self.data.addPiece("file.xml",{"instruments":["clarinet"],"clef":{"clarinet":[{"line":2,"sign":"G"}]}})
        self.data.addPiece("file2.xml",{"instruments":["clarinet"],"clef":{"clarinet":[{"line":1,"sign":"G"}]}})
        self.assertEqual(["file.xml"], self.data.getPieceByInstrumentInClef({"clarinet":"treble"}))

    def testFindPieceByMeter(self):
        pass

    def testFindPieceByTempo(self):
        pass

