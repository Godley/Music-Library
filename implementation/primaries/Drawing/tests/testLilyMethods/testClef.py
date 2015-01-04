from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Clef

#clef_type = {"G2": "treble", "G1": "french", "F4": "bass", "F3": "baritone", "F": "sub-bass", "C3": "alto",
             #"C4": "tenor", "C5": "Baritone on C", "C2": "mezzo-soprano", "C1": "soprano"}

'''
\clef GG
 [image of music]

\clef tenorG
 [image of music]

\clef soprano
 [image of music]

\clef mezzosoprano
 [image of music]

\clef C
 [image of music]

\clef alto
 [image of music]

\clef tenor
 [image of music]

\clef baritone
 [image of music]

\clef varC
 [image of music]

\clef altovarC
 [image of music]

\clef tenorvarC
 [image of music]

\clef baritonevarC
 [image of music]

\clef varbaritone
 [image of music]

\clef baritonevarF
 [image of music]

\clef F
 [image of music]

\clef bass
 [image of music]

\clef subbass
 [image of music]

\clef percussion
 [image of music]

\new TabStaff {
  \clef tab
}
 [image of music]

\new TabStaff {
  \clef moderntab
}'''

class testClef(Lily):
    def setUp(self):
        self.item = Clef.Clef()
        self.lilystring = "\clef treble"

class testClefFrench(Lily):
    def setUp(self):
        self.item = Clef.Clef(sign="G", line=1)
        self.lilystring = "\clef french"
