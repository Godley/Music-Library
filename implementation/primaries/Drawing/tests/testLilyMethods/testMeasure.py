from implementation.primaries.Drawing.classes import Measure
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testMeasure(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.lilystring = "\\new Staff {}"

class testMeasureStaves(Lily):
    def setUp(self):
        self.item = Measure.Measure()
        self.item.items[2] = []
        self.lilystring = "\\new PianoStaff <<\n \\new Staff {} \n \\new Staff {} \n>>"

