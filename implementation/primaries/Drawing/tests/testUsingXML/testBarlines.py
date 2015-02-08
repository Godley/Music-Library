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
        self.p_name = "Flute"

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
        self.assertEqual("dotted", item.barlines["right"].style)

    def testMeasure4Barline(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure4BarlineInstance(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertIsInstance(item.barlines["left"], Measure.Barline)
        self.assertIsInstance(item.barlines["right"], Measure.Barline)

    def testMeasure4BarlineLeft(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertTrue("left" in item.barlines)

    def testMeasure4BarlineRight(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertTrue("right" in item.barlines)

    def testMeasure4BarlineLeftStyle(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertEqual("heavy-light", item.barlines["left"].style)

    def testMeasure4BarlineRightStyle(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertEqual("light-heavy", item.barlines["right"].style)

    def testMeasure4BarlineLeftRepeat(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertTrue(hasattr(item.barlines["left"], "repeat"))

    def testMeasure4BarlineLeftRepeatVal(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertEqual("forward", item.barlines["left"].repeat)

    def testMeasure4BarlineRightRepeat(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertTrue(hasattr(item.barlines["right"], "repeat"))

    def testMeasure4BarlineRightRepeatVal(self):
        item = piece.Parts[self.p_id].measures[1][4]
        self.assertEqual("backward", item.barlines["right"].repeat)

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

    def testMeasure6BarlineRight(self):
        item = piece.Parts[self.p_id].measures[1][6]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure6BarlineRight(self):
        item = piece.Parts[self.p_id].measures[1][6]
        self.assertTrue("right" in item.barlines)

    def testMeasure6BarlineRightInstance(self):
        item = piece.Parts[self.p_id].measures[1][6]
        self.assertIsInstance(item.barlines["right"], Measure.Barline)

    def testMeasure6BarlineStyle(self):
        item = piece.Parts[self.p_id].measures[1][6]
        self.assertEqual("light-heavy", item.barlines["right"].style)

    def testMeasure7BarlineLeft(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure7BarlineLeft(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertTrue("left" in item.barlines)

    def testMeasure7BarlineLeftInstance(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertIsInstance(item.barlines["left"], Measure.Barline)

    def testMeasure7BarlineStyle(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertEqual("heavy-light", item.barlines["left"].style)

    def testMeasure7BarlineLeftRepeat(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertEqual("forward", item.barlines["left"].repeat)

    def testMeasure7BarlineCreated(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure7BarlineRight(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertTrue("right" in item.barlines)

    def testMeasure7BarlineRightInstance(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertIsInstance(item.barlines["right"], Measure.Barline)

    def testMeasure7BarlineRightStyle(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertEqual("light-heavy", item.barlines["right"].style)

    def testMeasure7BarlineRightRepeat(self):
        item = piece.Parts[self.p_id].measures[1][7]
        self.assertEqual("backward", item.barlines["right"].repeat)

    def testMeasure8BarlineLeft(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure8BarlineLeftVal(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertTrue("left" in item.barlines)

    def testMeasure8BarlineLeftInstance(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertIsInstance(item.barlines["left"], Measure.Barline)

    def testMeasure8BarlineStyle(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertEqual("heavy-light", item.barlines["left"].style)

    def testMeasure8BarlineLeftRepeat(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertEqual("forward", item.barlines["left"].repeat)

    def testMeasure8BarlineCreated(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure8BarlineRight(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertTrue("right" in item.barlines)

    def testMeasure8BarlineRightInstance(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertIsInstance(item.barlines["right"], Measure.Barline)

    def testMeasure8BarlineRightStyle(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertEqual("light-heavy", item.barlines["right"].style)

    def testMeasure8BarlineRightRepeat(self):
        item = piece.Parts[self.p_id].measures[1][8]
        self.assertEqual("backward", item.barlines["right"].repeat)

    def testMeasure9Barline(self):
        item = piece.Parts[self.p_id].measures[1][9]
        self.assertTrue(hasattr(item, "barlines"))

    def testMeasure9BarlineRight(self):
        item = piece.Parts[self.p_id].measures[1][9]
        self.assertTrue("right" in item.barlines)

    def testMeasure9BarlineStyle(self):
        item = piece.Parts[self.p_id].measures[1][9]
        self.assertEqual("light-heavy", item.barlines["right"].style)