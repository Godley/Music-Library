from implementation.primaries.Drawing.classes import Note, Directions, Part
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testPartMeasureWithNote(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.addEmptyMeasure(1,1)
        self.item.getMeasure(measure=1,staff=1).notes.append(Note.Note())
        self.item.getMeasure(measure=1,staff=1).notes[0].pitch = Note.Pitch()
        self.lilystring = (["Sone = \\new Staff{\\autoBeamOff % measure 1\n c' | }\n\n"], '\\Sone')

class testPartMultiStavesWithName(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.name = "Piano"
        self.item.addEmptyMeasure(1,1)
        self.item.addEmptyMeasure(1,2)
        self.item.getMeasure(measure=1,staff=1).addNote(Note.Note())
        self.item.getMeasure(measure=1,staff=2).addNote(Note.Note())
        self.item.getMeasure(measure=1,staff=1).notes[0].pitch = Note.Pitch()
        self.item.getMeasure(measure=1,staff=2).notes[0].pitch = Note.Pitch()
        self.lilystring = (["pianoSone = \\new Staff{\\autoBeamOff % measure 1\n c' | }\n\n", "pianoStwo = \\new Staff{\\autoBeamOff % measure 1\n c' | }\n\n"], "\\new StaffGroup \\with { \ninstrumentName = #\"Piano \"\n} <<\pianoSone\n\pianoStwo>>")


class testPartMultiStaves(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.addEmptyMeasure(1,1)
        self.item.addEmptyMeasure(1,2)
        self.item.getMeasure(measure=1,staff=1).addNote(Note.Note())
        self.item.getMeasure(measure=1,staff=2).addNote(Note.Note())
        self.item.getMeasure(measure=1,staff=1).notes[0].pitch = Note.Pitch()
        self.item.getMeasure(measure=1,staff=2).notes[0].pitch = Note.Pitch()
        self.lilystring = (["Sone = \\new Staff{\\autoBeamOff % measure 1\n c' | }\n\n", "Stwo = \\new Staff{\\autoBeamOff % measure 1\n c' | }\n\n"], "\\new StaffGroup <<\Sone\n\Stwo>>")

class testPartMultiBars(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.addEmptyMeasure(1,1)
        self.item.getMeasure(measure=1,staff=1).addNote(Note.Note())
        self.item.getMeasure(measure=1,staff=1).notes[0].pitch = Note.Pitch()
        self.item.addEmptyMeasure(2,1)
        self.item.getMeasure(measure=2,staff=1).addNote(Note.Note())
        self.item.getMeasure(measure=2,staff=1).notes[0].pitch = Note.Pitch()
        self.lilystring = (["Sone = \\new Staff{\\autoBeamOff % measure 1\n c' | \n\n% measure 2\n c' | }\n\n"],"\\Sone")

class testPartMultiBarsStaves(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.addEmptyMeasure(1,1)
        self.item.getMeasure(measure=1,staff=1).addNote(Note.Note())
        self.item.getMeasure(measure=1,staff=1).notes[0].pitch = Note.Pitch()
        self.item.addEmptyMeasure(1,2)
        self.item.getMeasure(measure=1,staff=2).addNote(Note.Note())
        self.item.getMeasure(measure=1,staff=2).notes[0].pitch = Note.Pitch()
        self.item.addEmptyMeasure(2,1)
        self.item.getMeasure(measure=2,staff=1).addNote(Note.Note())
        self.item.getMeasure(measure=2,staff=1).notes[0].pitch = Note.Pitch()
        self.lilystring = (["Sone = \\new Staff{\\autoBeamOff % measure 1\n c' | \n\n% measure 2\n c' | }\n\n", "Stwo = \\new Staff{\\autoBeamOff % measure 1\n c' | }\n\n"], "\\new StaffGroup <<\\Sone\n\\Stwo>>")

class testPartWithName(Lily):
    def setUp(self):
        self.item = Part.Part()
        self.item.addEmptyMeasure(1,1)
        self.item.name = "charlotte"
        self.lilystring = (["charlotteSone = \\new Staff \with {\ninstrumentName = #\"charlotte \"\n }{\\autoBeamOff % measure 1\n r | }\n\n"], "\charlotteSone")