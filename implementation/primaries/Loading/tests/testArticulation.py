import unittest
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
        self.assertTrue(hasattr(self.note, "articulations"))
        self.assertEqual(Note.Accent,type(self.note.articulations[0]))

    def testArticulationAccentType(self):
        self.tags.append("accent")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.note, "articulations"))
        self.assertEqual("-",self.note.articulations[0].symbol)

    def testArticulationAccentAttrib(self):
        self.tags.append("accent")
        self.attrs = {"placement":"below"}
        self.handler(self.tags,self.attrs,None,self.piece)
        self.assertEqual("below",self.note.articulations[0].placement)

    def testArticulationSaccentTag(self):
        self.tags.append("strong-accent")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(Note.StrongAccent, type(self.note.articulations[0]))

    def testArticulationStrongAccentTag(self):
        self.tags.append("strong-accent")
        self.attrs = {"type":"down"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual("V",self.note.articulations[0].symbol)

    def testStaccato(self):
        self.tags.append("staccato")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(Note.Staccato, type(self.note.articulations[0]))

    def testStaccatoSymbol(self):
        self.tags.append("staccato")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(".", self.note.articulations[0].symbol)

    def testStaccatissimo(self):
        self.tags.append("staccatissimo")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(Note.Staccatissimo, type(self.note.articulations[0]))

    def testStaccatissimoSymbol(self):
        self.tags.append("staccatissimo")
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual("triangle", self.note.articulations[0].symbol)