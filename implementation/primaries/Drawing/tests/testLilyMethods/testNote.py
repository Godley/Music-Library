from implementation.primaries.Drawing.classes import Note, Ornaments
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testNote(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.lilystring = ""
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]


class testNotePitch(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteDurationQuaver(Lily):
    def setUp(self):
        self.item = Note.Note(duration=2,divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'8"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteDurationMinim(Lily):
    def setUp(self):
        self.item = Note.Note(duration=8,divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'2"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]


class testNoteDurationSemiBreve(Lily):
    def setUp(self):
        self.item = Note.Note(duration=16,divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'1"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteDurationBreve(Lily):
    def setUp(self):
        self.item = Note.Note(duration=32,divisions=4)
        self.item.pitch = Note.Pitch()
        self.lilystring = "c'\\breve"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteRest(Lily):
    def setUp(self):
        self.item = Note.Note(duration=4,divisions=4,rest=True)
        self.item.pitch = Note.Pitch()
        self.lilystring = "r4"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteTuplet(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.timeMod = Note.TimeModifier(normal=2, actual=3)
        self.item.notations = [Note.Tuplet(type="start")]
        self.lilystring = "\\tuplet 3/2 {c'"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}}"]

class testNoteTupletEnd(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.timeMod = Note.TimeModifier(normal=2, actual=3)
        self.item.notations = [Note.Tuplet(type="stop")]
        self.lilystring = "c'}"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{\\tuplet 3/2 {","}"]

class testNoteStem(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.stem = Note.Stem("up")
        self.lilystring = "\stemUp\nc'"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteStemDown(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.stem = Note.Stem("down")
        self.lilystring = "\stemDown\nc'"

class testNoteBeam(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.beam = Note.Beam("start")
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","]}"]
        self.lilystring = "[c'"

class testNoteContinue(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.beam = Note.Beam("continue")
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{[c'","]}"]
        self.lilystring = "c'"

class testNoteStop(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.beam = Note.Beam("stop")
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{[","}"]
        self.lilystring = "c']"

class testNotehead(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notehead = Note.Notehead(type="diamond")
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]
        self.lilystring = "\harmonic c'"

class testGraceNote(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.grace = Note.GraceNote()
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]
        self.lilystring = "\grace c'"

class testNoteArpeggiate(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Note.Arpeggiate()]
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]
        self.lilystring = "\\arpeggioNormal\nc'\\arpeggio"

class testNoteNonArpeggiate(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Note.NonArpeggiate()]
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]
        self.lilystring = "\\arpeggioBracket\nc'\\arpeggio"

class testGliss(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Note.Glissando()]
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]
        self.lilystring = "\\override Glissando.style = #'zigzag\nc'\glissando"

class testSlide(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Note.Slide()]
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]
        self.lilystring = "c'\glissando"

class testSlideStop(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Note.Slide(type="stop")]
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]
        self.lilystring = "c'"

class testNoteMordent(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Ornaments.Mordent()]
        self.lilystring = "c'\mordent"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteInvMordent(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Ornaments.InvertedMordent()]
        self.lilystring = "c'\prall"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteTrill(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Ornaments.Trill()]
        self.lilystring = "c'\\trill"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteTurn(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Ornaments.Turn()]
        self.lilystring = "c'\\turn"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteInvTurn(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Ornaments.InvertedTurn()]
        self.lilystring = "c'\\reverseturn"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

class testNoteTremolo(Lily):
    def setUp(self):
        self.item = Note.Note()
        self.item.pitch = Note.Pitch()
        self.item.notations = [Ornaments.Tremolo()]
        self.lilystring = "\\repeat tremolo c'"
        Lily.setUp(self)
        self.compile = True
        self.wrappers = ["\\new Staff{","}"]

