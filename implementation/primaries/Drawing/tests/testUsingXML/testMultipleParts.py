from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Measure, Part
import os

partname = "multiple_parts.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testPart(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)

    def testPartExists(self):
        if hasattr(self, "p_id"):
            self.assertTrue(self.p_id in piece.Parts)
    def testPartInstance(self):
        if hasattr(self, "p_id"):
            self.assertIsInstance(piece.Parts[self.p_id], Part.Part)

    def testPartName(self):
        if hasattr(self, "p_id"):
            self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        if hasattr(self, "p_id"):
            self.assertTrue(self.m_num in piece.Parts[self.p_id].measures[1])

class testPart1(testPart):
    def setUp(self):
        self.p_id = "P1"
        self.p_name = "Piccolo"
        self.m_num = 32
        testPart.setUp(self)

class testPart2(testPart):
    def setUp(self):
        self.p_id = "P2"
        self.p_name = "Alto Flute"
        self.m_num = 32
        testPart.setUp(self)


class testPart3(testPart):
    def setUp(self):
        self.p_id = "P3"
        self.p_name = "Soprano Recorder"
        self.m_num = 32
        testPart.setUp(self)

class testPart4(testPart):
    def setUp(self):
        self.p_id = "P4"
        self.p_name = "Garklein Recorder"
        self.m_num = 32
        testPart.setUp(self)

class testPart5(testPart):
    def setUp(self):
        self.p_id = "P5"
        self.p_name = "Greatbass Recorder"
        self.m_num = 32
        testPart.setUp(self)