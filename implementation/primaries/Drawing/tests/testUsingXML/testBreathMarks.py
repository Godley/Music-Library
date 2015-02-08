from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Mark
import os

partname = "breathMarks.xml"
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

class testBreath(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts["P1"].measures[1][self.measure_id]
        if hasattr(self, "item_id"):
            self.item = self.measure.notes[self.item_id]
        if hasattr(self, "n_id"):
            self.notation = self.item.postnotation[self.n_id]



    def testInstance(self):
        if hasattr(self, "notation"):
            self.assertIsInstance(self.notation, self.instance)

class testMeasure1Note1(testBreath):
    def setUp(self):
        self.measure_id = 1
        self.item_id = 0
        self.n_id = 0
        self.instance = Mark.BreathMark
        testBreath.setUp(self)

class testMeasure1Note2(testBreath):
    def setUp(self):
        self.measure_id = 1
        self.item_id = 1
        self.n_id = 0
        self.instance = Mark.BreathMark
        testBreath.setUp(self)

class testMeasure1Note3(testBreath):
    def setUp(self):
        self.measure_id = 1
        self.item_id = 3
        self.n_id = 0
        self.instance = Mark.Caesura
        testBreath.setUp(self)

class testMeasure2Note3(testBreath):
    def setUp(self):
        self.measure_id = 1
        self.item_id = 3
        self.n_id = 0
        self.instance = Mark.Caesura
        testBreath.setUp(self)