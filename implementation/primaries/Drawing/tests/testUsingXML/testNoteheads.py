from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Note
import os

partname = "noteheads.xml"
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

class testNote(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]
        if hasattr(self, "note_id"):
            self.note = self.measure.items[1][self.note_id]

    def testInstance(self):
        if hasattr(self, "note"):
            self.assertIsInstance(self.note, Note.Note)

    def testHasHead(self):
        if hasattr(self, "note"):
            self.assertTrue(hasattr(self.note, "notehead"))

    def testHead(self):
        if hasattr(self, "note"):
            self.assertIsInstance(self.note.notehead, Note.Notehead)

    def testHeadVal(self):
        if hasattr(self, "note"):
            self.assertEqual(self.nhead, self.note.notehead.type)

    def testFilled(self):
        if hasattr(self, "note") and hasattr(self, "filled"):
            self.assertEqual(self.filled, self.note.notehead.filled)

class testMeasure1Note1(testNote):
    def setUp(self):
        self.note_id = 0
        self.measure_id = 1
        self.nhead = "diamond"
        testNote.setUp(self)

class testMeasure1Note2(testNote):
    def setUp(self):
        self.note_id = 1
        self.measure_id = 1
        self.nhead = "x"
        testNote.setUp(self)

class testMeasure1Note3(testNote):
    def setUp(self):
        self.note_id = 2
        self.measure_id = 1
        self.nhead = "triangle"
        testNote.setUp(self)

class testMeasure1Note4(testNote):
    def setUp(self):
        self.note_id = 3
        self.measure_id = 1
        self.nhead = "mi"
        testNote.setUp(self)

class testMeasure2Note1(testNote):
    def setUp(self):
        self.note_id = 0
        self.measure_id = 2
        self.nhead = "slash"
        testNote.setUp(self)

class testMeasure2Note2(testNote):
    def setUp(self):
        self.note_id = 1
        self.measure_id = 2
        self.nhead = "circle-x"
        testNote.setUp(self)

class testMeasure2Note3(testNote):
    def setUp(self):
        self.note_id = 2
        self.measure_id = 2
        self.nhead = "do"
        testNote.setUp(self)

class testMeasure2Note4(testNote):
    def setUp(self):
        self.note_id = 3
        self.measure_id = 2
        self.nhead = "re"
        testNote.setUp(self)

class testMeasure3Note1(testNote):
    def setUp(self):
        self.note_id = 0
        self.measure_id = 3
        self.nhead = "fa"
        testNote.setUp(self)

class testMeasure3Note2(testNote):
    def setUp(self):
        self.note_id = 1
        self.measure_id = 3
        self.nhead = "la"
        testNote.setUp(self)

class testMeasure3Note3(testNote):
    def setUp(self):
        self.note_id = 2
        self.measure_id = 3
        self.nhead = "ti"
        testNote.setUp(self)