from implementation.primaries.Drawing.classes import Measure, Note, Directions
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes.tree_cls.PieceTree import MeasureNode
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
        self.lilystring = " % voice 1\n{ c' } | "
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
        self.lilystring = " % voice 1\n{ <c' c'> } | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotechord"

class testMeasureNoteWithGrace(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch= Note.Pitch()
        note.addNotation(Note.GraceNote(first=True))
        self.item.addNote(note)
        self.lilystring = " % voice 1\n{ \grace { c' } } | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotegrace"

class testMeasureTempo(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        self.item.addDirection(Directions.Metronome(beat=4,min=60))
        self.lilystring = " % voice 1\n{ \\tempo 4=60 } | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretempo"

class testMeasureTwoDirections(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        self.item.addDirection(Directions.Direction(text="hello world",placement="above"))
        self.item.addDirection(Directions.Metronome(beat=4,min=60))
        self.lilystring = " % voice 1\n{ ^\\markup { \"hello world\"  }\\tempo 4=60 } | "
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
        self.lilystring = " % voice 1\n{ c' c' } | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwonotes"

class testMeasureOneNoteOneDirection(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.item.addDirection(Directions.Direction(text="hello",placement="below"))
        self.lilystring = " % voice 1\n{ c'_\\markup { \"hello\"  } } | "
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotedirection"

class testMeasureTranspositionCalc(unittest.TestCase):
    def setUp(self):
        self.item = Measure.Measure()


    def testCalcUpWithChromatic(self):
        self.item.transpose = Measure.Transposition(chromatic=2)
        expected = "\\transpose d' c' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)

    def testCalcUpWithDiatonic(self):
        self.item.transpose = Measure.Transposition(diatonic=1)
        expected = "\\transpose d' c' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)

    def testCalcOctaveShift(self):
        self.item.transpose = Measure.Transposition(octave=1)
        expected = "\\transpose c'' c' {"
        self.assertEqual(self.item.CalculateTransposition(), expected)



