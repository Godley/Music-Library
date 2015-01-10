from implementation.primaries.Drawing.classes import Meta, Directions
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testMeta(Lily):
    def setUp(self):
        self.item = Meta.Meta()
        self.lilystring = ""

class testMetaTitle(Lily):
    def setUp(self):
        self.item = Meta.Meta(title="hello world")
        self.lilystring = ""

class testMetaComposer(Lily):
    def setUp(self):
        self.item = Meta.Meta(composer="Danny Brown")
        self.lilystring = ""

class testMetaCreds(Lily):
    def setUp(self):
        self.item = Meta.Meta()
        self.item.credits = [Directions.CreditText(text="Danny is a jew")]
        self.lilystring = ""