from implementation.primaries.Drawing.classes import Measure, Note, Directions
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class MeasureTests(Lily):

    def testValue(self):
        if hasattr(self, "lilystring"):
            if hasattr(self, "item"):
                self.assertEqual(self.lilystring, self.item.toLily())

class testMeasure(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.lilystring = " r"

class testMeasureStaves(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.items[2] = []
        self.lilystring = " r"

class testMeasureNote(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        note = Note.Note()
        note.pitch= Note.Pitch()
        self.item.addNote(note)
        self.lilystring = " c'"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenote"

class testMeasureNoteWithGrace(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        note = Note.Note()
        note.pitch= Note.Pitch()
        note.grace = Note.GraceNote(first=True)
        self.item.addNote(note)
        self.lilystring = " \grace { c'}"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotegrace"

class testMeasureTempo(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.addDirection(Directions.Metronome(beat=4,min=60), 0)
        self.lilystring = " r\\tempo 4=60"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretempo"

class testMeasureTwoDirections(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.addDirection(Directions.Direction(text="hello world",placement="above"),0)
        self.item.addDirection(Directions.Metronome(beat=4,min=60),0)
        self.lilystring = " r^\\markup { hello world  }\\tempo 4=60"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwodirections"

class testMeasureTwoNotes(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        self.item.addNote(note2)
        self.lilystring = " c' c'"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwonotes"

class testMeasureOneNoteOneDirection(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.item.addDirection(Directions.Direction(text="hello",placement="below"), 0)
        self.lilystring = " c'_\\markup { hello  }"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotedirection"

class testMeasureSecondStave(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.lilystring = " c'"
        self.compile = True
        self.wrappers = ["<<\\new Staff{}\\new Staff {", "}>>"]
        Lily.setUp(self)
        self.name = "measurenote"


