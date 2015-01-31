from implementation.primaries.Drawing.classes import Measure, Note, Directions
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class MeasureTests(Lily):

    def testValue(self):
        if hasattr(self, "lilystring"):
            if hasattr(self, "item"):
                self.assertEqual(self.lilystring, self.item.toLily(self.staff_id))

class testMeasure(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.staff_id = 1
        self.lilystring = ""

class testMeasureStaves(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.staff_id = 2
        self.item.items[2] = []
        self.lilystring = ""

class testMeasureNote(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.staff_id = 1
        self.item.items[1].append(Note.Note())
        self.item.items[1][0].pitch = Note.Pitch()
        self.lilystring = " c'"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenote"

class testMeasureTempo(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.staff_id = 1
        self.item.items[1].append(Directions.Metronome(beat=4,min=60))
        self.lilystring = " \\tempo 4=60"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretempo"

class testMeasureTwoDirections(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.staff_id = 1
        self.item.items[1].append(Directions.Direction(text="hello world",placement="above"))
        self.item.items[1].append(Directions.Metronome(beat=4,min=60))
        self.lilystring = " ^\\markup { hello world } \\tempo 4=60"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwodirections"

class testMeasureTwoNotes(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.staff_id = 1
        self.item.items[1].append(Note.Note())
        self.item.items[1][0].pitch = Note.Pitch()
        self.item.items[1].append(Note.Note())
        self.item.items[1][1].pitch = Note.Pitch()
        self.lilystring = " c' c'"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measuretwonotes"

class testMeasureOneNoteOneDirection(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.staff_id = 1
        self.item.items[1].append(Note.Note())
        self.item.items[1][0].pitch = Note.Pitch()
        self.item.items[1].append(Directions.Direction(text="hello",placement="below"))
        self.lilystring = " c' _\\markup { hello  }"
        self.compile = True
        self.wrappers = ["\\new Staff {", "}"]
        Lily.setUp(self)
        self.name = "measurenotedirection"

class testMeasureSecondStave(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.staff_id = 2
        self.item.items[2] = []
        self.item.items[2].append(Note.Note())
        self.item.items[2][0].pitch = Note.Pitch()
        self.lilystring = " c'"
        self.compile = True
        self.wrappers = ["<<\\new Staff{}\\new Staff {", "}>>"]
        Lily.setUp(self)
        self.name = "measurenote"


