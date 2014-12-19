from implementation.primaries.Loading.classes import MxmlParser, Harmony, Piece, Measure, Part
import unittest


class MeasureTesting(unittest.TestCase):
    def setUp(self):
        self.tags = []
        self.tags.append("measure")
        self.attrs = {"number": "1"}
        self.chars = {}
        self.handler = MxmlParser.HandleMeasures
        self.piece = Piece.Piece()
        self.piece.Parts["P1"] = Part.Part()
        MxmlParser.part_id = "P1"
        self.part = self.piece.Parts["P1"]


class testHandleMeasures(MeasureTesting):

    def testNoData(self):
        MxmlParser.part_id = None
        self.tags.remove("measure")
        self.attrs.pop("number")
        self.assertEqual(None, self.handler(self.tags, self.attrs, self.chars, self.piece))

    def testUnrelatedTag(self):
        MxmlParser.part_id = None
        self.tags.remove("measure")
        self.attrs.pop("number")
        self.tags.append("wibble")
        self.assertEqual(None, self.handler(self.tags, self.attrs, self.chars, self.piece))

    def testMeasureTag(self):
        self.handler(self.tags, self.attrs, None, self.piece)
        self.assertEqual(1, MxmlParser.measure_id)
        self.assertEqual(Measure.Measure, type(self.piece.Parts["P1"].measures[1]))


class testKeySig(MeasureTesting):
    def testModeTag(self):
        self.tags.append("key")
        self.tags.append("mode")
        self.chars["mode"] = "minor"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "key"))
        self.assertEqual("minor", exp_measure.key.mode)

    def testFifthsTag(self):
        self.tags.append("key")
        self.tags.append("fifths")
        self.chars["fifths"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "key"))
        self.assertEqual(3, exp_measure.key.fifths)

    def testModeNoMeasureTag(self):
        self.tags.remove("measure")
        self.attrs.pop("number")
        result = self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual(None, result)
        self.attrs["number"] = "1"
        self.tags.append("measure")
        self.assertEqual(1, self.handler(self.tags, self.attrs, self.chars, self.piece))


class testMeter(MeasureTesting):
    def testBeatTag(self):
        self.tags.append("meter")
        self.tags.append("beats")
        self.chars["beats"] = "4"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "meter"))
        self.assertEqual(4, exp_measure.meter.beats)

    def testBeatTypeTag(self):
        self.tags.append("meter")
        self.tags.append("beat-type")
        self.chars["beat-type"] = "4"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "meter"))
        self.assertEqual(4, exp_measure.meter.type)


class testClef(MeasureTesting):
    def testLineTag(self):
        self.tags.append("clef")
        self.tags.append("line")
        self.chars["line"] = 2
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "clef"))
        self.assertEqual(2, exp_measure.clef.line)

    def testSignTag(self):
        self.tags.append("clef")
        self.tags.append("sign")
        self.chars["sign"] = "G"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "clef"))
        self.assertEqual("G", exp_measure.clef.sign)


class testTranspose(MeasureTesting):
    def testTransposeDiatonicTag(self):
        self.tags.append("transpose")
        self.tags.append("diatonic")
        self.chars["diatonic"] = "0"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "transpose"))
        self.assertEqual("0", exp_measure.transpose.diatonic)

    def testTransposeChromaticTag(self):
        self.tags.append("transpose")
        self.tags.append("chromatic")
        self.chars["chromatic"] = "0"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "transpose"))
        self.assertEqual("0", exp_measure.transpose.chromatic)

    def testTransposeOctaveChangeTag(self):
        self.tags.append("transpose")
        self.tags.append("octave-change")
        self.chars["octave-change"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "transpose"))
        self.assertEqual("1", exp_measure.transpose.octave)

    def testPrintNoAttribs(self):
        self.tags.append("print")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertFalse(hasattr(exp_measure, "new-system"))
        self.assertFalse(hasattr(exp_measure, "new-page"))


