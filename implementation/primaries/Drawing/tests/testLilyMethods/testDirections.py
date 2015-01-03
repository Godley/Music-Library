from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Directions

class testBasicDirection(Lily):
    def setUp(self):
        self.item = Directions.Direction()
        self.lilystring = "\markup{\n  }"

class testDirectionPlacedBelow(Lily):
    def setUp(self):
        self.item = Directions.Direction(placement="below")
        self.lilystring = "_\markup{\n  }"

class testDirectionPlacedAbove(Lily):
    def setUp(self):
        self.item = Directions.Direction(placement="above")
        self.lilystring = "^\markup{\n  }"

class testDirectionWithText(Lily):
    def setUp(self):
        self.item = Directions.Direction(text="whatsup")
        self.lilystring = "\markup{\n whatsup }"

class testDirectionFont(Lily):
    def setUp(self):
        self.item = Directions.Direction(font="calibri")
        self.lilystring = "\\override Voice.TextScript.font-family = #'calibri\n\\markup{\n  }"

class testDirectionWithFontSize(Lily):
    def setUp(self):
        self.item = Directions.Direction(size=11)
        self.lilystring = "\\override Voice.TextScript.font-size = #1\n\\markup{\n  }"

class testRehearsalMark(Lily):
    def setUp(self):
        self.item = Directions.RehearsalMark()
        self.lilystring = "\mark \default"

class testRehearsalMarkWithText(Lily):
    def setUp(self):
        self.item = Directions.RehearsalMark(text="B")
        self.lilystring = "\mark #2"


class testForward(Lily):
    def setUp(self):
        self.item = Directions.Forward()
        self.lilystring = "what"

class testForwardWithDuration(Lily):
    def setUp(self):
        self.item = Directions.Forward(duration=4)
        self.lilystring = "what"

class testRepeatSign(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign()
        self.lilystring = "what"

class testSegno(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign(type="segno")
        self.lilystring = "what"

class testCoda(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign(type="coda")
        self.lilystring = "what"

class testOctaveShift(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift()
        self.lilystring = "what"

class testOctaveShiftUp(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift(amount=8)
        self.lilystring = "what"

class testOctaveShiftDown(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift(amount=16)
        self.lilystring = "what"

class testWavyLine(Lily):
    def setUp(self):
        self.item = Directions.WavyLine()
        self.lilystring = "what"


class testPedal(Lily):
    def setUp(self):
        self.item = Directions.Pedal()
        self.lilystring = "what"

class testPedalLine(Lily):
    def setUp(self):
        self.item = Directions.Pedal(line=True)
        self.lilystring = "what"

class testBracket(Lily):
    def setUp(self):
        self.item = Directions.Bracket()
        self.lilystring = "what"

class testBracketNumber(Lily):
    def setUp(self):
        self.item = Directions.Pedal(number=1)
        self.lilystring = "what"

class testBracketlType(Lily):
    def setUp(self):
        self.item = Directions.Pedal(lineType="solid")
        self.lilystring = "what"

class testBracketendLength(Lily):
    def setUp(self):
        self.item = Directions.Pedal(endLength=1)
        self.lilystring = "what"

class testBracketlEnd(Lily):
    def setUp(self):
        self.item = Directions.Pedal(lineEnd="solid")
        self.lilystring = "what"

class testMetronome(Lily):
    def setUp(self):
        self.item = Directions.Metronome()
        self.lilystring = "wh"

class testMetronomeBeat(Lily):
    def setUp(self):
        self.item = Directions.Metronome(beat=2)
        self.lilystring = "wh"

class testMetronomeMin(Lily):
    def setUp(self):
        self.item = Directions.Metronome(min=4)
        self.lilystring = "wh"

class testMetronomeBeatMin(Lily):
    def setUp(self):
        self.item = Directions.Metronome(beat=2,min=4)
        self.lilystring = "wh"


class testMetronomeParenthesis(Lily):
    def setUp(self):
        self.item = Directions.Metronome(parentheses=True)
        self.lilystring = "wh"

class testDynamic(Lily):
    def setUp(self):
        self.item = Directions.Dynamic()
        self.lilystring = "wh"

class testDynamicMark(Lily):
    def setUp(self):
        self.item = Directions.Dynamic(mark="f")
        self.lilystring = "wh"

class testWedge(Lily):
    def setUp(self):
        self.item = Directions.Wedge()
        self.lilystring = "wh"

class testWedgeType(Lily):
    def setUp(self):
        self.item = Directions.Wedge(type="crescendo")
        self.lilystring = "wh"


class testSlur(Lily):
    def setUp(self):
        self.item = Directions.Slur()
        self.lilystring = "wh"




