from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Note
import os

partname = "tuplets.xml"
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

class testTimeMod(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts["P1"].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.notes[1][self.item_id]

    def testHasTimeMod(self):
        if hasattr(self, "item"):
            self.assertTrue(hasattr(self.item, "timeMod"))

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item.timeMod, Note.TimeModifier)

    def testActual(self):
        if hasattr(self, "item"):
            self.assertEqual(self.actual, self.item.timeMod.actual)

    def testNormal(self):
        if hasattr(self, "item"):
            self.assertEqual(self.normal, self.item.timeMod.normal)

    def testHasNotations(self):
        if hasattr(self, "item") and hasattr(self, "notation_id"):
            self.assertTrue(hasattr(self.item, "notations"))

    def testInstanceTuplet(self):
        if hasattr(self, "notation_id"):
            self.assertIsInstance(self.item.notations[self.notation_id], Note.Tuplet)

    def testType(self):
        if hasattr(self, "item") and hasattr(self, "type"):
            self.assertEqual(self.type, self.item.notations[self.notation_id].type)

    def testBracket(self):
        if hasattr(self, "item") and hasattr(self, "bracket"):
            self.assertEqual(self.bracket, self.item.notations[self.notation_id].bracket)

class testMeasure1Note1(testTimeMod):
    def setUp(self):
        self.actual = 2
        self.normal = 2
        self.type = "start"
        self.bracket = True
        self.measure_id= 1
        self.item_id = 0
        self.notation_id = 0
        testTimeMod.setUp(self)

class testMeasure1note2(testTimeMod):
    def setUp(self):
        self.actual = 2
        self.normal = 2
        self.type = "stop"
        self.measure_id= 1
        self.item_id = 1
        self.notation_id = 0
        testTimeMod.setUp(self)

class testMeasure2Note1(testTimeMod):
    def setUp(self):
        self.actual = 3
        self.normal = 2
        self.type = "start"
        self.bracket = True
        self.measure_id= 2
        self.item_id = 0
        self.notation_id = 0
        testTimeMod.setUp(self)

class testMeasure2note2(testTimeMod):
    def setUp(self):
        self.actual = 3
        self.normal = 2
        self.measure_id= 2
        self.item_id = 1
        testTimeMod.setUp(self)

class testMeasure2Note3(testTimeMod):
    def setUp(self):
        self.actual = 3
        self.normal = 2
        self.type = "stop"
        self.measure_id= 2
        self.item_id = 2
        self.notation_id = 0
        testTimeMod.setUp(self)

class testMeasure2Note4(testTimeMod):
    def setUp(self):
        self.actual = 4
        self.normal = 4
        self.type = "start"
        self.bracket = False
        self.measure_id= 2
        self.item_id = 3
        self.notation_id = 0
        testTimeMod.setUp(self)

class testMeasure2Note5(testTimeMod):
    def setUp(self):
        self.actual = 4
        self.normal = 4
        self.measure_id= 2
        self.item_id = 4
        testTimeMod.setUp(self)

class testMeasure2Note6(testTimeMod):
    def setUp(self):
        self.actual = 4
        self.normal = 4
        self.measure_id= 2
        self.item_id = 5
        testTimeMod.setUp(self)

class testMeasure2Note7(testTimeMod):
    def setUp(self):
        self.actual = 4
        self.normal = 4
        self.measure_id= 2
        self.item_id = 6
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)

class testMeasure2Note8(testTimeMod):
    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id= 2
        self.item_id = 7
        self.notation_id = 0
        self.type = "start"
        self.bracket = False
        testTimeMod.setUp(self)

class testMeasure2Note9(testTimeMod):
    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id= 2
        self.item_id = 8
        testTimeMod.setUp(self)

class testMeasure2Note10(testTimeMod):
    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id= 2
        self.item_id = 9
        testTimeMod.setUp(self)

class testMeasure2Note11(testTimeMod):
    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id= 2
        self.item_id = 10
        testTimeMod.setUp(self)

class testMeasure2Note12(testTimeMod):
    def setUp(self):
        self.actual = 5
        self.normal = 4
        self.measure_id= 2
        self.item_id = 11
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)

