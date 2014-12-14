from implementation.primaries.Loading.classes import MxmlParser, Piece, Measure, Part, Note
import unittest
from unittest import mock

class testSetupPiece(unittest.TestCase):
    def setUp(self):
        self.handler = MxmlParser.SetupPiece
        self.tags = []
        self.attrs = {}
        self.chars = {}
        self.piece = Piece.Piece()

    def testNoTags(self):
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: testNoTags failed: nothing should happen if there are no tags in list")

    def testMetaExists(self):
        self.assertFalse(hasattr(self.piece, "meta"), "ERROR: testMetaExists failed: meta should not be set in piece class at beginning of testing")

    def testIrrelevantTag(self):
        self.tags.append("lol")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: irrelevant tag should do nothing in TestIrrelevance")

    def testTitleTag(self):
        self.tags.append("movement-title")
        self.chars["movement-title"] = "hehehe"
        self.handler(self.tags, self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.piece, "meta"), "ERROR: Meta should exist in TestTitleTag")
        self.assertEqual("hehehe", self.piece.meta.title, "ERROR: title set incorrectly in TestTitleTag")

    def testCompTag(self):
        self.tags.append("creator")
        self.attrs["creator"] = {"type":"composer"}
        self.chars["creator"] = "lee"
        self.handler(self.tags, self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.piece, "meta"), "ERROR: meta should exist in piece class in TestCompTag")
        self.assertEqual("lee",self.piece.meta.composer, "ERROR: composer should match expected in TestCompTag")

    def testTitleCompTag(self):
        self.tags.append("creator")
        self.attrs["creator"] = {"type":"composer"}
        self.chars["creator"] = "lee"
        self.chars["movement-title"] = "hello world"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.piece.meta, "composer"), "ERROR: meta should have composer attrib in TestTitleCompTag")
        self.assertEqual("lee",self.piece.meta.composer, "ERROR: composer should match test in TestTitleCompTag")
        self.tags.append("movement-title")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.piece.meta, "title"), "ERROR: meta should have title in TestTitleCompTag")
        self.assertEqual("hello world", self.piece.meta.title, "ERROR: meta title set incorrectly in TestTitleCompTag")

class testHandlePart(unittest.TestCase):
    def setUp(self):
        self.handler = MxmlParser.UpdatePart
        self.tags = []
        self.chars = {}
        self.attrs = {}
        self.piece = Piece.Piece()

    def testNoData(self):
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: no tags should return none in TestNodata")

    def testIrrelevantTag(self):
        self.tags.append("wut")
        self.assertEqual(None, self.handler(self.tags, self.attrs,self.chars,self.piece), "ERROR: irrelevant tags should return none in TestIrrelevantTag")

    def testScorePartTag(self):
        MxmlParser.part_id = None
        self.assertEqual(None,MxmlParser.part_id,"ERROR: part_id not none in testScorePartTag")
        self.tags.append("score-part")
        self.attrs = {"id":"P1"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(1, len(self.piece.Parts.keys()), "ERROR: part not created properly in testScorePartTag")

    def testPnameTag(self):
        self.assertEqual(0, len(self.piece.Parts.keys()), "ERROR: part list should be empty in TestPnameTag")
        self.tags.append("score-part")
        self.attrs = {"id":"P1"}
        self.tags.append("part-name")
        self.chars["part-name"] = "will"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual("will", self.piece.Parts["P1"].name, "ERROR: partname not set correctly in testPnameTag")

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

class testCreateNoteHandler(unittest.TestCase):
    def setUp(self):
        self.tags = ["note"]
        self.chars = {}
        self.attrs = {}
        self.handler = MxmlParser.CreateNote
        MxmlParser.part_id = "P1"
        MxmlParser.measure_id = 1
        MxmlParser.note = None
        self.piece = Piece.Piece()
        self.piece.Parts["P1"] = Part.Part()
        self.piece.Parts["P1"].measures[1] = Measure.Measure()

    def testNoTags(self):
        self.tags.remove("note")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: 0 tags should do nothing in method CreateNote in testNoData")

    def testIrrelevantTag(self):
        self.tags.remove("note")
        self.tags.append("hello")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars, self.piece), "ERROR: irrelevant tags should get nothing from method CreateNote in testIrrelevantTags")

    def testNoteTag(self):
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(Note.Note, type(MxmlParser.note), "ERROR: note global val is not a note instance in testNoteTag")
        self.assertEqual(MxmlParser.note, self.piece.Parts["P1"].measures[1].notes[0],"ERROR: note not added to measure correctly in testNoteTag")

    def testRestTag(self):
        self.tags.append("rest")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note, "rest"), "ERROR: note should have rest attrib")
        self.assertEqual(True, MxmlParser.note.rest, "ERROR: rest tag should make note's rest value true in testRestTag")

    def testDurationTag(self):
        self.tags.append("duration")
        self.chars["duration"] = "8"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note,"duration"),"ERROR: note should have duration attrib")
        self.assertEqual(8, MxmlParser.note.duration, "ERROR: note duration set incorrectly")

    def testDotTag(self):
        self.tags.append("dot")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note, "dotted"), "ERROR: note should have dotted attrib")
        self.assertTrue(MxmlParser.note.dotted, "ERROR: dotted attrib should be true")

    def testTieTag(self):
        self.tags.append("tie")
        self.attrs["type"] = "start"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        expected = self.piece.Parts["P1"].measures[1].notes[0]
        self.assertEqual(1, len(MxmlParser.note.ties), "ERROR: note tie not added to tie list in note")
        self.assertEqual("start",expected.ties[-1].type, "ERROR: note tie type not matching to test input")

    def testStemTag(self):
        self.tags.append("stem")
        self.chars["stem"] = "up"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        note = MxmlParser.note
        self.assertTrue(hasattr(note, "stem"), "ERROR: stem attrib not added to note")
        self.assertEqual(Note.Stem, type(note.stem), "ERROR: stem not of type Stem")
        self.assertEqual("up",note.stem.type, "ERROR: stem type value incorrect")

