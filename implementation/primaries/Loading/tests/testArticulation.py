import unittest
from implementation.primaries.Loading.tests import TestClass
from implementation.primaries.Loading.classes import MxmlParser, Piece, Part, Measure, Note

class testHandleArticulation(unittest.TestCase):
    def setUp(self):
        self.tags = []
        self.attrs = {}
        self.chars = {}
        self.piece = Piece.Piece()
        self.piece.Parts["P1"] = Part.Part()
        self.part = self.piece.Parts["P1"]
        self.part.measures[1] = Measure.Measure()
        MxmlParser.note = Note.Note()
        self.note = MxmlParser.note
        self.part.measures[1].notes.append(MxmlParser.note)
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
        self.assertEqual(Note.Accent,type(self.note.notations[0]))

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
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(Note.StrongAccent, type(self.note.notations[0]))

    def testArticulationStrongAccentTag(self):
        self.tags.append("strong-accent")
        self.attrs = {"type":"down"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual("V",self.note.notations[0].symbol)

    def testStaccato(self):
        self.tags.append("staccato")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(Note.Staccato, type(self.note.notations[0]))

    def testStaccatoSymbol(self):
        self.tags.append("staccato")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(".", self.note.notations[0].symbol)

    def testStaccatissimo(self):
        self.tags.append("staccatissimo")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(Note.Staccatissimo, type(self.note.notations[0]))

    def testStaccatissimoSymbol(self):
        self.tags.append("staccatissimo")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual("triangle", self.note.notations[0].symbol)

class testSlurAndTechnical(TestClass.TestClass):
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
        self.assertEqual(Note.Slur, type(MxmlParser.note.slurs[0]))

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

    def testNoteheadTag(self):
        self.tags.append("notehead")
        self.handler = MxmlParser.CreateNote
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(MxmlParser.note, "notehead"))

