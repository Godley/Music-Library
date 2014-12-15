from implementation.primaries.Loading.classes import MxmlParser, Piece, Measure, Part, Note, text
import unittest

class testHandleMeasures(unittest.TestCase):
    def setUp(self):
        self.tags = []
        self.tags.append("measure")
        self.attrs = {"number":"1"}
        self.chars = {}
        self.handler = MxmlParser.HandleMeasures
        self.piece = Piece.Piece()
        self.piece.Parts["P1"] = Part.Part()
        MxmlParser.part_id="P1"

    def testNoData(self):
        MxmlParser.part_id = None
        self.tags.remove("measure")
        self.attrs.pop("number")
        self.assertEqual(None,self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: measure should return none if nothing happening in TestNoData")

    def testUnrelatedTag(self):
        MxmlParser.part_id = None
        self.tags.remove("measure")
        self.attrs.pop("number")
        self.tags.append("wibble")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: measure should return none if tag not related to class in TestUnrelatedTag")

    def testMeasureTag(self):
        self.handler(self.tags,self.attrs,None,self.piece)
        self.assertEqual(1,MxmlParser.measure_id,"ERROR: measure_id not set correctly in testMeasureTag")
        self.assertEqual(Measure.Measure,type(self.piece.Parts["P1"].measures[1]), "ERROR: measure not created correctly in testMeasureTag")

    def testModeTag(self):
        self.tags.append("key")
        self.tags.append("mode")
        self.chars["mode"] = "minor"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "key"), "ERROR: key not created in testModeTag")
        self.assertEqual("minor",exp_measure.key.mode,"ERROR: mode not set correctly in testModeTag")

    def testFifthsTag(self):
        self.tags.append("key")
        self.tags.append("fifths")
        self.chars["fifths"] = "3"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "key"), "ERROR: key not created in testModeTag")
        self.assertEqual(3,exp_measure.key.fifths,"ERROR: mode not set correctly in testModeTag")

    def testModeNoMeasureTag(self):
        self.tags.remove("measure")
        self.attrs.pop("number")
        result = self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(None, result, "ERROR: if mode is in tag list but measure isn't, result should be none in testModeNoMeasureTag")
        self.attrs["number"] = "1"
        self.tags.append("measure")
        self.assertEqual(1, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: if measure tag is in and mode is in, result should be 1 in testModeNoMeasureTag")
    def testBeatTag(self):
        self.tags.append("meter")
        self.tags.append("beats")
        self.chars["beats"] = "4"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure,"meter"), "ERROR: meter not created in testBeatTag")
        self.assertEqual(4,exp_measure.meter.beats, "ERROR: beat value in meter class not correct in testBeatTag")

    def testBeatTypeTag(self):
        self.tags.append("meter")
        self.tags.append("beat-type")
        self.chars["beat-type"] = "4"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "meter"), "ERROR: meter not created in testBeatTypeTag")
        self.assertEqual(4,exp_measure.meter.type, "ERROR: beat type in meter class not correct in testBeatTypeTag")

    def testLineTag(self):
        self.tags.append("clef")
        self.tags.append("line")
        self.chars["line"] = 2
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "clef"), "ERROR: clef not created in testLineTag")
        self.assertEqual(2, exp_measure.clef.line, "ERROR: clef line value not correct in testLineTag")

    def testSignTag(self):
        self.tags.append("clef")
        self.tags.append("sign")
        self.chars["sign"] = "G"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "clef"), "ERROR: clef not created in testLineTag")
        self.assertEqual("G", exp_measure.clef.sign, "ERROR: clef sign value not correct in testLineTag")

    def testTransposeDiatonicTag(self):
        self.tags.append("transpose")
        self.tags.append("diatonic")
        self.chars["diatonic"] = "0"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "transpose"), "ERROR: transpose not created in testTransposeChromaticTag")
        self.assertEqual("0", exp_measure.transpose.diatonic, "ERROR: transpose diatonic value not correct in testTrnasposeDiatonicTag")

    def testTransposeChromaticTag(self):
        self.tags.append("transpose")
        self.tags.append("chromatic")
        self.chars["chromatic"] = "0"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "transpose"), "ERROR: transpose not created in testTransposeChromaticTag")
        self.assertEqual("0", exp_measure.transpose.chromatic, "ERROR: transpose chromatic value not correct in testTransposeChromaticTag")

    def testTransposeOctaveChangeTag(self):
        self.tags.append("transpose")
        self.tags.append("octave-change")
        self.chars["octave-change"] = "1"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "transpose"), "ERROR: transpose not created properly in testTransposeOctaveChangeTag")
        self.assertEqual("1", exp_measure.transpose.octave, "ERROR: octave change not set properly in testTransposeOctaveChangeTag")

    def testPrintNoAttribs(self):
        self.tags.append("print")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertFalse(hasattr(exp_measure, "new-system"), "ERROR: no attribs in print tag should set nothing, new-system is set instead")
        self.assertFalse(hasattr(exp_measure, "new-page"), "ERROR: no attribs in print tag mean nothing should be set, new-page set instead")

    def testPrintNewSysAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-system":"yes"}
        self.handler(self.tags,self.attrs,None,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "newSystem"), "ERROR: newSystem should be set after testPrintNewSysAttrib")
        self.assertTrue(exp_measure.newSystem, "ERROR: newSys should be set to true in test")

    def testPrintNewPageAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-page":"yes"}
        self.handler(self.tags,self.attrs,None,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "newPage"), "ERROR: newPage should be set after testPrintNewSysAttrib")
        self.assertTrue(exp_measure.newPage, "ERROR: newPage should be set to false in test")

    def testPrintBothAttrib(self):
        self.tags.append("print")
        self.attrs["print"] = {"new-page":"yes","new-system":"yes"}
        self.handler(self.tags,self.attrs,None,self.piece)
        exp_measure = self.piece.Parts["P1"].measures[1]
        self.assertTrue(hasattr(exp_measure, "newPage"), "ERROR: newPage should be set after testPrintBothAttrib")
        self.assertTrue(exp_measure.newPage, "ERROR: newPage should be set to false in test")
        self.assertTrue(hasattr(exp_measure, "newSystem"), "ERROR: newSystem should be set after testPrintBothAttrib")
        self.assertTrue(exp_measure.newSystem, "ERROR: newSystem should be set to false in test")


