from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Measure
import os

partname = "barlines.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testBarlines(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Piano"

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures[1])

    def testMeasure2Barline(self):
        item = piece.Parts[self.p_id].measures[1][2]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure2BarlineLocation(self):
        item = piece.Parts[self.p_id].measures[1][2]
        self.assertTrue("right" in item.barlines)

    def testMeasure2BarlineInstance(self):
        item = piece.Parts[self.p_id].measures[1][2]
        self.assertIsInstance(item.barlines["right"], Measure.Barline)

    def testMeasure2BarlineStyle(self):
        item = piece.Parts[self.p_id].measures[1][2]
        self.assertEqual("dashed", item.barlines["right"].style)

    def testMeasure4Barline(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure4BarlineInstance(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertIsInstance(item.barlines["right"], Measure.Barline)

    def testMeasure4BarlineRight(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertTrue("right" in item.barlines)

    def testMeasure4BarlineRightStyle(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertEqual("light-heavy", item.barlines["right"].style)

    def testMeasure5Barline(self):
        item = piece.Parts[self.p_id].measures[1][5]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure5BarlineRight(self):
        item = piece.Parts[self.p_id].measures[1][5]
        self.assertTrue("right" in item.barlines)

    def testMeasure5BarlineRightInstance(self):
        item = piece.Parts[self.p_id].measures[1][5]
        self.assertIsInstance(item.barlines["right"], Measure.Barline)

    def testMeasure5BarlineStyle(self):
        item = piece.Parts[self.p_id].measures[1][5]
        self.assertEqual("light-light", item.barlines["right"].style)