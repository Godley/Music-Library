from implementation.primaries.Loading.classes import MxmlParser, Piece, Measure, Part, Note, text
import unittest

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

