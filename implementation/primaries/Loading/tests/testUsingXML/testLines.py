from implementation.primaries.Loading.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Loading.classes import Directions
import os

partname = "lines.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testFile(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 15
        self.p_id = "P1"
        self.p_name = "Flute"

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

class testWedge(xmlSet):
    def setUp(self):
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]
        if hasattr(self, "item_id"):
            self.item = self.measure.items[self.item_id]

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Wedge)

    def testType(self):
        if hasattr(self, "type"):
            self.assertEqual(self.type, self.item.type)

    def testPlacement(self):
        if hasattr(self, "placement"):
            self.assertEqual(self.placement, self.item.placement)

class testOctaveShift(xmlSet):
    def setUp(self):
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]
        if hasattr(self, "item_id"):
            self.item = self.measure.items[self.item_id]

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.OctaveShift)

    def testType(self):
        if hasattr(self, "type"):
            self.assertEqual(self.type, self.item.type)

    def testAmount(self):
        if hasattr(self, "amount"):
            self.assertEqual(self.amount, self.item.amount)

    def testFont(self):
        if hasattr(self, "font"):
            self.assertEqual(self.font, self.item.font)

class testPedal(xmlSet):
    def setUp(self):
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]
        if hasattr(self, "item_id"):
            self.item = self.measure.items[self.item_id]

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Pedal)

    def testType(self):
        if hasattr(self, "type"):
            self.assertEqual(self.type, self.item.type)

    def testLine(self):
        if hasattr(self, "line"):
            self.assertEqual(self.line, self.item.line)

    def testPlacement(self):
        if hasattr(self, "placement"):
            self.assertEqual(self.placement, self.item.placement)

class testBracket(xmlSet):
    def setUp(self):
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]
        if hasattr(self, "item_id"):
            self.item = self.measure.items[self.item_id]

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Bracket)

    def testType(self):
        if hasattr(self, "type"):
            self.assertEqual(self.type, self.item.type)

    def testNumber(self):
        if hasattr(self, "number"):
            self.assertEqual(self.number, self.item.number)

    def testLineEnd(self):
        if hasattr(self, "lineend"):
            self.assertEqual(self.lineend, self.item.lineEnd)

    def testLineType(self):
        if hasattr(self, "linetype"):
            self.assertEqual(self.linetype, self.item.lineType)

    def testEndLength(self):
        if hasattr(self, "endlength"):
            self.assertEqual(self.endlength, self.item.endLength)

class testMeasure1Item1(testWedge):
    def setUp(self):
        self.placement = "below"
        self.type = "crescendo"
        self.measure_id = 1
        self.item_id = 0
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure1Item3(testWedge):
    def setUp(self):
        self.placement = "below"
        self.type = "stop"
        self.measure_id = 1
        self.item_id = 2
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure2Item1(testWedge):
    def setUp(self):
        self.placement = "below"
        self.type = "diminuendo"
        self.measure_id = 2
        self.item_id = 0
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure2Item3(testWedge):
    def setUp(self):
        self.placement = "below"
        self.type = "stop"
        self.measure_id = 2
        self.item_id = 2
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure6Item1(testOctaveShift):
    def setUp(self):
        self.placement = "above"
        self.amount = 8
        self.type = "down"
        self.measure_id = 6
        self.item_id = 0
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure6Item3(testOctaveShift):
    def setUp(self):
        self.placement = "above"
        self.amount = 8
        self.type = "stop"
        self.measure_id = 6
        self.item_id = 2
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure7Item1(testOctaveShift):
    def setUp(self):
        self.placement = "above"
        self.amount = 15
        self.type = "down"
        self.measure_id = 7
        self.item_id = 0
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure7Item3(testOctaveShift):
    def setUp(self):
        self.placement = "above"
        self.amount = 15
        self.type = "stop"
        self.measure_id = 7
        self.item_id = 2
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure8Item1(testOctaveShift):
    def setUp(self):
        self.placement = "below"
        self.amount = 8
        self.type = "up"
        self.measure_id = 8
        self.item_id = 0
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure8Item3(testOctaveShift):
    def setUp(self):
        self.placement = "below"
        self.amount = 8
        self.type = "stop"
        self.measure_id = 8
        self.item_id = 2
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure9Item1(testOctaveShift):
    def setUp(self):
        self.placement = "below"
        self.amount = 15
        self.type = "up"
        self.measure_id = 9
        self.item_id = 0
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure9Item3(testOctaveShift):
    def setUp(self):
        self.placement = "below"
        self.amount = 15
        self.type = "stop"
        self.measure_id = 9
        self.item_id = 2
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure12Item1(testPedal):
    def setUp(self):
        self.type = "start"
        self.line = True
        self.measure_id = 12
        self.item_id = 0
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure12Item3(testPedal):
    def setUp(self):
        self.type = "stop"
        self.line = True
        self.measure_id = 12
        self.item_id = 2
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure13Item1(testPedal):
    def setUp(self):
        self.type = "start"
        self.line = True
        self.measure_id = 13
        self.item_id = 0
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure13Item3(testPedal):
    def setUp(self):
        self.type = "stop"
        self.line = True
        self.measure_id = 13
        self.item_id = 2
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure14Item2(testBracket):
    def setUp(self):
        self.type = "start"
        self.number = 1
        self.lineend = "none"
        self.linetype = "solid"
        self.measure_id = 14
        self.item_id = 1
        self.p_id = "P1"
        testWedge.setUp(self)

class testMeasure14Item4(testBracket):
    def setUp(self):
        self.type = "stop"
        self.number = 1
        self.lineend = "down"
        self.endlength = 15
        self.measure_id = 14
        self.item_id = 3
        self.p_id = "P1"
        testWedge.setUp(self)