from implementation.primaries.Loading.tests import testclass
from implementation.primaries.Loading.classes import MxmlParser, Part, Measure, Directions


class testRepeatSymbols(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
        self.handler = MxmlParser.HandleRepeatMarking
        self.piece.Parts["P1"] = Part.Part()
        self.piece.Parts["P1"].measures[1] = Measure.Measure()
        MxmlParser.part_id = "P1"
        MxmlParser.measure_id = 1
        self.measure = self.piece.Parts["P1"].measures[1]
        self.tags.append("direction")
        self.attrs["direction"] = {"placement": "above"}

    def testSegno(self):
        self.tags.append("direction-type")
        self.tags.append("segno")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(self.measure.items[-1], Directions.RepeatSign)

    def testRType(self):
        self.tags.append("direction-type")
        self.tags.append("segno")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("segno", self.measure.items[-1].type)

    def testCoda(self):
        self.tags.append("direction-type")
        self.tags.append("coda")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(self.measure.items[-1], Directions.RepeatSign)

    def testCType(self):
        self.tags.append("direction-type")
        self.tags.append("coda")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("coda", self.measure.items[-1].type)