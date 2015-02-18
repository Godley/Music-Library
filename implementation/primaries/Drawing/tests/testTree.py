import unittest

from implementation.primaries.Drawing.classes.tree_cls import PieceTree


class testTree(unittest.TestCase):
    def setUp(self):
        self.item = PieceTree.Tree()

    def testAddNode(self):
        elem = PieceTree.Node()
        self.item.AddNode(elem)
        self.assertEqual(elem, self.item.root)

    def testAddInvalidNode(self):
        elem = PieceTree.Node()
        self.item.AddNode(elem)
        self.assertRaises(PieceTree.CannotAddToTreeException, self.item.AddNode, PieceTree.Node())

    def testAddTwoValidNodes(self):
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode, PieceTree.IndexedNode])
        self.item.AddNode(elem)
        self.item.AddNode(PieceTree.EmptyNode(0))
        self.assertEqual(1, len(elem.children))

    def testAddNodeOverLimit(self):
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode, PieceTree.IndexedNode],limit=-1)
        self.item.AddNode(elem)
        self.assertRaises(PieceTree.CannotAddToTreeException, self.item.AddNode, PieceTree.EmptyNode(0))

    def testAddNodeAddsToNextLevel(self):
        # this test confirms that with a parent who allows 1 child which has to be empty or indexed, Next is it's child
        # and third is a child of next.
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode, PieceTree.IndexedNode],limit=1)
        next = PieceTree.EmptyNode(0,rules=[PieceTree.Node])
        third = PieceTree.Node()
        self.item.AddNode(elem)
        self.item.AddNode(next)
        self.item.AddNode(third)
        self.assertEqual(next.GetChild(0),third)

    def testAddNodeAddsToNextLevelWithExpandedLimit(self):
        # this test confirms the above still happens when the limit is 2
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode, PieceTree.IndexedNode],limit=2)
        next = PieceTree.EmptyNode(0,rules=[PieceTree.Node])
        third = PieceTree.Node()
        self.item.AddNode(elem)
        self.item.AddNode(next)
        self.item.AddNode(third)
        self.assertEqual(next.GetChild(0),third)

    def testAddNodeAddsToCurrentLevelWithRelevantRuleAndLimit(self):
        # this test confirms the first spot for third to land in is a second child of elem, because elem lets you have
        # node as a child and can have 2 children.
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode, PieceTree.Node],limit=2)
        next = PieceTree.EmptyNode(0,rules=[PieceTree.Node])
        third = PieceTree.Node()
        self.item.AddNode(elem)
        self.item.AddNode(next)
        self.item.AddNode(third)
        self.assertEqual(elem.GetChild(1),third)

    def testAddNodeWithIndex(self):
        elem = PieceTree.IndexedNode(rules=[PieceTree.EmptyNode], limit=1)
        second_elem = PieceTree.EmptyNode(0)
        self.item.AddNode(elem)
        self.item.AddNode(second_elem, index=2)
        self.assertEqual(elem.GetChild(2),second_elem)

    def testAddNodeToSecondNode(self):
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode])
        self.item.AddNode(elem)
        second = PieceTree.EmptyNode(0)
        self.item.AddNode(second)
        third = PieceTree.EmptyNode(0,rules=[PieceTree.Node])
        self.item.AddNode(third)
        fourth = PieceTree.Node()
        self.item.AddNode(fourth)
        self.assertEqual(third.GetChild(0), fourth)

    def testAddNodeToThirdNode(self):
        elem = PieceTree.Node(rules=[PieceTree.EmptyNode])
        self.item.AddNode(elem)
        second = PieceTree.EmptyNode(0)
        self.item.AddNode(second)
        third = PieceTree.EmptyNode(0)
        self.item.AddNode(third)
        fourth = PieceTree.EmptyNode(0, rules=[PieceTree.Node])
        self.item.AddNode(fourth)
        fifth = PieceTree.Node()
        self.item.AddNode(fifth)
        self.assertEqual(fourth.GetChild(0), fifth)

    def testFindFirstNode(self):
        elem = PieceTree.Node()
        self.item.AddNode(elem)
        self.assertEqual(self.item.FindNode(type(elem), 0), elem)

    def testFindSecondNode(self):
        elem = PieceTree.Node(rules=[PieceTree.Node])
        self.item.AddNode(elem)
        second = PieceTree.Node()
        self.item.AddNode(second)
        node = self.item.FindNode(type(elem), 1)
        self.assertEqual(node, second)

    def testFindFirstEmptyNodeOnFirstChild(self):
        elem = PieceTree.Node(rules=[PieceTree.Node])
        self.item.AddNode(elem)
        second = PieceTree.Node(rules=[PieceTree.EmptyNode])
        self.item.AddNode(second)
        third = PieceTree.EmptyNode(0)
        self.item.AddNode(third)
        node = self.item.FindNode(PieceTree.EmptyNode, 0)
        self.assertEqual(node, third)

    def testFindEmptyNodeOnSecondChild(self):
        elem = PieceTree.Node(rules=[PieceTree.Node])
        self.item.AddNode(elem)
        second = PieceTree.Node()
        self.item.AddNode(second)
        third = PieceTree.Node(rules=[PieceTree.EmptyNode])
        self.item.AddNode(third)
        fourth = PieceTree.EmptyNode(0)
        self.item.AddNode(fourth)
        node = self.item.FindNode(PieceTree.EmptyNode, 0)
        self.assertEqual(node, fourth)

    def testFailure(self):
        elem = PieceTree.Node(rules=[PieceTree.Node])
        self.item.AddNode(elem)
        second = PieceTree.Node()
        self.item.AddNode(second)
        third = PieceTree.Node(rules=[PieceTree.EmptyNode])
        self.item.AddNode(third)
        with self.assertRaises(PieceTree.CannotFindInTreeException):
            self.item.FindNode(PieceTree.EmptyNode, 0)

    def testAddNodeWithStringIndex(self):
        elem = PieceTree.IndexedNode(rules=[PieceTree.Node])
        self.item.AddNode(elem)
        second = PieceTree.Node()
        self.item.AddNode(second, "P1")
        self.assertEqual(elem.GetChild("P1"), second)

    def testFindNodeWithStringIndex(self):
        elem = PieceTree.IndexedNode(rules=[PieceTree.Node])
        self.item.AddNode(elem)
        second = PieceTree.Node()
        self.item.AddNode(second, "P1")
        self.assertEqual(self.item.FindNodeByIndex("P1"), second)

    def testFindNodeWithStringIndexOnSecondLevel(self):
        elem = PieceTree.Node(rules=[PieceTree.IndexedNode])
        self.item.AddNode(elem)
        second = PieceTree.IndexedNode(rules=[PieceTree.Node])
        self.item.AddNode(second)
        third = PieceTree.Node()
        self.item.AddNode(third, "S")
        self.assertEqual(self.item.FindNodeByIndex("S"), third)

    def testFindNodeWithStringIndexOnSecondLevelWhereFirstLevelIsIndexed(self):
        elem = PieceTree.IndexedNode(rules=[PieceTree.IndexedNode])
        self.item.AddNode(elem)
        second = PieceTree.IndexedNode(rules=[PieceTree.Node])
        self.item.AddNode(second, "A")
        third = PieceTree.Node()
        self.item.AddNode(third, "B")
        self.assertEqual(self.item.FindNodeByIndex("B"), third)



