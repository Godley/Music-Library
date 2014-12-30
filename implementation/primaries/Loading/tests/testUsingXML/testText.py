from implementation.primaries.Loading.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Loading.classes import Directions, Note, Mark
import os

partname = "text.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testFile(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

class testCredit(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        if hasattr(self, "note_id"):
            self.item = piece.meta.credits[self.note_id]

    def testHasCredits(self):
        meta = piece.meta
        self.assertTrue(hasattr(meta, "credits"))

    def testCredOne(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.CreditText)

    def testVal(self):
        if hasattr(self, "item"):
            self.assertEqual(self.value, self.item.text)

    def testPos(self):
        if hasattr(self, "item"):
            self.assertEqual(self.x, self.item.x)
            self.assertEqual(self.y, self.item.y)

    def testSize(self):
        if hasattr(self, "item"):
            self.assertEqual(self.size, self.item.size)

    def testJustify(self):
        if hasattr(self, "item"):
            self.assertEqual(self.justify, self.item.justify)

    def testValign(self):
        if hasattr(self, "item"):
            self.assertEqual(self.valign, self.item.valign)

    def testPage(self):
        if hasattr(self, "item"):
            self.assertEqual(self.page, self.item.page)

class testDirection(xmlSet):
    def setUp(self):
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][self.item_id]

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testPlacement(self):
        if hasattr(self, "item"):
            self.assertEqual(self.placement, self.item.placement)

    def testVal(self):
        if hasattr(self, "item"):
            self.assertEqual(self.words, self.item.text)

class testRehearsal(testDirection):
    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.RehearsalMark)

class testLyric(xmlSet):
    def setUp(self):
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]
        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][self.item_id]

    def testExists(self):
        if hasattr(self, "item"):
            self.assertTrue(hasattr(self.item, "lyrics"))

    def testInDict(self):
        if hasattr(self, "item"):
            self.assertTrue(self.number in self.item.lyrics)

    def testInstance(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item.lyrics[self.number], Directions.Lyric)



    def testSyllable(self):
        if hasattr(self, "item"):
            self.assertEqual(self.syllable, self.item.lyrics[self.number].syllabic)

    def testText(self):
        if hasattr(self, "item"):
            self.assertEqual(self.text, self.item.lyrics[self.number].text)

class testCreditOne(testCredit):
    def setUp(self):
        self.note_id = 0
        self.x = 56.6929
        self.y = 1560.09
        self.size = 12
        self.justify = "left"
        self.valign ="top"
        self.value = "Charlotte Godley"
        self.page = 1
        testCredit.setUp(self)

class testCreditTwo(testCredit):
    def setUp(self):
        self.note_id = 1
        self.x = 595.276
        self.y = 1627.09
        self.size = 24
        self.justify = "center"
        self.valign ="top"
        self.value = "Hello Friends"
        self.page = 1
        testCredit.setUp(self)

class testCreditThree(testCredit):
    def setUp(self):
        self.note_id = 2
        self.x = 1133.86
        self.y = 1560.09
        self.size = 12
        self.justify = "right"
        self.valign ="top"
        self.value = "Charlotte Godley"
        self.page = 1
        testCredit.setUp(self)

class testMeasureTwo(testDirection):
    def setUp(self):
        self.measure_id = 2
        self.item_id = 0
        self.placement = "above"
        self.words = "blablabla"
        testDirection.setUp(self)

class testMeasureFive(testRehearsal):
    def setUp(self):
        self.measure_id = 5
        self.item_id = 0
        self.words = "B"
        self.placement = "above"
        testRehearsal.setUp(self)

class testMeasureSeven(testLyric):
    def setUp(self):
        self.measure_id = 7
        self.item_id = 0
        self.text = "abc"
        self.syllable = "single"
        self.number = 1
        testLyric.setUp(self)