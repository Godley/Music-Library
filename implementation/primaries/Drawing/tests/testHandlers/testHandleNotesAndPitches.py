import unittest
from implementation.primaries.Drawing.classes.tree_cls.PieceTree import PieceTree
from implementation.primaries.Drawing.classes.tree_cls.OtherNodes import DirectionNode
from implementation.primaries.Drawing.classes import MxmlParser, Piece, Measure, Part, Note


class notes(unittest.TestCase):
    def setUp(self):
        self.tags = ["note"]
        self.chars = {}
        self.attrs = {"part":{"id": "P1"}, "measure":{"number": "1"}}
        self.handler = MxmlParser.CreateNote
        MxmlParser.part_id = "P1"
        MxmlParser.measure_id = 1
        MxmlParser.note = None
        MxmlParser.expression = None
        MxmlParser.direction = None
        self.piece = PieceTree()
        self.piece.addPart(Part.Part(), index="P1")
        self.piece.getPart("P1").addEmptyMeasure(1,1)
        self.data = {"note": None, "direction": None, "expression": None}


    def copy(self):
        pass

class testCreateNoteHandler(notes):
    def setUp(self):
        if isinstance(self, testCreateNoteHandler):
            self.tags = ["note"]
        notes.setUp(self)

    def testNoTags(self):
        self.tags.remove("note")
        self.attrs = {}
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece, self.data), "ERROR: 0 tags should do nothing in method CreateNote in testNoData")

    def testIrrelevantTag(self):
        self.tags.remove("note")
        self.attrs = {}
        self.tags.append("hello")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars, self.piece, self.data), "ERROR: irrelevant tags should get nothing from method CreateNote in testIrrelevantTags")

    def testNoteTag(self):
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.copy()
        self.assertIsInstance(MxmlParser.note, Note.Note)

    def testNoteChordTag(self):
        self.tags.append("chord")
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.copy()
        self.assertTrue(hasattr(MxmlParser.note, "chord"))
#deprecated method of handling: not sure how to test this now? it's done at parser level rather than handler level
    # def testNoteChordTagAffectsPreviousNote(self):
    #     self.tags.append("chord")
    #     MxmlParser.notes[1] = []
    #     MxmlParser.notes[1].append(Note.Note())
    #     self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
    #     self.assertTrue(hasattr(MxmlParser.notes[1][len(MxmlParser.notes[1])-2], "chord"))

    def testRestTag(self):
        self.tags.append("rest")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note, "rest"))
        self.assertEqual(True, MxmlParser.note.rest)

    def testRestMeasure(self):
        self.tags.append("rest")
        self.attrs["rest"] = {"measure":"yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note, "MeasureRest"))
        self.assertEqual(True, MxmlParser.note.MeasureRest)

    def testCueTag(self):
        self.tags.append("cue")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note, "cue"))

    def testGraceTag(self):
        self.tags.append("grace")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(MxmlParser.note.Search(Note.GraceNote), Note.GraceNote)

    def testGraceIsFirst(self):
        self.tags.append("grace")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(MxmlParser.note.Search(Note.GraceNote).first)

    def testDurationTag(self):
        self.tags.append("duration")
        self.chars["duration"] = "8"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note,"duration"), "ERROR: note should have duration attrib")
        self.assertEqual(8, MxmlParser.note.duration, "ERROR: note duration set incorrectly")

    def testTypeTag(self):
        self.tags.append("type")
        self.chars["type"] = "eighth"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note,"val_type"))
        self.assertEqual(8, MxmlParser.note.duration)


    def testDotTag(self):
        self.tags.append("dot")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(MxmlParser.note.dots, 1)


    def testDoubleDot(self):
        self.tags.append("dot")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.tags.append("dot")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertEqual(MxmlParser.note.dots, 2)

    def testTieTag(self):
        self.tags.append("tie")
        self.attrs["tie"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        expected = MxmlParser.note
        self.assertEqual(1, len(MxmlParser.note.ties))
        self.assertEqual("start",expected.ties[-1].type)

    def testStemTag(self):
        self.tags.append("stem")
        self.chars["stem"] = "up"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        note = MxmlParser.note
        self.assertTrue(hasattr(note, "stem"), "ERROR: stem attrib not added to note")
        self.assertEqual(Note.Stem, type(note.stem), "ERROR: stem not of type Stem")
        self.assertEqual("up",note.stem.type, "ERROR: stem type value incorrect")

    def testBeamTag(self):
        self.tags.append("beam")
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note, "beams"))
        self.assertIsInstance(MxmlParser.note.beams[0], Note.Beam)

    def testBeamType(self):
        self.tags.append("beam")
        self.chars["beam"] = "begin"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.beams[0], "type"))
        self.assertEqual("begin",MxmlParser.note.beams[0].type)

    def testBeamAttrs(self):
        self.tags.append("beam")
        self.chars["beam"] = "begin"
        self.attrs["beam"] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(1 in MxmlParser.note.beams)

    def testAccidental(self):
        self.tags.append("accidental")
        self.chars["accidental"] = "sharp"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note, "pitch"))
        self.assertTrue(hasattr(MxmlParser.note.pitch, "accidental"))


