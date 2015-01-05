from implementation.primaries.Drawing.classes import Note
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testNote(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.lilystring = ""

class testNotePitch(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'"

class testNoteDurationQuaver(Lily):
    def setUp(self):
        self.item = Note.Note(duration=2,divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'8"

class testNoteDurationMinim(Lily):
    def setUp(self):
        self.item = Note.Note(duration=8,divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'2"


class testNoteDurationSemiBreve(Lily):
    def setUp(self):
        self.item = Note.Note(duration=16,divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'1"

class testNoteDurationBreve(Lily):
    def setUp(self):
        self.item = Note.Note(duration=32,divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'\\breve"

class testNoteRest(Lily):
    def setUp(self):
        self.item = Note.Note(duration=4,divisions=4,rest=True)
        self.item.pitch = Note.Pitch()
        self.lilystring = "r4"