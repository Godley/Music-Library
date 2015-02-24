import unittest, os
from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes.tree_cls.Testclasses import StaffNode

partname = "two_staves_one_part.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testTwoStavesInOnePart(unittest.TestCase):

    def testItemsIds(self):
        self.assertIsInstance(piece.getPart("P1").getStaff(1), StaffNode)
        self.assertTrue(piece.getPart("P1").getStaff(2), StaffNode)