class testHandlePitch(unittest.TestCase):
    def setUp(self):
        self.tags = ["note","pitch"]
        self.attrs = {}
        self.chars = {}
        MxmlParser.note = Note.Note()
        MxmlParser.part_id = "P1"
        MxmlParser.measure_id = 1
        self.handler = MxmlParser.HandlePitch
        self.piece = Piece.Piece()

    def testNoTags(self):
        self.tags = []
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: no tags into method should give a result of none")

    def testIrrelevantTag(self):
        self.tags.append("hello")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: irrelevant tag should return no result")

    def testPitchTag(self):
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note, "pitch"), "ERROR: pitch attrib not created")

    def testStepTag(self):
        self.tags.append("step")
        self.chars["step"] = "E"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "step"), "ERRPR: pitch step attrib not set")
        self.assertEqual("E",MxmlParser.note.pitch.step,"ERROR: note pitch step value incorrect")

    def testAlterTag(self):
        self.tags.append("alter")
        self.chars["alter"] = "-1"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "accidental"))
        self.assertEqual("-1",MxmlParser.note.pitch.accidental)

    def testOctaveTag(self):
        self.tags.append("octave")
        self.chars["octave"] = "1"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "octave"))
        self.assertEqual("1",MxmlParser.note.pitch.octave)


class testCheckDynamics(unittest.TestCase):
    def setUp(self):
        self.handler = MxmlParser.CheckDynamics

    def testEmpty(self):
        self.assertFalse(self.handler(''))

    def testRandChar(self):
        self.assertFalse(self.handler('q'))

    def testP(self):
        self.assertTrue(self.handler('p'))

    def testF(self):
        self.assertTrue(self.handler('f'))

    def testmf(self):
        self.assertTrue(self.handler('mf'))

    def testmp(self):
        self.assertTrue(self.handler('mp'))

    def testpp(self):
        self.assertTrue(self.handler('pp'))

    def testff(self):
        self.assertTrue(self.handler('ff'))

    def testm(self):
        self.assertFalse(self.handler('m'))

    def testfm(self):
        self.assertFalse(self.handler('fm'))

    def testpm(self):
        self.assertFalse(self.handler('pm'))

    def testmm(self):
        self.assertFalse(self.handler('mm'))

class testHandleDirections(unittest.TestCase):
    def setUp(self):
        self.tags = []
        self.chars = {}
        self.attrs = {}
        self.handler = MxmlParser.HandleDirections
