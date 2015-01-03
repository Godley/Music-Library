from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.classes import Key

class testKey(Lily):
    def setUp(self):
        self.item = Key.Key()
        self.lilystring = "\key c \major"

class testKeyFifths(Lily):
    def setUp(self):
        self.item = Key.Key(fifths=1)
        self.lilystring = "\key g \major"

class testKeyMode(Lily):
    def setUp(self):
        self.item = Key.Key(mode="minor")
        self.lilystring = "\key a \minor"

class testKeyFifthsMode(Lily):
    def setUp(self):
        self.item = Key.Key(fifths=-3, mode="minor")
        self.lilystring = "\key c \minor"

class testKeyFifthsModeFlat(Lily):
    def setUp(self):
        self.item = Key.Key(fifths=-4, mode="major")
        self.lilystring = "\key aes \major"

class testKeyFifthsModeSharp(Lily):
    def setUp(self):
        self.item = Key.Key(fifths=7, mode="major")
        self.lilystring = "\key cis \major"
