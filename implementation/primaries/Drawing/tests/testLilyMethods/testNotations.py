from implementation.primaries.Drawing.classes import Note
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testTie(Lily):
    def setUp(self):
        self.item = Note.Tie(None)
        self.lilystring = ""

class testTieStart(Lily):
    def setUp(self):
        self.item = Note.Tie("start")
        self.lilystring = "~"

class testTieStop(Lily):
    def setUp(self):
        self.item = Note.Tie("stop")
        self.lilystring = ""

class testNotehead(Lily):
    def setUp(self):
        self.item = Note.Notehead()
        self.lilystring = ["","\\revert NoteHead.style"]

class testNoteheadCircleX(Lily):
    def setUp(self):
        self.item = Note.Notehead(type="circle-x")
        self.lilystring = ["\\override NoteHead.style = #'xcircle", "\\revert NoteHead.style"]

class testNoteheadType(Lily):
    def setUp(self):
        self.item = Note.Notehead(type="diamond")
        self.lilystring = ["\\override NoteHead.style = #'harmonic", "\\revert NoteHead.style"]

class testNoteheadCross(Lily):
    def setUp(self):
        self.item = Note.Notehead(type="x")
        self.lilystring = ["\\override NoteHead.style = #'cross", "\\revert NoteHead.style"]

class testStem(Lily):
    def setUp(self):
        self.item = Note.Stem(None)
        self.lilystring = "\n\stemNeutral"

class testStemUp(Lily):
    def setUp(self):
        self.item = Note.Stem("up")
        self.lilystring = "\n\stemUp"

class testStemDown(Lily):
    def setUp(self):
        self.item = Note.Stem("down")
        self.lilystring = "\n\stemDown"

class testTuplet(Lily):
    def setUp(self):
        self.item = Note.Tuplet()
        self.lilystring = "\\tuplet"

class testTupletType(Lily):
    def setUp(self):
        self.item = Note.Tuplet(type="start")
        self.lilystring = "\\tuplet"

class testTupletStop(Lily):
    def setUp(self):
        self.item = Note.Tuplet(type="stop")
        self.lilystring = "}"

class testTupletBracket(Lily):
    def setUp(self):
        self.item = Note.Tuplet(bracket=True)
        self.lilystring = "\override TupletBracket.bracket-visibility = ##t\n\\tuplet"

class testTupletBracketNone(Lily):
    def setUp(self):
        self.item = Note.Tuplet(bracket=False)
        self.lilystring = "\override TupletBracket.bracket-visibility = ##f\n\\tuplet"


class testGraceNote(Lily):
    def setUp(self):
        self.item = Note.GraceNote(first=True)
        self.lilystring = "\\grace {"

class testGraceNoteSlash(Lily):
    def setUp(self):
        self.item = Note.GraceNote(slash=True, first=True)
        self.lilystring = "\slashedGrace {"

class testTimeMod(Lily):
    def setUp(self):
        self.item = Note.TimeModifier()
        self.lilystring = "/"

class testTimeModNormal(Lily):
    def setUp(self):
        self.item = Note.TimeModifier(normal=3)
        self.lilystring = "/3"

class testTimeModActual(Lily):
    def setUp(self):
        self.item = Note.TimeModifier(actual=3)
        self.lilystring = "3/"

class testTimeModNormalActual(Lily):
    def setUp(self):
        self.item = Note.TimeModifier(normal=2, actual=3)
        self.lilystring = "3/2"

class testArpeggiate(Lily):
    def setUp(self):
        self.item = Note.Arpeggiate()
        self.lilystring = ["\\arpeggioNormal","\\arpeggio"]

class testArpeggiateDir(Lily):
    def setUp(self):
        self.item = Note.Arpeggiate(direction="up")
        self.lilystring = ["\\arpeggioArrowUp","\\arpeggio"]

class testArpeggiateDirDown(Lily):
    def setUp(self):
        self.item = Note.Arpeggiate(direction="down")
        self.lilystring = ["\\arpeggioArrowDown","\\arpeggio"]

class testNonArpeggiate(Lily):
    def setUp(self):
        self.item = Note.NonArpeggiate()
        self.lilystring = ["\\arpeggioBracket","\\arpeggio"]


class testSlide(Lily):
    def setUp(self):
        self.item = Note.Slide()
        self.lilystring = ["\glissando"]

class testSlideType(Lily):
    def setUp(self):
        self.item = Note.Slide(type="start")
        self.lilystring = ["\glissando"]

class testSlideStop(Lily):
    def setUp(self):
        self.item = Note.Slide(type="stop")
        self.lilystring = []

class testSlideLineType(Lily):
    def setUp(self):
        self.item = Note.Slide(lineType="wavy")
        self.lilystring = ["\override Glissando.style = #'zigzag","\glissando"]

class testGliss(Lily):
    def setUp(self):
        self.item = Note.Glissando()
        self.lilystring = ["\override Glissando.style = #'zigzag","\glissando"]

class testGlissType(Lily):
    def setUp(self):
        self.item = Note.Glissando(type="start")
        self.lilystring = ["\override Glissando.style = #'zigzag","\glissando"]

class testGlissStop(Lily):
    def setUp(self):
        self.item = Note.Glissando(type="stop")
        self.lilystring = []

class testBeamStart(Lily):
    def setUp(self):
        self.item = Note.Beam("begin")
        self.lilystring = "["

class testBeamStop(Lily):
    def setUp(self):
        self.item = Note.Beam("end")
        self.lilystring = "]"
