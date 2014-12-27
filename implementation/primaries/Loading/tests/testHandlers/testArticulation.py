from implementation.primaries.Loading.tests.testHandlers import testclass
from implementation.primaries.Loading.classes import Mark, MxmlParser, Directions, Part, Measure, Note

class testHandleArticulation(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
        self.piece.Parts["P1"] = Part.Part()
        self.part = self.piece.Parts["P1"]
        self.part.measures[1] = Measure.Measure()
        MxmlParser.note = Note.Note()
        self.note = MxmlParser.note
        self.part.measures[1].items.append(MxmlParser.note)
        self.handler = MxmlParser.handleArticulation
        self.tags.append("articulations")


    def testNoData(self):
        self.tags.remove("articulations")
        self.assertEqual(None,self.handler(self.tags,self.attrs,self.chars,self.piece))

    def testIrrelevant(self):
        self.tags.remove("articulations")
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

class testLyrics(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
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

class testFermata(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
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


class testSlurs(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
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
        self.assertEqual(Directions.Slur, type(MxmlParser.note.slurs[0]))

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

class t(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
        self.tags.append("note")
        self.tags.append("notations")
        self.handler = MxmlParser.handleOtherNotations
        MxmlParser.note = Note.Note()
        self.tags.append("technical")

class testTechniques(t):
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

class testClosedTechnique(t):
    def setUp(self):
        t.setUp(self)
        self.tag = ""

    def testCreated(self):
        self.tags.append(self.tag)
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note, "techniques"))
        self.assertIsInstance(MxmlParser.note.techniques[0], Mark.Technique)

    def testTechniqueType(self):
        self.tags.append(self.tag)
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note.techniques[0], "type"))
        self.assertEqual(self.tag,MxmlParser.note.techniques[0].type)

class testUpBow(testClosedTechnique):
    def setUp(self):
        testClosedTechnique.setUp(self)
        self.tag = "up-bow"

class testDownBow(testClosedTechnique):
    def setUp(self):
        testClosedTechnique.setUp(self)
        self.tag = "down-bow"

class testSnapPizz(testClosedTechnique):
    def setUp(self):
        testClosedTechnique.setUp(self)
        self.tag = "snap-pizzicato"

class testOpenTechnique(testClosedTechnique):
    def setUp(self):
        t.setUp(self)
        self.tag = ""
        self.value = ""

    def testTechniqueText(self):
        self.tags.append(self.tag)
        self.chars[self.tag] = self.value
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertEqual(self.value, MxmlParser.note.techniques[0].symbol)

class testFingering(testOpenTechnique):
    def setUp(self):
        testOpenTechnique.setUp(self)
        self.tag = "fingering"
        self.value = "0"

class testPluck(testOpenTechnique):
    def setUp(self):
        testOpenTechnique.setUp(self)
        self.tag = "pluck"
        self.value = "p"

class testString(testOpenTechnique):
    def setUp(self):
        testOpenTechnique.setUp(self)
        self.tag = "string"
        self.value = "0"

