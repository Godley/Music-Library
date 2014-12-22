import unittest
from implementation.primaries.Loading.tests import TestClass
from implementation.primaries.Loading.classes import Mark, MxmlParser, Piece, text, Part, Measure, Note

class testHandleArticulation(TestClass.TestClass):
    def setUp(self):
        TestClass.TestClass.setUp(self)
        self.piece.Parts["P1"] = Part.Part()
        self.part = self.piece.Parts["P1"]
        self.part.measures[1] = Measure.Measure()
        MxmlParser.note = Note.Note()
        self.note = MxmlParser.note
        self.part.measures[1].items.append(MxmlParser.note)
        self.handler = MxmlParser.handleArticulation
        self.tags.append("articulation")


    def testNoData(self):
        self.tags.remove("articulation")
        self.assertEqual(None,self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testIrrelevant(self):
        self.tags.remove("articulation")
        self.tags.append("what")
        self.assertEqual(None,self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testRelevant(self):
        self.assertEqual(1, self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testArticulationAccentTag(self):
        self.tags.append("accent")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.note, "notations"))
        self.assertIsInstance(self.note.notations[0], Mark.Accent)

    def testArticulationAccentType(self):
        self.tags.append("accent")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.note, "notations"))
        self.assertEqual("-",self.note.notations[0].symbol)

    def testArticulationAccentAttrib(self):
        self.tags.append("accent")
        self.attrs = {"placement":"below"}
        self.handler(self.tags,self.attrs,None,self.piece)
        self.assertEqual("below",self.note.notations[0].placement)

    def testArticulationSaccentTag(self):
        self.tags.append("strong-accent")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(self.note.notations[0], Mark.StrongAccent)

    def testArticulationStrongAccentTag(self):
        self.tags.append("strong-accent")
        self.attrs = {"type":"down"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual("V",self.note.notations[0].symbol)

    def testStaccato(self):
        self.tags.append("staccato")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(self.note.notations[0], Mark.Staccato)

    def testStaccatoSymbol(self):
        self.tags.append("staccato")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(".", self.note.notations[0].symbol)

    def testStaccatissimo(self):
        self.tags.append("staccatissimo")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertIsInstance(self.note.notations[0], Mark.Staccatissimo)

    def testStaccatissimoSymbol(self):
        self.tags.append("staccatissimo")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("triangle", self.note.notations[0].symbol)

    def testDetachedLegato(self):
        self.tags.append("detached-legato")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(self.note.notations[0], Mark.DetachedLegato)

    def testDetachedLegSymbol(self):
        self.tags.append("detached-legato")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("lineDot", self.note.notations[0].symbol)

    def testTenuto(self):
        self.tags.append("tenuto")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(self.note.notations[0], Mark.Tenuto)

    def testTenutoSymbol(self):
        self.tags.append("tenuto")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("line", self.note.notations[0].symbol)

class testLyrics(TestClass.TestClass):
    def setUp(self):
        TestClass.TestClass.setUp(self)
        self.tags.append("note")
        self.tags.append("lyric")
        self.handler = MxmlParser.handleLyrics
        MxmlParser.note = Note.Note()

    def testLyricCreation(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(MxmlParser.note, "lyrics"))

    def testLyricNum(self):
        self.attrs["lyric"] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(1 in MxmlParser.note.lyrics.keys())

    def testLyricText(self):
        self.attrs["lyric"] = {"number": "1"}
        self.chars["text"] = "aaah"
        self.tags.append("text")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("aaah", MxmlParser.note.lyrics[1].text)

    def testLyricSyllable(self):
        self.attrs["lyric"] = {"number": "1"}
        self.chars["syllabic"] = "single"
        self.tags.append("syllabic")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("single", MxmlParser.note.lyrics[1].syllabic)

class testFermata(TestClass.TestClass):
    def setUp(self):
        TestClass.TestClass.setUp(self)
        self.tags.append("fermata")
        MxmlParser.note = Note.Note()
        self.handler = MxmlParser.HandleFermata

    def testFermata(self):
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.note.notations[-1], Mark.Fermata)

    def testFermataType(self):
        self.attrs["fermata"] = {"type": "inverted"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("inverted", MxmlParser.note.notations[-1].type)

    def testFermataSymbol(self):
        self.chars["fermata"] = "square"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("square", MxmlParser.note.notations[-1].symbol)


class testSlurs(TestClass.TestClass):
    def setUp(self):
        TestClass.TestClass.setUp(self)
        self.tags.append("note")
        self.tags.append("notations")
        self.handler = MxmlParser.handleOtherNotations
        MxmlParser.note = Note.Note()

    def testNoData(self):
        self.tags.remove("note")
        self.tags.remove("notations")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testUnrelated(self):
        self.tags.remove("note")
        self.tags.remove("notations")
        self.tags.append("hello")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testRelated(self):
        self.assertEqual(1,self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testSlur(self):
        self.tags.append("slur")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note, "slurs"))
        self.assertEqual(text.Slur, type(MxmlParser.note.slurs[0]))

    def testSlurPlacement(self):
        self.tags.append("slur")
        self.attrs = {"placement":"above"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note.slurs[0], "placement"))
        self.assertEqual("above",MxmlParser.note.slurs[0].placement)

    def testSlurWithId(self):
        self.tags.append("slur")
        self.attrs = {"number":"1"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(1 in MxmlParser.note.slurs)

    def testSlurType(self):
        self.tags.append("slur")
        self.attrs = {"type":"start"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note.slurs[0], "type"))
        self.assertEqual("start",MxmlParser.note.slurs[0].type)

class testTechniques(TestClass.TestClass):
    def setUp(self):
        TestClass.TestClass.setUp(self)
        self.tags.append("note")
        self.tags.append("notations")
        self.handler = MxmlParser.handleOtherNotations
        MxmlParser.note = Note.Note()
        self.tags.append("technical")

    def testNoData(self):
        self.tags.remove("notations")
        self.tags.remove("note")
        self.tags.remove("technical")
        self.assertIsNone(self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testIrrelevant(self):
        self.tags.remove("technical")
        self.tags.remove("notations")
        self.tags.remove("note")
        self.tags.append("hello")
        self.assertIsNone(self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testUpBow(self):
        self.tags.append("up-bow")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note, "techniques"))
        self.assertIsInstance(MxmlParser.note.techniques[0], text.Technique)

    def testUpBowVal(self):
        self.tags.append("up-bow")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note.techniques[0], "type"))
        self.assertEqual("up-bow",MxmlParser.note.techniques[0].type)

    def testDownBowVal(self):
        self.tags.append("down-bow")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note.techniques[0], "type"))
        self.assertEqual("down-bow",MxmlParser.note.techniques[0].type)

    def testSnapPizz(self):
        self.tags.append("snap-pizzicato")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("snap-pizzicato", MxmlParser.note.techniques[0].type)

    def testStopped(self):
        self.tags.append("stopped")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual("stopped", MxmlParser.note.techniques[0].type)