class pitchin(unittest.TestCase):
    def setUp(self):
        self.tags = ["note","pitch"]
        self.attrs = {}
        self.chars = {}
        MxmlParser.note = Note.Note()
        MxmlParser.part_id = "P1"
        MxmlParser.measure_id = 1
        self.handler = MxmlParser.HandlePitch
        self.piece = Piece.Piece()
        self.data = {"note": None, "direction": None, "expression": None}

class testHandlePitch(pitchin):
    def testNoTags(self):
        self.tags = []
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece, self.data))

    def testIrrelevantTag(self):
        self.tags.append("hello")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece, self.data))

    def testPitchTag(self):
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note, "pitch"), "ERROR: pitch attrib not created")

    def testStepTag(self):
        self.tags.append("step")
        self.chars["step"] = "E"
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "step"), "ERRPR: pitch step attrib not set")
        self.assertEqual("E",MxmlParser.note.pitch.step,"ERROR: note pitch step value incorrect")

    def testAlterTag(self):
        self.tags.append("alter")
        self.chars["alter"] = "-1"
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "alter"))
        self.assertEqual(-1,MxmlParser.note.pitch.alter)

    def testOctaveTag(self):
        self.tags.append("octave")
        self.chars["octave"] = "1"
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "octave"))
        self.assertEqual("1",MxmlParser.note.pitch.octave)

class testUnpitched(pitchin):
    def setUp(self):
        pitchin.setUp(self)
        self.tags.remove("pitch")
        self.tags.append("unpitched")

    def testUnpitchedTag(self):
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "unpitched"))

    def testDisplayStepTag(self):
        self.tags.append("display-step")
        self.chars["display-step"] = "E"
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "step"))

    def testDisplayOctaveTag(self):
        self.tags.append("display-octave")
        self.chars["display-octave"] = "2"
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.pitch, "octave"))

class testNotehead(testCreateNoteHandler):
    def setUp(self):
        testCreateNoteHandler.setUp(self)
        self.tags.append("notehead")

    def testNoteheadTag(self):
        self.tags = ["note"]
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.tags = ["note", "notehead"]
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note, "notehead"))
        self.assertIsInstance(MxmlParser.note.notehead, Note.Notehead)

    def testNoteheadFilled(self):
        self.tags = ["note"]
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.tags.append("notehead")
        self.attrs["notehead"] = {"filled":"yes"}
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.notehead, "filled"))
        self.assertTrue(MxmlParser.note.notehead.filled)

    def testNoteheadType(self):
        self.tags = ["note"]
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.tags.append("notehead")
        self.chars["notehead"] = "diamond"
        self.handler(self.tags,self.attrs,self.chars,self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.notehead, "type"))
        self.assertEqual("diamond",MxmlParser.note.notehead.type)

class testTuplets(notes):
    def setUp(self):
        notes.setUp(self)
        self.tags.append("time-modification")
        MxmlParser.note = Note.Note()
        self.handler = MxmlParser.handleTimeMod

    def testMod(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note, "timeMod"))

    def testModVal(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertIsInstance(MxmlParser.note.timeMod, Note.TimeModifier)


    def testModNormal(self):
        self.tags.append("normal-notes")
        self.chars["normal-notes"] = "2"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.timeMod, "normal"))
        self.assertEqual(2, MxmlParser.note.timeMod.normal)

    def testModActual(self):
        self.tags.append("actual-notes")
        self.chars["actual-notes"] = "3"
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        self.assertTrue(hasattr(MxmlParser.note.timeMod, "actual"))
        self.assertEqual(3, MxmlParser.note.timeMod.actual)

    def testTupletTag(self):
        self.tags.append("notations")
        self.tags.append("tuplet")
        self.attrs["tuplet"] = {"type":"stop"}
        self.handler(self.tags, self.attrs, self.chars, self.piece, self.data)
        direction = MxmlParser.note.closing_notation[0]
        self.assertIsInstance(direction, Note.Tuplet)

