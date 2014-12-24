from implementation.primaries.Loading.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Loading.classes import Mark
import os

partname = "fingering.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testFile(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

class testFingering(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

class testNoteFingering(testFingering):
    def setUp(self):
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]
    def testMeasureNote(self):
        if hasattr(self, "note_id"):
            self.assertTrue(hasattr(self.measure.items[self.note_id], "techniques"))

    def testMeasureNoteInstance(self):
        if hasattr(self, "note_id"):
            self.assertIsInstance(self.measure.items[self.note_id].techniques[0], Mark.Technique)

    def testMeasureNoteType(self):
        if hasattr(self, "note_id") and hasattr(self, "type"):
            self.assertEqual(self.type, self.measure.items[self.note_id].techniques[0].type)

    def testMeasureNoteSymbol(self):
        if hasattr(self, "note_id") and hasattr(self, "symbol"):
            self.assertEqual(self.symbol, self.measure.items[self.note_id].techniques[0].symbol)


class testMeasure1Note1(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 1
        self.note_id = 0
        self.type = "fingering"
        self.symbol = "0"
        testNoteFingering.setUp(self)

class testMeasure1Note2(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 1
        self.note_id = 1
        self.type = "fingering"
        self.symbol = "1"
        testNoteFingering.setUp(self)

class testMeasure1Note3(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 1
        self.note_id = 2
        self.type = "fingering"
        self.symbol = "2"
        testNoteFingering.setUp(self)

class testMeasure1Note4(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 1
        self.note_id = 3
        self.type = "fingering"
        self.symbol = "4"
        testNoteFingering.setUp(self)

class testMeasure2Note1(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 2
        self.note_id = 0
        self.type = "fingering"
        self.symbol = "5"
        testNoteFingering.setUp(self)

class testMeasure2Note2(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 2
        self.note_id = 1
        self.type = "pluck"
        self.symbol = "p"
        testNoteFingering.setUp(self)

class testMeasure2Note3(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 2
        self.note_id = 2
        self.type = "pluck"
        self.symbol = "i"
        testNoteFingering.setUp(self)

class testMeasure2Note4(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 2
        self.note_id = 3
        self.type = "pluck"
        self.symbol = "m"
        testNoteFingering.setUp(self)

class testMeasure3Note1(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 3
        self.note_id = 0
        self.type = "pluck"
        self.symbol = "a"
        testNoteFingering.setUp(self)

class testMeasure3Note2(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 3
        self.note_id = 1
        self.type = "pluck"
        self.symbol = "c"
        testNoteFingering.setUp(self)

class testMeasure3Note3(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 3
        self.note_id = 2
        self.type = "string"
        self.symbol = "0"
        testNoteFingering.setUp(self)

class testMeasure3Note4(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 3
        self.note_id = 3
        self.type = "string"
        self.symbol = "1"
        testNoteFingering.setUp(self)


class testMeasure4Note1(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 4
        self.note_id = 0
        self.type = "string"
        self.symbol = "2"
        testNoteFingering.setUp(self)

class testMeasure4Note2(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 4
        self.note_id = 1
        self.type = "string"
        self.symbol = "3"
        testNoteFingering.setUp(self)

class testMeasure4Note3(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 4
        self.note_id = 2
        self.type = "string"
        self.symbol = "4"
        testNoteFingering.setUp(self)

class testMeasure4Note4(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 4
        self.note_id = 3
        self.type = "string"
        self.symbol = "5"
        testNoteFingering.setUp(self)

class testMeasure5Note1(testNoteFingering):
    def setUp(self):
        self.p_id = "P1"
        self.measure_id = 5
        self.note_id = 0
        self.type = "string"
        self.symbol = "6"
        testNoteFingering.setUp(self)







