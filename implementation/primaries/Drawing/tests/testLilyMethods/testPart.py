from implementation.primaries.Drawing.classes import Measure, Note, Directions, Part
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testPartMeasureWithNote(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].notes[1].append(Note.Note())
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.lilystring = "\\new Staff{ c'}"

class testPartMultiStaves(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].addNote(Note.Note(),1)
        self.item.measures[1].addNote(Note.Note(),2)
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.item.measures[1].notes[2][0].pitch = Note.Pitch()
        self.lilystring = "\\new StaffGroup <<\\new Staff{ c'}\\new Staff{ c'}>>"

class testPartMultiBars(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].addNote(Note.Note(),1)
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.item.measures[2] = Measure.Measure()
        self.item.measures[2].addNote(Note.Note(), 1)
        self.item.measures[2].notes[1][0].pitch = Note.Pitch()
        self.lilystring = "\\new Staff{ c' c'}"

class testPartForwardRepeats(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].addNote(Note.Note(duration=4),1)
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.item.measures[2] = Measure.Measure()
        self.item.measures[2].forwards[1] = {}
        self.item.measures[2].forwards[1][0] = Directions.Forward(duration=4)
        self.lilystring = "\\new Staff{ \\repeat percent 2 { c'1}}"

class testPartTwoForwardRepeats(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].addNote(Note.Note(duration=4),1)
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.item.measures[2] = Measure.Measure()
        self.item.measures[2].forwards[1] = {}
        self.item.measures[2].forwards[1][0] = Directions.Forward(duration=4)
        self.item.measures[3] = Measure.Measure()
        self.item.measures[3].forwards[1] = {}
        self.item.measures[3].forwards[1][0] = Directions.Forward(duration=4)
        self.lilystring = "\\new Staff{ \\repeat percent 3 { c'1}}"

class testPartTwoNotesOneForward(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].addNote(Note.Note(duration=2),1)
        self.item.measures[1].addNote(Note.Note(duration=2),1)
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.item.measures[1].notes[1][1].pitch = Note.Pitch()
        self.item.measures[2] = Measure.Measure()
        self.item.measures[2].forwards[1] = {}
        self.item.measures[2].forwards[1][0] = Directions.Forward(duration=2)
        self.lilystring = "\\new Staff{ c'2 \\repeat percent 2 { c'2}}"

class testPartMultiBarsStaves(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].addNote(Note.Note(),1)
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.item.measures[1].addNote(Note.Note(),2)
        self.item.measures[1].notes[2][0].pitch = Note.Pitch()
        self.item.measures[2] = Measure.Measure()
        self.item.measures[2].addNote(Note.Note(),1)
        self.item.measures[2].notes[1][0].pitch = Note.Pitch()
        self.lilystring = "\\new StaffGroup <<\\new Staff{ c' c'}\\new Staff{ c'}>>"

class testPartWithName(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.name = "charlotte"
        self.lilystring = "\\new Staff \with { \ninstrumentName = #\"charlotte \"\n}{r}"