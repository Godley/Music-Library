from implementation.primaries.Drawing.classes import Measure, Note, Directions
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testMeasure(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.lilystring = "\\new Staff {}"

class testMeasureStaves(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.items[2] = []
        self.lilystring = "\\new PianoStaff <<\n \\new Staff {} \n \\new Staff {} \n>>"

class testMeasureNote(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.items[1].append(Note.Note())
        self.item.items[1][0].pitch = Note.Pitch()
        self.lilystring = "\\new Staff {c'}"

class testMeasureTempo(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.items[1].append(Directions.Metronome(beat=4,min=60))
        self.lilystring = "\\new Staff {\\tempo 4=60}"

class testMeasureTwoDirections(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.items[1].append(Directions.Direction(text="hello world",placement="above"))
        self.item.items[1].append(Directions.Metronome(beat=4,min=60))
        self.lilystring = "\\new Staff {^\\markup { hello world }\\tempo 4=60}"

class testMeasureTwoNotes(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.items[1].append(Note.Note())
        self.item.items[1][0].pitch = Note.Pitch()
        self.item.items[1].append(Note.Note())
        self.item.items[1][1].pitch = Note.Pitch()
        self.lilystring = "\\new Staff {c'c'}"

class testMeasureOneNoteOneDirection(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.items[1].append(Note.Note())
        self.item.items[1][0].pitch = Note.Pitch()
        self.item.items[1].append(Directions.Direction(text="hello",placement="below"))
        self.lilystring = "\\new Staff {c'_\\markup { hello }}"