class testPrint(MeasureTesting):
    def testPrintNewSysAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-system": "yes"}
        self.handler(self.tags, self.attrs, None, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "newSystem"))
        self.assertTrue(exp_measure.newSystem)

    def testPrintNewPageAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-page": "yes"}
        self.handler(self.tags, self.attrs, None, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "newPage"))
        self.assertTrue(exp_measure.newPage)

    def testPrintBothAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-page": "yes", "new-system": "yes"}
        self.handler(self.tags, self.attrs, None, self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "newPage"))
        self.assertTrue(exp_measure.newPage)
        self.assertTrue(hasattr(exp_measure, "newSystem"))
        self.assertTrue(exp_measure.newSystem)


class testHarmony(MeasureTesting):
    def setUp(self):
        MeasureTesting.setUp(self)
        self.tags.append("harmony")


    def testHarmonyTag(self):
        self.tags.append("harmony")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(self.part.measures[1].items[-1], Harmony.Harmony)


    def testRootStep(self):
        '''<harmony default-y="100">
        <root>
          <root-step>A</root-step>
        </root>
        <kind halign="center" parentheses-degrees="yes">major</kind>
        <degree>
          <degree-value>9</degree-value>
          <degree-alter>0</degree-alter>
          <degree-type text="">add</degree-type>
        </degree>
      </harmony>'''
        self.tags.append("root")
        self.tags.append("root-step")
        self.chars["root-step"] = "A"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.part.measures[1].items[-1], "root"))

    def testRootStepVal(self):
        self.tags.append("root")
        self.tags.append("root-step")
        self.chars["root-step"] = "A"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("A", self.part.measures[1].items[-1].root.step)

    def testRootAlter(self):
        self.tags.append("root")
        self.tags.append("root-alter")
        self.chars["root-alter"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("1", self.part.measures[1].items[-1].root.alter)

    def testKindTag(self):
        self.tags.append("kind")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.part.measures[1].items[-1], "kind"))

    def testKindVal(self):
        self.tags.append("kind")
        self.chars["kind"] = "major"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("major", self.part.measures[1].items[-1].kind.value)

    def testKindAttribs(self):
        self.tags.append("kind")
        self.chars["kind"] = "major"
        self.attrs["kind"] = {"text": "6", "halign": "center", "parenthesis-degrees": "no"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.part.measures[1].items[-1].kind, "text"))
        self.assertTrue(hasattr(self.part.measures[1].items[-1].kind, "halign"))
        self.assertTrue(hasattr(self.part.measures[1].items[-1].kind, "parenthesis"))


    def testBassTag(self):
        # because I'm all about that
        self.tags.append("bass")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.part.measures[1].items[-1], "bass"))

    def testBassStepVal(self):
        self.tags.append("bass")
        self.tags.append("bass-step")
        self.chars["bass-step"] = "D"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("D", self.part.measures[1].items[-1].bass.step)

    def testBassAlter(self):
        self.tags.append("bass")
        self.tags.append("bass-alter")
        self.chars["bass-alter"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("1", self.part.measures[1].items[-1].bass.alter)

    def testDegreeTag(self):
        self.tags.append("degree")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual(1, len(self.part.measures[1].items[-1].degrees))

    def testDegreeValue(self):
        self.tags.append("degree")
        self.tags.append("degree-value")
        self.chars["degree-value"] = "9"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("9", self.part.measures[1].items[-1].degrees[-1].value)

    def testDegreeAlter(self):
        self.tags.append("degree")
        self.tags.append("degree-alter")
        self.chars["degree-alter"] = "1"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("1", self.part.measures[1].items[-1].degrees[-1].alter)

    def testDegreeType(self):
        self.tags.append("degree")
        self.tags.append("degree-type")
        self.chars["degree-type"] = "add"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("add", self.part.measures[1].items[-1].degrees[-1].type)

    def testDegreeDisplay(self):
        self.tags.append("degree")
        self.tags.append("degree-type")
        self.chars["degree-type"] = "add"
        self.attrs["degree-type"] = {"text": ""}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("", self.part.measures[1].items[-1].degrees[-1].display)