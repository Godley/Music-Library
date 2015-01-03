from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Note
import os

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
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

    def testNotes(self):
        for measure in piece.Parts[self.p_id].measures.keys():
            if measure in self.note_num:
                self.assertEqual(self.note_num[measure], len(piece.Parts[self.p_id].measures[measure].items[1]))


    def testNote1Measure1(self):
        note = piece.Parts[self.p_id].measures[1].items[1][0]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[0], Note.Arpeggiate)

    def testNote2Measure1(self):
        note = piece.Parts[self.p_id].measures[1].items[1][1]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[0], Note.Arpeggiate)

    def testNote2Measure1DirectionValue(self):
        notation = piece.Parts[self.p_id].measures[1].items[1][1].notations[0]
        self.assertEqual("up", notation.direction)

    def testNote3Measure1(self):
        note = piece.Parts[self.p_id].measures[1].items[1][2]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[0], Note.Arpeggiate)

    def testNote3Measure1DirectionValue(self):
        notation = piece.Parts[self.p_id].measures[1].items[1][2].notations[0]
        self.assertEqual("down", notation.direction)

    def testNote4Measure1FirstNotation(self):
        note = piece.Parts[self.p_id].measures[1].items[1][3]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[0], Note.NonArpeggiate)

    def testNote4Measure1SecondNotation(self):
        note = piece.Parts[self.p_id].measures[1].items[1][3]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[1], Note.NonArpeggiate)

    def testNote4Measure1Notation1Type(self):
        notation = piece.Parts[self.p_id].measures[1].items[1][3].notations[0]
        self.assertEqual("bottom", notation.type)

    def testNote4Measure1Notation2Type(self):
        notation = piece.Parts[self.p_id].measures[1].items[1][3].notations[1]
        self.assertEqual("top", notation.type)

    def testNote1Measure2(self):
        note = piece.Parts[self.p_id].measures[2].items[1][0]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[0], Note.Slide)

    def testNote1Measure2Type(self):
        item = piece.Parts[self.p_id].measures[2].items[1][0].notations[0]
        self.assertEqual("start", item.type)

    def testNote1Measure2Number(self):
        item = piece.Parts[self.p_id].measures[2].items[1][0].notations[0]
        self.assertEqual(1, item.number)

    def testNote1Measure2LineType(self):
        item = piece.Parts[self.p_id].measures[2].items[1][0].notations[0]
        self.assertEqual("solid", item.lineType)

    def testNote2Measure2(self):
        note = piece.Parts[self.p_id].measures[2].items[1][1]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[0], Note.Slide)

    def testNote2Measure2Type(self):
        item = piece.Parts[self.p_id].measures[2].items[1][1].notations[0]
        self.assertEqual("stop", item.type)

    def testNote2Measure2Number(self):
        item = piece.Parts[self.p_id].measures[2].items[1][1].notations[0]
        self.assertEqual(1, item.number)

    def testNote2Measure2LineType(self):
        item = piece.Parts[self.p_id].measures[2].items[1][1].notations[0]
        self.assertEqual("solid", item.lineType)

    def testNote3Measure2(self):
        note = piece.Parts[self.p_id].measures[2].items[1][2]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[0], Note.Glissando)

    def testNote3Measure2Type(self):
        item = piece.Parts[self.p_id].measures[2].items[1][2].notations[0]
        self.assertEqual("start", item.type)

    def testNote3Measure2Number(self):
        item = piece.Parts[self.p_id].measures[2].items[1][2].notations[0]
        self.assertEqual(1, item.number)

    def testNote3Measure2LineType(self):
        item = piece.Parts[self.p_id].measures[2].items[1][2].notations[0]
        self.assertEqual("wavy", item.lineType)

    def testNote4Measure2(self):
        note = piece.Parts[self.p_id].measures[2].items[1][3]
        self.assertTrue(hasattr(note, "notations"))
        self.assertIsInstance(note.notations[0], Note.Glissando)

    def testNote4Measure2Type(self):
        item = piece.Parts[self.p_id].measures[2].items[1][3].notations[0]
        self.assertEqual("stop", item.type)

    def testNote4Measure2Number(self):
        item = piece.Parts[self.p_id].measures[2].items[1][3].notations[0]
        self.assertEqual(1, item.number)

    def testNote4Measure2LineType(self):
        item = piece.Parts[self.p_id].measures[2].items[1][3].notations[0]
        self.assertEqual("wavy", item.lineType)
