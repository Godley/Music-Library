from implementation.primaries.Drawing.classes import Measure, Note, Directions, Meter
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes.tree_cls.NoteNode import NoteNode
import unittest

class MeasureTests(Lily):

    def testValue(self):
        if hasattr(self, "lilystring"):
            if hasattr(self, "item"):
                self.assertEqual(self.lilystring, self.item.toLily())

class testMeasure(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        self.item.SetItem(Measure.Measure())
        self.lilystring = " | "

class testMeasureNote(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        self.item.SetItem(Measure.Measure())
        note = Note.Note()
        note.pitch= Note.Pitch()
        self.item.addNote(note)
        self.lilystring = "c'  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenote"

class testMeasureChord(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch= Note.Pitch()
        self.item.addNote(note)
        note2 = Note.Note(chord=True)
        note2.pitch = Note.Pitch()
        self.item.addNote(note2, chord=True)
        self.lilystring = "<c' c'>  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotechord"

class testMeasureNoteWithGrace(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note(type="quarter")
        note.pitch= Note.Pitch()
        note.addNotation(Note.GraceNote(first=True))
        self.item.addNote(note)
        self.item.RunVoiceChecks()
        self.lilystring = "\grace { c'4 }  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotegrace"

class testMeasureTempo(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        self.item.addDirection(Directions.Metronome(beat="quarter",min=60))
        self.item.addNote(NoteNode())
        self.lilystring = " \\tempo 4=60  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretempo"

class testMeasureTwoDirections(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        self.item.addDirection(Directions.Direction(text="hello world",placement="above"))
        self.item.addDirection(Directions.Metronome(beat="quarter",min=60))
        self.item.addNote(NoteNode())
        self.lilystring = " ^\\markup { \"hello world\"  } \\tempo 4=60  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwodirections"

class testMeasureTwoNotes(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        self.item.addNote(note2)
        self.lilystring = "c' c'  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwonotes"

class testMeasureOneNoteOneDirection(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addDirection(Directions.Direction(text="hello",placement="below"))
        self.item.addNote(note)
        self.lilystring = "c' _\\markup { \"hello\"  }  | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotedirection"

class testPartialMeasure(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        self.item.GetItem().partial = True
        self.item.GetItem().meter = Meter.Meter(beats=4, type=4)
        note = Note.Note(type="quarter")
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.lilystring = "\\time 4/4 \partial 4 c'4 | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurePartial"

class testMeasureTranspositionCalc(unittest.TestCase):
    def setUp(self):
        self.item = Measure.Measure()


    def testCalcUpWithChromatic(self):
        self.item.transpose = Measure.Transposition(chromatic=2)
        expected = "\\transpose c' d' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)

    def testCalcUpWithDiatonic(self):
        self.item.transpose = Measure.Transposition(diatonic=1)
        expected = "\\transpose c' d' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)

    def testCalcOctaveShift(self):
        self.item.transpose = Measure.Transposition(octave=1)
        expected = "\\transpose c' c'' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)




class testMeasureNoteWithShifter(Lily):
    def setUp(self):
        self.item = MeasureNode()
        node = NoteNode()
        node.GetItem().pitch = Note.Pitch(octave=4)
        self.item.addNote(node)
        dirnode = Directions.OctaveShift(amount=8, type="up")
        self.item.addDirection(dirnode)
        node2 = NoteNode()
        node2.GetItem().pitch = Note.Pitch(octave=4)
        self.item.addNote(node2)
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{a8 ","c'8]}"]
        self.lilystring = "c' \n\\ottava #-1\n c'  | "
        self.name = "noteOctaveShift"

class testShiftBeforeNote(unittest.TestCase):
    def setUp(self):
        self.item = MeasureNode()
        dirnode = Directions.OctaveShift(amount=8, type="up")
        self.item.addDirection(dirnode)
        self.node = NoteNode()
        self.node.GetItem().pitch = Note.Pitch(octave=2)
        self.item.addNote(self.node)

    def testLilystring(self):
        value = "\n\\ottava #-1\n c,  | "
        self.assertEqual(value, self.item.toLily())


class testGraceAtStartOfMeasure(unittest.TestCase):
    def setUp(self):
        self.item = MeasureNode()
        node = NoteNode()
        self.note = Note.Note(type="quarter")
        self.note.addNotation(Note.GraceNote())
        self.note.pitch = Note.Pitch()
        node.SetItem(self.note)
        self.item.addNote(node)
        self.item.RunVoiceChecks()

    def testIsFirstGraceNote(self):
        result = self.note.Search(Note.GraceNote)
        self.assertTrue(result.first)

    def testLilystring(self):
        value = "\grace { c'4 }  | "
        self.assertEqual(value, self.item.toLily())

