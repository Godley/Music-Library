import unittest, os
from implementation.primaries.Loading.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Loading.classes import MxmlParser, Directions

partname = "two_staves_one_part.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testTwoStavesInOnePart(unittest.TestCase):
    def testItemsInstance(self):
        self.assertIsInstance(piece.Parts["P1"].measures[1].items, dict)

    def testItemsIds(self):
        self.assertTrue(1 in piece.Parts["P1"].measures[0].items)
        self.assertTrue(2 in piece.Parts["P1"].measures[0].items)

    def testItemOneStaveOne(self):
        measure = piece.Parts["P1"].measures[0]
        self.assertIsInstance(measure.items[1][0], Directions.Dynamic)