from implementation.primaries.Drawing.classes import Measure, Note, Directions, Part
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testPart(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.lilystring = "<<>>"

class testPartMeasureWithNote(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].notes[1].append(Note.Note())
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.lilystring = "<<\\new Staff{c'}>>"

class testPartMultiStaves(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].addNote(Note.Note(),1)
        self.item.measures[1].addNote(Note.Note(),2)
        self.item.measures[1].notes[1][0].pitch = Note.Pitch()
        self.item.measures[1].notes[2][0].pitch = Note.Pitch()
        self.lilystring = "<<\\new Staff{c'}\\new Staff{c'}>>"

class testPartMultiBars(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.measures[1].addNote(Note.Note(),1)
        self.item.measures[1].items[1][0].pitch = Note.Pitch()
        self.item.measures[2] = Measure.Measure()
        self.item.measures[2].items[1].append(Note.Note())
        self.item.measures[2].items[1][0].pitch = Note.Pitch()
        self.lilystring = "<<\\new Staff{c'c'}>>"

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
        self.lilystring = "<<\\new Staff{c'c'}\\new Staff{c'}>>"

class testPartWithName(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.measures[1] = Measure.Measure()
        self.item.name = "charlotte"
        self.lilystring = "<<\\new Staff \with { \ninstrumentName = #\"charlotte \"\n}{}>>"