import unittest, os
from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import MxmlParser, Directions

partname = "two_staves_one_part.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testTwoStavesInOnePart(unittest.TestCase):
    def testItemsInstance(self):
        self.assertIsInstance(piece.Parts["P1"].measures, dict)

    def testItemsIds(self):
        self.assertTrue(1 in piece.Parts["P1"].measures)
        self.assertTrue(2 in piece.Parts["P1"].measures)