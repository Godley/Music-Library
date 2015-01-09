from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Ornaments

class testMordent(Lily):
    def setUp(self):
        self.item =Ornaments.Mordent()
        self.lilystring = "\mordent"

class testInvertedMordent(Lily):
    def setUp(self):
        self.item =Ornaments.InvertedMordent()
        self.lilystring = "\prall"

class testTrill(Lily):
    def setUp(self):
        self.item =Ornaments.Trill()
        self.lilystring = "\\trill"

class testTurn(Lily):
    def setUp(self):
        self.item =Ornaments.Turn()
        self.lilystring = "\\turn"

class testInvertedTurn(Lily):
    def setUp(self):
        self.item =Ornaments.InvertedTurn()
        self.lilystring = "\\reverseturn"

class testTremolo(Lily):
    def setUp(self):
        self.item =Ornaments.Tremolo()
        self.lilystring = "\\repeat tremolo "

class testTremoloType(Lily):
    def setUp(self):
        self.item =Ornaments.Tremolo(type="single")
        self.lilystring = "\\repeat tremolo 8 "

class testTremoloVal(Lily):
    def setUp(self):
        self.item =Ornaments.Tremolo(value=2)
        self.lilystring = "\\repeat tremolo 16 "

class testTremoloTypeStart(Lily):
    def setUp(self):
        self.item =Ornaments.Tremolo(type="start")
        self.lilystring = "\\repeat tremolo {"

class testTremoloTypeStop(Lily):
    def setUp(self):
        self.item =Ornaments.Tremolo(type="stop")
        self.lilystring = "}"