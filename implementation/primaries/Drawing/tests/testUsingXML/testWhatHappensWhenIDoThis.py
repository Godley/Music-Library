from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Measure
import os

partname = "WhatHappensWhenIDoThis.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testFile(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Piccolo"

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures[1])

class testMeasure1(xmlSet):
    def setUp(self):
        self.measure_id = 1
        self.left_number = 1
        self.left_type = "start"
        self.right_number = 1
        self.right_type = "stop"
        self.right_repeat = "backward"
        self.right_style = "light-heavy"
        self.measure = piece.Parts["P1"].measures[1][self.measure_id]

    def testHasBarlines(self):
        self.assertTrue(hasattr(self.measure, "barlines"))

    def testHasLeftBarline(self):
        self.assertTrue("left" in self.measure.barlines)

    def testHasLeftEnding(self):
        self.assertTrue(hasattr(self.measure.barlines["left"], "ending"))

    def testLeftEndingInstance(self):
        barline = self.measure.barlines["left"]
        self.assertIsInstance(barline.ending, Measure.EndingMark)

    def testLeftNumber(self):
        barline = self.measure.barlines["left"]
        self.assertEqual(self.left_number, barline.ending.number)

    def testLeftType(self):
        barline = self.measure.barlines["left"]
        self.assertEqual(self.left_type, barline.ending.type)

    def testHasRightEnding(self):
        self.assertTrue(hasattr(self.measure.barlines["right"], "ending"))

    def testRightEndingInstance(self):
        barline = self.measure.barlines["right"]
        self.assertIsInstance(barline.ending, Measure.EndingMark)

    def testRightNumber(self):
        barline = self.measure.barlines["right"]
        self.assertEqual(self.right_number, barline.ending.number)

    def testRightType(self):
        barline = self.measure.barlines["right"]
        self.assertEqual(self.right_type, barline.ending.type)

    def testRightStyle(self):
        barline = self.measure.barlines["right"]
        self.assertEqual(self.right_style, barline.style)

    def testRightRepeat(self):
        barline = self.measure.barlines["right"]
        self.assertEqual(self.right_repeat, barline.repeat)

