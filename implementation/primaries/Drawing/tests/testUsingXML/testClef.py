from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Clef
import os

partname = "clefs.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testClef(xmlSet):
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
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

class CTests(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.p_id = "P1"
        self.sign = ""
        self.line = None
        self.clef_octave_change = None
        self.measure = None

    def testClef(self):
        if self.measure is not None:
            measure = piece.Parts[self.p_id].measures[self.measure]
            self.assertTrue(hasattr(measure, "clef"))


    def testSign(self):
        if self.measure is not None:
            measure = piece.Parts[self.p_id].measures[self.measure]
            self.assertEqual(self.sign, measure.clef.sign)

    def testLine(self):
        if self.measure is not None:
            measure = piece.Parts[self.p_id].measures[self.measure]
            self.assertEqual(self.line, measure.clef.line)

    def testOctaveChange(self):
        if self.measure is not None and self.clef_octave_change is not 0:
            measure = piece.Parts[self.p_id].measures[self.measure]
            self.assertEqual(self.clef_octave_change, measure.clef.octave_change)

class testMeasure1(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 1
        self.sign = "G"
        self.line = 2
        self.clef_octave_change = 0

class testMeasure2(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 2
        self.sign = "G"
        self.line = 2
        self.clef_octave_change = 1

class testMeasure3(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 3
        self.sign = "G"
        self.line = 2
        self.clef_octave_change = 2

class testMeasure4(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 4
        self.sign = "G"
        self.line = 2
        self.clef_octave_change = -1

class testMeasure5(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 5
        self.sign = "G"
        self.line = 1
        self.clef_octave_change = 0

class testMeasure6(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 6
        self.sign = "C"
        self.line = 1
        self.clef_octave_change = 0

class testMeasure7(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 7
        self.sign = "C"
        self.line = 2
        self.clef_octave_change = 0

class testMeasure8(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 8
        self.sign = "C"
        self.line = 3
        self.clef_octave_change = 0

class testMeasure9(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 9
        self.sign = "C"
        self.line = 4
        self.clef_octave_change = 0

class testMeasure10(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 10
        self.sign = "C"
        self.line = 5
        self.clef_octave_change = 0

class testMeasure11(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 11
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = 0

class testMeasure12(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 12
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = 1

class testMeasure13(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 13
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = 2

class testMeasure14(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 14
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = -1

class testMeasure15(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 15
        self.sign = "F"
        self.line = 4
        self.clef_octave_change = -2

class testMeasure16(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 16
        self.sign = "F"
        self.line = 3
        self.clef_octave_change = 0

class testMeasure17(CTests):
    def setUp(self):
        CTests.setUp(self)
        self.measure = 17
        self.sign = "F"
        self.line = 5
        self.clef_octave_change = 0