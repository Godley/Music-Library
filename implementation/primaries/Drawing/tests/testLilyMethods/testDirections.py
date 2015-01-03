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
        self.lilystring = ["\repeat percent 2 {","}"]

class testForwardWithDuration(Lily):
    def setUp(self):
        self.item = Directions.Forward(duration=4)
        self.lilystring = ["\repeat percent 2 {","}"]

class testRepeatSign(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign()
        self.lilystring = "\mark \markup{\n  }"

class testSegno(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign(type="segno")
        self.lilystring = "\mark \markup{\n \musicglyph #\"scripts.segno\" }"

class testCoda(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign(type="coda")
        self.lilystring = "\mark \markup{\n \musicglyph #\"scripts.coda\" }"

class testOctaveShift(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift()
        self.lilystring = "/ottava #0"

class testOctaveShiftUp(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift(amount=8)
        self.lilystring = "/ottava #1"

class testOctaveShiftDown(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift(amount=-16)
        self.lilystring = "/ottava #-2"

class testWavyLine(Lily):
    def setUp(self):
        self.item = Directions.WavyLine()
        self.lilystring = "\startTrillSpan"

class testWavyLineStop(Lily):
    def setUp(self):
        self.item = Directions.WavyLine(type="stop")
        self.lilystring = "\stopTrillSpan"


class testPedal(Lily):
    def setUp(self):
        self.item = Directions.Pedal()
        self.lilystring = "\sustainOn"

class testPedalLine(Lily):
    def setUp(self):
        self.item = Directions.Pedal(line=True)
        self.lilystring = "\set Staff.pedalSustainStyle = #'mixed \n \sustainOn"

class testPedalType(Lily):
    def setUp(self):
        self.item = Directions.Pedal(type="start")
        self.lilystring = "\sustainOn"

class testPedalTypeOff(Lily):
    def setUp(self):
        self.item = Directions.Pedal(type="stop")
        self.lilystring = "\sustainOff"

# TODO: REFACTOR BRACKET CLASS ACCORDING TO LILYPOND NOTATION
class testBracket(Lily):
    def setUp(self):
        self.item = Directions.Bracket()
        self.lilystring = "\\alternative{}"

class testBracketlType(Lily):
    def setUp(self):
        self.item = Directions.Bracket(lineType="solid")
        self.lilystring = "what"

class testBracketendLength(Lily):
    def setUp(self):
        self.item = Directions.Bracket(endLength=1)
        self.lilystring = "what"

class testBracketlEnd(Lily):
    def setUp(self):
        self.item = Directions.Bracket(lineEnd="solid")
        self.lilystring = "what"

class testMetronome(Lily):
    def setUp(self):
        self.item = Directions.Metronome()
        self.lilystring = "\tempo "

class testMetronomeBeat(Lily):
    def setUp(self):
        self.item = Directions.Metronome(beat=2)
        self.lilystring = "\tempo 2 = "

class testMetronomeMin(Lily):
    def setUp(self):
        self.item = Directions.Metronome(min=60)
        self.lilystring = "\tempo 60"

class testMetronomeBeatMin(Lily):
    def setUp(self):
        self.item = Directions.Metronome(beat=2,min=60)
        self.lilystring = "\tempo 2 = 60"


class testMetronomeParenthesis(Lily):
    def setUp(self):
        self.item = Directions.Metronome(parentheses=True)
        self.lilystring = "\tempo \"\" "

class testDynamic(Lily):
    def setUp(self):
        self.item = Directions.Dynamic()
        self.lilystring = "\\"

class testDynamicMark(Lily):
    def setUp(self):
        self.item = Directions.Dynamic(mark="f")
        self.lilystring = "\\f"

class testWedge(Lily):
    def setUp(self):
        self.item = Directions.Wedge()
        self.lilystring = "\\"

class testWedgeType(Lily):
    def setUp(self):
        self.item = Directions.Wedge(type="crescendo")
        self.lilystring = "\<"

class testWedgeTypeDim(Lily):
    def setUp(self):
        self.item = Directions.Wedge(type="diminuendo")
        self.lilystring = "\>"

class testWedgeTypeStop(Lily):
    def setUp(self):
        self.item = Directions.Wedge(type="stop")
        self.lilystring = "\!"

class testSlur(Lily):
    def setUp(self):
        self.item = Directions.Slur()
        self.lilystring = ""

class testSlurStart(Lily):
    def setUp(self):
        self.item = Directions.Slur(type="start")
        self.lilystring = "("

class testSlurEnd(Lily):
    def setUp(self):
        self.item = Directions.Slur(type="stop")
        self.lilystring = ")"




