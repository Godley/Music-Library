from implementation.primaries.Drawing.classes import Note, Part
from implementation.primaries.Drawing.classes.tree_cls.PieceTree import PartNode, MeasureNode
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testPartMeasureWithNote(Lily):
    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1,1)
        measure = self.item.getMeasure(1,1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        measure.addNote(note)
        self.lilystring = ["staffone = \\new Staff{\\autoBeamOff % measure 1\n % voice 1\n{ c' } | \n\n }\n\n", '\\staffone']

class testPartMultistafftavesWithName(Lily):
    def setUp(self):
        self.item = PartNode()
        self.item.GetItem().name = "Piano"
        self.item.addEmptyMeasure(1,1)
        measure = self.item.getMeasure(1,1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        measure.addNote(note)
        self.item.addEmptyMeasure(1,2)
        measure2 = self.item.getMeasure(1,2)
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        measure2.addNote(note2)
        self.lilystring = ["pianostaffone = \\new Staff{\\autoBeamOff % measure 1\n % voice 1\n{ c' } | \n\n }\n\npianostafftwo = \\new Staff{\\autoBeamOff % measure 1\n % voice 1\n{ c' } | \n\n }\n\n", "\\new StaffGroup \\with {\ninstrumentName = #\"Piano \"\n }<<\pianostaffone\n\pianostafftwo>>"]

class testPartMultistafftaves(Lily):
    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1,1)
        self.item.addEmptyMeasure(1,2)
        measure1 = self.item.getMeasure(1,1)
        measure2 = self.item.getMeasure(1,2)
        note1 = Note.Note()
        note1.pitch = Note.Pitch()
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        measure1.addNote(note1)
        measure2.addNote(note2)
        self.lilystring = ["staffone = \\new Staff{\\autoBeamOff % measure 1\n % voice 1\n{ c' } | \n\n }\n\nstafftwo = \\new Staff{\\autoBeamOff % measure 1\n % voice 1\n{ c' } | \n\n }\n\n", "\\new StaffGroup <<\staffone\n\stafftwo>>"]

class testPartMultiBars(Lily):
    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1,1)
        self.item.addEmptyMeasure(2,1)
        measure2 = self.item.getMeasure(2,1)
        measure = self.item.getMeasure(1,1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        measure.addNote(note)
        measure2.addNote(note2)
        self.lilystring = ["staffone = \\new Staff{\\autoBeamOff % measure 1\n % voice 1\n{ c' } | \n\n % measure 2\n % voice 1\n{ c' } | \n\n }\n\n","\\staffone"]

class testPartMultiBarsstafftaves(Lily):
    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1,1)
        measure = self.item.getMeasure(1,1)
        note = Note.Note()
        note.pitch = Note.Pitch()
        measure.addNote(note)
        self.item.addEmptyMeasure(1,2)
        measure2 = self.item.getMeasure(1,2)
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        measure2.addNote(note2)
        self.item.addEmptyMeasure(2,1)
        measure3 = self.item.getMeasure(2,1)
        note3 = Note.Note()
        note3.pitch = Note.Pitch()
        measure3.addNote(note3)
        self.lilystring = ["staffone = \\new Staff{\\autoBeamOff % measure 1\n % voice 1\n{ c' } | \n\n % measure 2\n % voice 1\n{ c' } | \n\n }\n\nstafftwo = \\new Staff{\\autoBeamOff % measure 1\n % voice 1\n{ c' } | \n\n }\n\n", "\\new StaffGroup <<\\staffone\n\\stafftwo>>"]

class testPartWithName(Lily):
    def setUp(self):
        self.item = PartNode()
        self.item.addEmptyMeasure(1,1)
        self.item.GetItem().name = "charlotte"
        self.lilystring = ["charlottestaffone = \\new Staff \with {\ninstrumentName = #\"charlotte \"\n }{\\autoBeamOff % measure 1\n | \n\n }\n\n", "\charlottestaffone"]