class testMeasure3Note1(testTimeMod):
    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id= 3
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.bracket = True
        testTimeMod.setUp(self)

class testMeasure3Note2(testTimeMod):
    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id= 3
        self.item_id = 1
        testTimeMod.setUp(self)

class testMeasure3Note3(testTimeMod):
    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id= 3
        self.item_id = 2
        testTimeMod.setUp(self)

class testMeasure3Note4(testTimeMod):
    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id= 3
        self.item_id = 3
        testTimeMod.setUp(self)

class testMeasure3Note5(testTimeMod):
    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id= 3
        self.item_id = 4
        testTimeMod.setUp(self)

class testMeasure3Note6(testTimeMod):
    def setUp(self):
        self.actual = 6
        self.normal = 4
        self.measure_id= 3
        self.item_id = 5
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)

class testMeasure4Note1(testTimeMod):
    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id= 4
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.bracket = True
        testTimeMod.setUp(self)

class testMeasure4Note2(testTimeMod):
    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id= 4
        self.item_id = 1
        testTimeMod.setUp(self)

class testMeasure4Note3(testTimeMod):
    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id= 4
        self.item_id = 2
        testTimeMod.setUp(self)

class testMeasure4Note4(testTimeMod):
    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id= 4
        self.item_id = 3
        testTimeMod.setUp(self)

class testMeasure4Note5(testTimeMod):
    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id= 4
        self.item_id = 4
        testTimeMod.setUp(self)

class testMeasure4Note6(testTimeMod):
    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id= 4
        self.item_id = 5
        testTimeMod.setUp(self)

    def testChord(self):
        self.assertTrue(self.item.chord)

class testMeasure4Note7(testTimeMod):
    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id= 4
        self.item_id = 6
        testTimeMod.setUp(self)

class testMeasure4Note8(testTimeMod):
    def setUp(self):
        self.actual = 7
        self.normal = 4
        self.measure_id= 4
        self.item_id = 7
        testTimeMod.setUp(self)

class testMeasure5Note1(testTimeMod):
    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id= 5
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.bracket = False
        testTimeMod.setUp(self)

class testMeasure5Note2(testTimeMod):
    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id= 5
        self.item_id = 1
        testTimeMod.setUp(self)

class testMeasure5Note3(testTimeMod):
    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id= 5
        self.item_id = 2
        testTimeMod.setUp(self)

class testMeasure5Note4(testTimeMod):
    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id= 5
        self.item_id = 3
        testTimeMod.setUp(self)

class testMeasure5Note5(testTimeMod):
    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id= 5
        self.item_id = 4
        testTimeMod.setUp(self)

class testMeasure5Note6(testTimeMod):
    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id= 5
        self.item_id = 5
        testTimeMod.setUp(self)

class testMeasure5Note7(testTimeMod):
    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id= 5
        self.item_id = 6
        testTimeMod.setUp(self)

class testMeasure5Note8(testTimeMod):
    def setUp(self):
        self.actual = 8
        self.normal = 8
        self.measure_id= 5
        self.item_id = 7
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)

class testMeasure6Note1(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 0
        self.notation_id = 0
        self.type = "start"
        self.bracket = False
        testTimeMod.setUp(self)

class testMeasure6Note2(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 1
        testTimeMod.setUp(self)

class testMeasure6Note3(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 2
        testTimeMod.setUp(self)

class testMeasure6Note4(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 3
        testTimeMod.setUp(self)

class testMeasure6Note5(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 4
        testTimeMod.setUp(self)

class testMeasure6Note6(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 5
        testTimeMod.setUp(self)

class testMeasure6Note7(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 6
        testTimeMod.setUp(self)

class testMeasure6Note8(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 7
        testTimeMod.setUp(self)

class testMeasure6Note9(testTimeMod):
    def setUp(self):
        self.actual = 9
        self.normal = 8
        self.measure_id= 6
        self.item_id = 8
        self.notation_id = 0
        self.type = "stop"
        testTimeMod.setUp(self)