from implementation.primaries.Drawing.classes import Measure, Note, Directions
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes.tree_cls.PieceTree import MeasureNode, StaffNode,NoteNode,DirectionNode
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

class testStaffWithMeasureWithTransposition(unittest.TestCase):
    def setUp(self):
        self.item = StaffNode()
        m1 = MeasureNode()
        item = m1.GetItem()
        item.transpose = Measure.Transposition(octave=1)
        self.item.AddChild(m1, 1)

    def testOutput(self):
        lstring = self.item.toLily()
        expected = "\\autoBeamOff % measure 1\n\\transpose c' c'' { | \n\n}"
        self.assertEqual(lstring, expected)

    def testOutputWithAnotherTransposedMeasure(self):
        m2 = MeasureNode()
        item = m2.GetItem()
        item.transpose = Measure.Transposition(octave=-1)
        self.item.AddChild(m2, 2)
        lstring = self.item.toLily()
        expected = "\\autoBeamOff % measure 1\n\\transpose c' c'' { | \n\n} % measure 2\n\\transpose c' c { | \n\n}"
        self.assertEqual(lstring, expected)

    def testOutputWithAnotherMeasure(self):
        m2 = MeasureNode()
        item = m2.GetItem()
        self.item.AddChild(m2, 2)
        lstring = self.item.toLily()
        expected = "\\autoBeamOff % measure 1\n\\transpose c' c'' { | \n\n % measure 2\n | \n\n}"
        self.assertEqual(lstring, expected)

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
        self.lilystring = "c'\n\\ottava #1\n c'''  | "
        self.name = "noteOctaveShift"

class testMeasureNoteShift(unittest.TestCase):
    def setUp(self):
        self.item = MeasureNode()
        self.node = NoteNode()
        self.node.GetItem().pitch = Note.Pitch()
        self.item.addNote(self.node)
        dirnode = Directions.OctaveShift(amount=8, type="up")
        self.item.addDirection(dirnode)
        self.node2 = NoteNode()
        self.node2.GetItem().pitch = Note.Pitch(octave=2)
        self.item.addNote(self.node2)

    def testHasShift(self):
        self.assertTrue(hasattr(self.node, "shift"))

    def testShiftVal(self):
        self.assertEqual(self.node.shift, 2)

    def testNode2Pitch(self):
        self.assertEqual(self.node2.GetItem().pitch.octave, 4)

    def testNode3Pitch(self):
        node3 = NoteNode()
        node3.GetItem().pitch = Note.Pitch(octave=3)
        self.item.addNote(node3)
        self.assertEqual(node3.GetItem().pitch.octave, 5)

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

class testPedalBeforeNote(unittest.TestCase):
    def setUp(self):
        self.item = MeasureNode()
        dirnode = Directions.Pedal(type="start")
        self.item.addDirection(dirnode)
        self.node = NoteNode()
        self.node.GetItem().pitch = Note.Pitch(octave=2)
        self.item.addNote(self.node)


    def testLilystring(self):
        value = "\sustainOn\n c,  | "
        self.assertEqual(value, self.item.toLily())

