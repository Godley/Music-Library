from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Harmony

class testHarmony(Lily):
    def setUp(self):
        self.item = Harmony.Harmony()
        self.lilystring = "\chords {\n\r}"

class testHarmonyRoot(Lily):
    def setUp(self):
        self.item = Harmony.Harmony(root="G")
        self.lilystring = "\chords {\n\rG\n\r}"

class testHarmonyBass(Lily):
    def setUp(self):
        self.item = Harmony.Harmony(bass="F")
        self.lilystring = "\chords {\n\r:/F\n\r}"

class testDegree(Lily):
    def setUp(self):
        self.item = Harmony.Degree()
        self.lilystring = ""

class testDegreeAlter(Lily):
    def setUp(self):
        self.item = Harmony.Degree(alter=1)
        self.lilystring = ""

class testDegreeValue(Lily):
    def setUp(self):
        self.item = Harmony.Degree(value=1)
        self.lilystring = "1"

class testDegreeType(Lily):
    def setUp(self):
        self.item = Harmony.Degree(type="subtract")
        self.lilystring = "no "

class testDegreeAdd(Lily):
    def setUp(self):
        self.item = Harmony.Degree(type="add")
        self.lilystring = "add "

class testDegreeTypeAlter(Lily):
    def setUp(self):
        self.item = Harmony.Degree(type="alter")
        self.lilystring = "#"


class testKindDegree(Lily):
    def setUp(self):
        self.item = Harmony.Harmony()
        self.item.kind = Harmony.Kind(parenthesis=True)
        self.item.degrees.append(Harmony.Degree(value=3))
        self.lilystring = "\\chords {\n\r:(3)\n\r}"


class testHarmonyDegrees(Lily):
    def setUp(self):
        self.item = Harmony.Harmony()
        self.item.degrees.append(Harmony.Degree())
        self.lilystring = "\chords {\n\r:\n\r}"

class testHarmonyKind(Lily):
    def setUp(self):
        self.item = Harmony.Harmony()
        self.item.kind = Harmony.Kind()
        self.lilystring = "\chords {\n\r:\n\r}"

class testKind(Lily):
    def setUp(self):
        self.item = Harmony.Kind()
        self.lilystring = ""

class testKindVal(Lily):
    def setUp(self):
        self.item = Harmony.Kind(value=1)
        self.lilystring = "1"

class testKindText(Lily):
    def setUp(self):
        self.item = Harmony.Kind(text="3")
        self.lilystring = "3"

class testKindTextOverridesVal(Lily):
    def setUp(self):
        self.item = Harmony.Kind(text="3",value=2)
        self.lilystring = "3"

