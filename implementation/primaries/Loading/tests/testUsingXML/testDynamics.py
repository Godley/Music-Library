from implementation.primaries.Loading.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Loading.classes import Directions
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
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

class testDynamics(xmlSet):
    # TODO: handle multiple sound dynamic values in 1 bar
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testMeasure1Direction1(self):
        measure = piece.Parts[self.p_id].measures[1]
        self.assertIsInstance(measure.items[0], Directions.Dynamic)

    def testMeasure1Direction1Val(self):
        measure = piece.Parts[self.p_id].measures[1]
        self.assertEqual("ppp", measure.items[0].mark)

    def testMeasure1Direction3(self):
        measure = piece.Parts[self.p_id].measures[1]
        self.assertIsInstance(measure.items[2], Directions.Dynamic)

    def testMeasure1Direction3Val(self):
        measure = piece.Parts[self.p_id].measures[1]
        self.assertEqual("pp", measure.items[2].mark)

    def testMeasure1Direction5(self):
        measure = piece.Parts[self.p_id].measures[1]
        self.assertIsInstance(measure.items[4], Directions.Dynamic)

    def testMeasure1Direction5Val(self):
        measure = piece.Parts[self.p_id].measures[1]
        self.assertEqual("p", measure.items[4].mark)

    def testMeasure1Direction7(self):
        measure = piece.Parts[self.p_id].measures[1]
        self.assertIsInstance(measure.items[6], Directions.Dynamic)

    def testMeasure1Direction7Val(self):
        measure = piece.Parts[self.p_id].measures[1]
        self.assertEqual("mp", measure.items[6].mark)

    def testMeasure2Direction1(self):
        measure = piece.Parts[self.p_id].measures[2]
        self.assertIsInstance(measure.items[0], Directions.Dynamic)

    def testMeasure2Direction1Val(self):
        measure = piece.Parts[self.p_id].measures[2]
        self.assertEqual("mf", measure.items[0].mark)

    def testMeasure2Direction4(self):
        measure = piece.Parts[self.p_id].measures[2]
        self.assertIsInstance(measure.items[3], Directions.Dynamic)

    def testMeasure2Direction4Val(self):
        measure = piece.Parts[self.p_id].measures[2]
        self.assertEqual("f", measure.items[3].mark)

    def testMeasure3Direction1(self):
        measure = piece.Parts[self.p_id].measures[3]
        self.assertIsInstance(measure.items[0], Directions.Dynamic)

    def testMeasure3Direction1Val(self):
        measure = piece.Parts[self.p_id].measures[3]
        self.assertEqual("ff", measure.items[0].mark)

    def testMeasure3Direction5(self):
        measure = piece.Parts[self.p_id].measures[3]
        self.assertIsInstance(measure.items[4], Directions.Dynamic)

    def testMeasure3Direction5Val(self):
        measure = piece.Parts[self.p_id].measures[3]
        self.assertEqual("fff", measure.items[4].mark)
