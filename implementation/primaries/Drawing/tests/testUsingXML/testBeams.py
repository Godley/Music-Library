from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Note
import os

partname = "beams.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testArpeg(xmlSet):
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

    def testNote1(self):
        item = piece.Parts[self.p_id].measures[1].notes[0]
        self.assertFalse(hasattr(item, "beams"))

    def testNote2(self):
        item = piece.Parts[self.p_id].measures[1].notes[1]
        self.assertTrue(hasattr(item, "beams"))

    def testNote2ID(self):
        item = piece.Parts[self.p_id].measures[1].notes[1]
        self.assertTrue(1 in item.beams)

    def testNote2Type(self):
        item = piece.Parts[self.p_id].measures[1].notes[1]
        self.assertEqual("begin", item.beams[1].type)

    def testNote3(self):
        item = piece.Parts[self.p_id].measures[1].notes[2]
        self.assertTrue(hasattr(item, "beams"))

    def testNote3ID(self):
        item = piece.Parts[self.p_id].measures[1].notes[2]
        self.assertTrue(1 in item.beams)

    def testNote3Type(self):
        item = piece.Parts[self.p_id].measures[1].notes[2]
        self.assertEqual("continue", item.beams[1].type)

    def testNote4(self):
        item = piece.Parts[self.p_id].measures[1].notes[3]
        self.assertTrue(hasattr(item, "beams"))

    def testNote4ID(self):
        item = piece.Parts[self.p_id].measures[1].notes[3]
        self.assertTrue(1 in item.beams)

    def testNote4Type(self):
        item = piece.Parts[self.p_id].measures[1].notes[3]
        self.assertEqual("end", item.beams[1].type)

    def testNote5(self):
        item = piece.Parts[self.p_id].measures[1].notes[4]
        self.assertFalse(hasattr(item, "beams"))

    def testNote6(self):
        item = piece.Parts[self.p_id].measures[1].notes[5]
        self.assertTrue(hasattr(item, "beams"))

    def testNote6ID(self):
        item = piece.Parts[self.p_id].measures[1].notes[5]
        self.assertTrue(1 in item.beams)

    def testNote6Type(self):
        item = piece.Parts[self.p_id].measures[1].notes[5]
        self.assertEqual("begin", item.beams[1].type)

    def testNote7(self):
        item = piece.Parts[self.p_id].measures[1].notes[6]
        self.assertTrue(hasattr(item, "beams"))

    def testNote7ID(self):
        item = piece.Parts[self.p_id].measures[1].notes[6]
        self.assertTrue(1 in item.beams)

    def testNote7Type(self):
        item = piece.Parts[self.p_id].measures[1].notes[6]
        self.assertEqual("continue", item.beams[1].type)

    def testNote8(self):
        item = piece.Parts[self.p_id].measures[1].notes[7]
        self.assertTrue(hasattr(item, "beams"))

    def testNote8ID(self):
        item = piece.Parts[self.p_id].measures[1].notes[7]
        self.assertTrue(1 in item.beams)

    def testNote8Type(self):
        item = piece.Parts[self.p_id].measures[1].notes[7]
        self.assertEqual("end", item.beams[1].type)


