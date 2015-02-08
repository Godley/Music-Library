from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Note
import os, unittest

partname = "arpeggiosAndGlissandos.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testArpeg(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Piccolo"
        self.note_num = {1: 4,2: 4,3: 1,4: 1,5: 1,6: 1,7: 1,8: 1,9: 1,10: 1,
                         11: 1,12: 1,13: 1,14: 1,15: 1,16: 1,17: 1,18: 1,19: 1,
                         20: 1,21: 1,22: 1,23: 1,24: 1,25: 1,26: 1,27: 1,28: 1,
                         29: 1,30: 1,31: 1,32: 1}

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures[1])

    def testNotes(self):
        for measure in piece.Parts[self.p_id].measures.keys():
            if measure in self.note_num:
                self.assertEqual(self.note_num[measure], len(piece.Parts[self.p_id].measures[1][measure].notes))

class testBar(unittest.TestCase):
    def testInstance(self):
        if hasattr(self, "instance_type"):
            self.assertIsInstance(self.item.wrap_notation[0], self.instance_type)

    def testEquality(self):
        if hasattr(self, "value"):
            self.assertEqual(self.item, self.value)

class Note1Measure1(testBar):
    def setUp(self):
        self.p_id = "P1"
        self.item = piece.Parts[self.p_id].measures[1][1].notes[0]
        self.instance_type = Note.Arpeggiate

class Note2Measure1(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][1].notes[1]
        self.instance_type = Note.Arpeggiate

class Note2Measure1DirectionValue(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][1].notes[1].wrap_notation[0].direction
        self.value = "up"

class Note3Measure1(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][1].notes[2]
        self.instance_type = Note.Arpeggiate

class Note3Measure1DirectionValue(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][1].notes[2].wrap_notation[0].direction
        self.value = "down"

class Note4Measure1FirstNotation(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][1].notes[3]
        self.instance_type = Note.NonArpeggiate

class Note4Measure1SecondNotation(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][1].notes[3]
        self.instance_type = Note.NonArpeggiate

class Note4Measure1Notation1Type(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][1].notes[3].wrap_notation[0].type
        self.value = "bottom"

class Note4Measure1Notation2Type(testBar):
    def setUp(self):
        self.item= piece.Parts["P1"].measures[1][1].notes[3].wrap_notation[1].type
        self.value = "top"

class Note1Measure2(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[0]
        self.instance_type = Note.Slide

class Note1Measure2Type(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[0].wrap_notation[0].type
        self.value = "start"

class Note1Measure2Number(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[0].wrap_notation[0].number
        self.value = 1

class Note1Measure2LineType(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[0].wrap_notation[0].lineType
        self.value = "solid"

class Note2Measure2(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[1]
        self.instance_type = Note.Slide

class Note2Measure2Type(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[1].wrap_notation[0].type
        self.value = "stop"

class Note2Measure2Number(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[1].wrap_notation[0].number
        self.value = 1

class Note2Measure2LineType(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[1].wrap_notation[0].lineType
        self.value = "solid"

class Note3Measure2(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[2]
        self.instance_type=Note.Glissando

class Note3Measure2Type(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[2].wrap_notation[0].type
        self.value = "start"

class Note3Measure2Number(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[2].wrap_notation[0].number
        self.value = 1

class Note3Measure2LineType(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[2].wrap_notation[0].lineType
        self.value = "wavy"

class Note4Measure2(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[3]
        self.instance_type = Note.Glissando

class Note4Measure2Type(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[3].wrap_notation[0].type
        self.value = "stop"

class Note4Measure2Number(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[3].wrap_notation[0].number
        self.value = 1

class Note4Measure2LineType(testBar):
    def setUp(self):
        self.item = piece.Parts["P1"].measures[1][2].notes[3].wrap_notation[0].lineType
        self.value = "wavy"
