from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Note

class testPitch(Lily):
    def setUp(self):
        self.item = Note.Pitch()
        self.lilystring = "\\absolute c1"

class testPitchAlter(Lily):
    def setUp(self):
        self.item = Note.Pitch(alter=1)
        self.lilystring = "\\absolute cis1"

class testPitchOctave(Lily):
    def setUp(self):
        self.item = Note.Pitch(octave=1)
        self.lilystring = "\\absolute c1"

class testPitchStep(Lily):
    def setUp(self):
        self.item = Note.Pitch(step="A")
        self.lilystring = "\\absolute a1"

class testPitchDubSharp(Lily):
    def setUp(self):
        self.item = Note.Pitch(accidental="double-sharp")
        self.lilystring = "\\absolute cisis1"

class testPitchDubFlat(Lily):
    def setUp(self):
        self.item = Note.Pitch(accidental="flat-flat")
        self.lilystring = "\\absolute ceses1"

class testPitchNatural(Lily):
    def setUp(self):
        self.item = Note.Pitch(accidental="natural")
        self.lilystring = "\\absolute c1"

class testPitchQuarterFlat(Lily):
    def setUp(self):
        self.item = Note.Pitch(accidental="quarter-flat")
        self.lilystring = "\\absolute ceh1"

class testPitchThreeQuarterFlat(Lily):
    def setUp(self):
        self.item = Note.Pitch(accidental="three-quarters-flat")
        self.lilystring = "\\absolute ceseh1"

class testPitchQuarterSharp(Lily):
    def setUp(self):
        self.item = Note.Pitch(accidental="quarter-sharp")
        self.lilystring = "\\absolute cih1"

class testPitchThreeQuarterSharp(Lily):
    def setUp(self):
        self.item = Note.Pitch(accidental="three-quarters-sharp")
        self.lilystring = "\\absolute cisih1"
