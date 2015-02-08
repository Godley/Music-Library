from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Measure

class testNormalBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline()
        self.lilystring = "\\bar \"|\""

class testDottedBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="dotted")
        self.lilystring = "\\bar \";\""

class testDashedBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="dashed")
        self.lilystring = "\\bar \"!\""

class testHeavyLightBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-light")
        self.lilystring = "\\bar \".|\""

class testLightHeavyBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-heavy")
        self.lilystring = "\\bar \"|.\""

class testLightLightBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-light")
        self.lilystring = "\\bar \"||\""

class testHeavyHeavyBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-heavy")
        self.lilystring = "\\bar \"..\""

class testForwardRepeat(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-light", repeat="forward")
        self.lilystring = "\\bar \".|:\""

class testBackwardRepeat(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-heavy", repeat="backward")
        self.lilystring = "\\bar \":|.\""

class testEndingMark(Lily):
    def setUp(self):
        self.item = Measure.EndingMark()
        self.lilystring = "\\alternative {{"

class testEndingMark2(Lily):
    def setUp(self):
        self.item = Measure.EndingMark(number=2)
        self.lilystring = "{"

class testEndingMarkEnd(Lily):
    def setUp(self):
        self.item = Measure.EndingMark(type="stop")
        self.lilystring = "}"