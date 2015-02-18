from implementation.primaries.Drawing.classes import PieceTree
import unittest

class testPieceTree(unittest.TestCase):
    def setUp(self):
        self.item = PieceTree.Tree()

    #
    def testAddNode(self):
        elem = PieceTree.Node()
        self.item.AddNode(elem)
        self.assertEqual(elem, self.item.root)

    def testAddInvalidNode(self):
        elem = PieceTree.Node()
        self.item.AddNode(elem)
        self.assertRaises(PieceTree.CannotAddToTreeException, self.item.AddNode, PieceTree.Node())

    def testAddTwoValidNodes(self):
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode,PieceTree.IndexedNode])
        self.item.AddNode(elem)
        self.item.AddNode(PieceTree.EmptyNode(0))
        self.assertEqual(1, len(elem.children))

    def testAddNodeOverLimit(self):
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode,PieceTree.IndexedNode],limit=-1)
        self.item.AddNode(elem)
        self.assertRaises(PieceTree.CannotAddToTreeException, self.item.AddNode, PieceTree.EmptyNode(0))

    def testAddNodeAddsToNextLevel(self):
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode,PieceTree.IndexedNode],limit=1)
        next = PieceTree.EmptyNode(0,rules=[PieceTree.Node])
        third = PieceTree.Node()
        self.item.AddNode(elem)
        self.item.AddNode(next)
        self.item.AddNode(third)
        self.assertEqual(next.GetChild(0),third)


