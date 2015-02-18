import unittest
from implementation.primaries.Drawing.classes.tree_cls import PieceTree,Testclasses

class testPieceTree(unittest.TestCase):
    def setUp(self):
        self.item = Testclasses.PieceTree()

    def testAddPart(self):
        part = Testclasses.PartNode()
        self.item.AddNode(part, index="P1")
        self.assertEqual(self.item.FindNode(type(part),"P1"))
        
