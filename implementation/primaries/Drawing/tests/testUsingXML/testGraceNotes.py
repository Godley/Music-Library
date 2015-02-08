from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Note
import os

partname = "GraceNotes.xml"
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

class GraceNotes(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

    def testGrace(self):
        if hasattr(self, "nid") and hasattr(self, "grace"):
            note = self.measure.notes[self.nid]
            self.assertEqual(self.grace, hasattr(note, "grace"))

    def testGraceVal(self):
        if hasattr(self, "nid") and hasattr(self, "grace"):
            if self.grace:
                note = self.measure.notes[self.nid]
                self.assertIsInstance(note.grace, Note.GraceNote)

    def testGraceSlash(self):
        if hasattr(self, "nid") and hasattr(self, "grace") and hasattr(self, "graceSlash"):
            if self.grace:
                note = self.measure.notes[self.nid]
                self.assertEqual(self.graceSlash, note.grace.slash)

class testNote1Measure1(GraceNotes):
    def setUp(self):
        self.measure_id= 1
        self.nid = 0
        self.grace = True
        self.graceSlash = True
        GraceNotes.setUp(self)

class testNote2Measure1(GraceNotes):
    def setUp(self):
        self.measure_id= 1
        self.nid = 1
        self.grace = True
        self.graceSlash = False
        GraceNotes.setUp(self)

class testNote3Measure1(GraceNotes):
    def setUp(self):
        self.measure_id= 1
        self.nid = 2
        self.grace = True
        self.graceSlash = False
        GraceNotes.setUp(self)

class testNote4Measure1(GraceNotes):
    def setUp(self):
        self.measure_id= 1
        self.nid = 3
        self.grace = False
        self.graceSlash = False
        GraceNotes.setUp(self)

class testNote5Measure1(GraceNotes):
    def setUp(self):
        self.measure_id= 1
        self.nid = 4
        self.grace = True
        self.graceSlash = False
        GraceNotes.setUp(self)

class testNote6Measure1(GraceNotes):
    def setUp(self):
        self.measure_id= 1
        self.nid = 5
        self.grace = False
        self.graceSlash = False
        GraceNotes.setUp(self)

class testNote7Measure1(GraceNotes):
    def setUp(self):
        self.measure_id= 1
        self.nid = 6
        self.grace = True
        self.graceSlash = False
        GraceNotes.setUp(self)

class testNote8Measure1(GraceNotes):
    def setUp(self):
        self.measure_id= 1
        self.nid = 7
        self.grace = False
        self.graceSlash = False
        GraceNotes.setUp(self)

