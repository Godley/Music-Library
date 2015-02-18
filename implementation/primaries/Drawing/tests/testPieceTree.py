import unittest
from implementation.primaries.Drawing.classes.tree_cls import PieceTree,Testclasses

class testPieceTree(unittest.TestCase):
    def setUp(self):
        self.item = Testclasses.PieceTree()

    def testAddPart(self):
        part = Testclasses.PartNode()
        self.item.AddNode(part, index="P1")
        self.assertEqual(self.item.FindNodeByIndex("P1"), part)

    def testAddInvalidMeasure(self):
        part = Testclasses.PartNode()
        measure = Testclasses.MeasureNode()
        with self.assertRaises(PieceTree.CannotAddToTreeException):
            self.item.AddNode(measure, index=1)
        
