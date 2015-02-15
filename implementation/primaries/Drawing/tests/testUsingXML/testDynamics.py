from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Directions
import os

partname = "dynamics.xml"
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
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures[1])

class testDynamics(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testMeasure1Direction1(self):
        measure = piece.Parts[self.p_id].measures[1][1]
        self.assertIsInstance(measure.expressions[0][0], Directions.Dynamic)

    def testMeasure1Direction1Val(self):
        measure = piece.Parts[self.p_id].measures[1][1]
        self.assertEqual("ppp", measure.expressions[0][0].mark)

    def testMeasure1Direction3(self):
        measure = piece.Parts[self.p_id].measures[1][1]
        self.assertIsInstance(measure.expressions[0][1], Directions.Dynamic)

    def testMeasure1Direction3Val(self):
        measure = piece.Parts[self.p_id].measures[1][1]
        self.assertEqual("pp", measure.expressions[0][1].mark)

    def testMeasure1Direction5(self):
        measure = piece.Parts[self.p_id].measures[1][1]
        self.assertIsInstance(measure.expressions[1][0], Directions.Dynamic)

    def testMeasure1Direction5Val(self):
        measure = piece.Parts[self.p_id].measures[1][1]
        self.assertEqual("p", measure.expressions[1][0].mark)

    def testMeasure1Direction7(self):
        measure = piece.Parts[self.p_id].measures[1][1]
        self.assertIsInstance(measure.expressions[2][0], Directions.Dynamic)

    def testMeasure1Direction7Val(self):
        measure = piece.Parts[self.p_id].measures[1][1]
        self.assertEqual("mp", measure.expressions[2][0].mark)

    def testMeasure2Direction1(self):
        measure = piece.Parts[self.p_id].measures[1][2]
        self.assertIsInstance(measure.expressions[0][0], Directions.Dynamic)

    def testMeasure2Direction1Val(self):
        measure = piece.Parts[self.p_id].measures[1][2]
        self.assertEqual("mf", measure.expressions[0][0].mark)

    def testMeasure2Direction4(self):
        measure = piece.Parts[self.p_id].measures[1][2]
        self.assertIsInstance(measure.expressions[1][0], Directions.Dynamic)

    def testMeasure2Direction4Val(self):
        measure = piece.Parts[self.p_id].measures[1][2]
        self.assertEqual("f", measure.expressions[1][0].mark)

    def testMeasure3Direction1(self):
        measure = piece.Parts[self.p_id].measures[1][3]
        self.assertIsInstance(measure.expressions[0][0], Directions.Dynamic)

    def testMeasure3Direction1Val(self):
        measure = piece.Parts[self.p_id].measures[1][3]
        self.assertEqual("ff", measure.expressions[0][0].mark)

    def testMeasure3Direction5(self):
        measure = piece.Parts[self.p_id].measures[1][3]
        self.assertIsInstance(measure.expressions[2][0], Directions.Dynamic)

    def testMeasure3Direction5Val(self):
        measure = piece.Parts[self.p_id].measures[1][3]
        self.assertEqual("fff", measure.expressions[2][0].mark)
