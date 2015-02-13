from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.tests.testLilyMethods.testMeasure import MeasureTests
from implementation.primaries.Drawing.classes import Measure, Note

class testNormalBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline()
        self.lilystring = " \\bar \"|\""

class testDottedBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="dotted")
        self.lilystring = " \\bar \";\""

class testDashedBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="dashed")
        self.lilystring = " \\bar \"!\""

class testHeavyLightBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-light")
        self.lilystring = " \\bar \".|\""

class testLightHeavyBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-heavy")
        self.lilystring = " \\bar \"|.\""

class testLightLightBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-light")
        self.lilystring = " \\bar \"||\""

class testHeavyHeavyBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-heavy")
        self.lilystring = " \\bar \"..\""

class testForwardRepeat(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-light", repeat="forward")
        self.lilystring = " \\repeat volta 2 {"

class testBackwardRepeat(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-heavy", repeat="backward")
        self.lilystring = "}"

class testEndingMark(Lily):
    def setUp(self):
        self.item = Measure.EndingMark()
        self.lilystring = "}\n\\alternative {\n{"

class testEndingMark2(Lily):
    def setUp(self):
        self.item = Measure.EndingMark(number=2)
        self.lilystring = "{"

class testEndingMarkEnd(Lily):
    def setUp(self):
        self.item = Measure.EndingMark(type="stop")
        self.lilystring = "}\n"

class testBarlineWithEndingStart(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-light",ending=Measure.EndingMark())
        self.lilystring = "}\n\\alternative {\n{"

class testMeasureLeftBarline(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.addNote(Note.Note())
        self.item.notes[-1].pitch = Note.Pitch()
        self.item.barlines = {}
        self.item.barlines["left"] = Measure.Barline(repeat="forward")
        self.lilystring = " \\repeat volta 2 { c'"

class testMeasureRightBarline(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.addNote(Note.Note())
        self.item.notes[-1].pitch = Note.Pitch()
        self.item.AddBarline("left", Measure.Barline(repeat="forward"))
        self.item.AddBarline("right",Measure.Barline(repeat="backward"))
        self.lilystring = " \\repeat volta 2 { c'}"


class testMeasureRightRepeatBarlineNoLeft(MeasureTests):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.addNote(Note.Note())
        self.item.notes[-1].pitch = Note.Pitch()
        self.item.AddBarline("right", Measure.Barline(repeat="backward-barline"))
        self.lilystring = " c' \\bar \":|.\""