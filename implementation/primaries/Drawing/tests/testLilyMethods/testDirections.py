from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Directions


class testText(Lily):
    def setUp(self):
        self.item = Directions.Text()
        self.lilystring = ""

class testTextSize(Lily):
    def setUp(self):
        self.item = Directions.Text(size=8,text="hello")
        self.lilystring = "\markup { \\abs-fontsize #8 hello  }"

class testTextFont(Lily):
    def setUp(self):
        self.item = Directions.Text(font="typewriter",text="hello")
        self.lilystring = "\markup { \\typewriter hello  }"

class testBasicDirection(Lily):
    def setUp(self):
        self.item = Directions.Direction()
        self.lilystring = ""

class testDirectionPlacedBelow(Lily):
    def setUp(self):
        self.item = Directions.Direction(placement="below", text="hello")
        self.lilystring = "_\markup { hello  }"

class testDirectionPlacedAbove(Lily):
    def setUp(self):
        self.item = Directions.Direction(placement="above", text="hello")
        self.lilystring = "^\markup { hello  }"

class testDirectionWithText(Lily):
    def setUp(self):
        self.item = Directions.Direction(text="whatsup")
        self.lilystring = "\markup { whatsup  }"

class testDirectionFont(Lily):
    def setUp(self):
        self.item = Directions.Direction(font="calibri",text="lol")
        self.lilystring = "\markup { \calibri lol  }"

class testDirectionWithFontSize(Lily):
    def setUp(self):
        self.item = Directions.Direction(size=11,text="hello")
        self.lilystring = "\\markup { \\abs-fontsize #11 hello  }"

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
        self.lilystring = ["\\repeat percent 2 {","}"]

class testForwardWithDuration(Lily):
    def setUp(self):
        self.item = Directions.Forward(duration=4)
        self.lilystring = ["\\repeat percent 2 {","}"]

class testRepeatSign(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign()
        self.lilystring = "\mark "

class testSegno(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign(type="segno")
        self.lilystring = "\mark \markup { \musicglyph #\"scripts.segno\"  }"

class testCoda(Lily):
    def setUp(self):
        self.item = Directions.RepeatSign(type="coda")
        self.lilystring = "\mark \markup { \musicglyph #\"scripts.coda\"  }"

class testOctaveShift(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift()
        self.lilystring = "\n\ottava #0"

class testOctaveShiftUp(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift(amount=8)
        self.lilystring = "\ottava #1"

class testOctaveShiftDown(Lily):
    def setUp(self):
        self.item = Directions.OctaveShift(amount=-16)
        self.lilystring = "\ottava #-2"

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
        self.lilystring = ["On", "\n\\sustain"]

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
        self.lilystring = "\\tempo "

class testMetronomeBeat(Lily):
    def setUp(self):
        self.item = Directions.Metronome(beat=2)
        self.lilystring = "\\tempo 2="

class testMetronomeMin(Lily):
    def setUp(self):
        self.item = Directions.Metronome(min=60)
        self.lilystring = "\\tempo 60"

class testMetronomeBeatMin(Lily):
    def setUp(self):
        self.item = Directions.Metronome(beat=2,min=60)
        self.lilystring = "\\tempo 2=60"


class testMetronomeParenthesis(Lily):
    def setUp(self):
        self.item = Directions.Metronome(parentheses=True)
        self.lilystring = "\\tempo \"\" "

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

class testCreditText(Lily):
    def setUp(self):
        self.item = Directions.CreditText(text="hello")
        self.lilystring = "\markup { hello  }"


class testCreditTextX(Lily):
    def setUp(self):
        self.item = Directions.CreditText(x=100,text="hello")
        self.lilystring = "\markup { hello  }"

class testCreditTextY(Lily):
    def setUp(self):
        self.item = Directions.CreditText(y=100,text="hello")
        self.lilystring = "\markup { hello  }"

class testCreditTextVal(Lily):
    def setUp(self):
        self.item = Directions.CreditText(text="hello")
        self.lilystring = "\markup { hello  }"

class testCreditTextPage(Lily):
    def setUp(self):
        self.item = Directions.CreditText(page=1,text="hello")
        self.lilystring = "\markup { hello  }"


