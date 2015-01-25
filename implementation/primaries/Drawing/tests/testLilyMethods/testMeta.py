from implementation.primaries.Drawing.classes import Meta, Directions
from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily

class testMeta(Lily):
    def setUp(self):
        self.item = Meta.Meta()
        self.lilystring = "\header {\n\n}"

class testMetaTitle(Lily):
    def setUp(self):
        self.item = Meta.Meta(title="hello world")
        self.lilystring = "\header {\ntitle = \"hello world\"\n}"

class testMetaComposer(Lily):
    def setUp(self):
        self.item = Meta.Meta(composer="Danny Brown")
        self.lilystring = "\header {\ncomposer = \"Danny Brown\"\n}"

class testMetaCreds(Lily):
    def setUp(self):
        self.item = Meta.Meta()
        self.item.credits = [Directions.CreditText(text="Danny is a jew")]
        self.lilystring = "\header {\n\n}\n\markup { Danny is a jew }"