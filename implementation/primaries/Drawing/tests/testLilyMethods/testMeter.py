from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Meter

class testTimeSig(Lily):
    def setUp(self):
        self.item = Meter.Meter()
        self.lilystring = "\\time 4/4"

class testTimeSigBeat(Lily):
    def setUp(self):
        self.item = Meter.Meter(beats=2)
        self.lilystring = "\\time 2/4"

class testTimeSigType(Lily):
    def setUp(self):
        self.item = Meter.Meter(type=2)
        self.lilystring = "\\time 2/2"

class testTimeSigBeatAndType(Lily):
    def setUp(self):
        self.item = Meter.Meter(type=8, beats=6)
        self.lilystring = "\\time 6/8"

