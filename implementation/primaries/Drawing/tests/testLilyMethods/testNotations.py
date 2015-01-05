from implementation.primaries.Drawing.classes import Note
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testTie(Lily):
    def setUp(self):
        self.item = Note.Tie(None)
        self.lilystring = "~"

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
        self.lilystring = "\\"

class testNoteheadFilled(Lily):
    def setUp(self):
        self.item = Note.Notehead(filled=True)
        self.lilystring = "\\"

class testNoteheadType(Lily):
    def setUp(self):
        self.item = Note.Notehead(type="diamond")
        self.lilystring = "\harmonic"

class testNoteheadCross(Lily):
    def setUp(self):
        self.item = Note.Notehead(type="x")
        self.lilystring = "\\xNote"

class testStem(Lily):
    def setUp(self):
        self.item = Note.Stem(None)
        self.lilystring = "\stemNeutral"

class testStemUp(Lily):
    def setUp(self):
        self.item = Note.Stem("up")
        self.lilystring = "\stemUp"

class testStemDown(Lily):
    def setUp(self):
        self.item = Note.Stem("down")
        self.lilystring = "\stemDown"

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
        self.item = Note.GraceNote()
        self.lilystring = "\grace"

class testGraceNoteSlash(Lily):
    def setUp(self):
        self.item = Note.GraceNote(slash=True)
        self.lilystring = "\slashedGrace"

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

class testBeam(Lily):
    def setUp(self):
        self.item = Note.Beam(None)
        self.lilystring = "\\autoBeamOn"

class testBeamStart(Lily):
    def setUp(self):
        self.item = Note.Beam("start")
        self.lilystring = "["

class testBeamStop(Lily):
    def setUp(self):
        self.item = Note.Beam("stop")
        self.lilystring = "]"
