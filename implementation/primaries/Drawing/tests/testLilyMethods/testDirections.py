from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Directions

class testBasicDirection(Lily):
    def setUp(self):
        self.item = Directions.Direction()
        self.lilystring = ""

class testDirectionPlacedBelow(Lily):
    def setUp(self):
        self.item = Directions.Direction(placement="below")
        self.lilystring = "something else"

class testDirectionPlacedAbove(Lily):
    def setUp(self):
        self.item = Directions.Direction(placement="above")
        self.lilystring = "hello world"

class testDirectionWithText(Lily):
    def setUp(self):
        self.item = Directions.Direction(text="whatsup")
        self.lilystring = "something else"

class testDirectionFont(Lily):
    def setUp(self):
        self.item = Directions.Direction(font="calibri")
        self.lilystring = "calibrid"

class testDirectionWithFontSize(Lily):
    def setUp(self):
        self.item = Directions.Direction(size="what")
        self.lilystring = "what"

class testRehearsalMark(Lily):
    def setUp(self):
        self.item = Directions.RehearsalMark()
        self.lilystring = "what"

class testRehearsalMarkWithText(Lily):
    def setUp(self):
        self.item = Directions.RehearsalMark(text="B")
        self.lilystring = "what"


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





