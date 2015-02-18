import unittest
try:
    from implementation.primaries.Drawing.classes.TimedElementsHolder import Node, LinkedList
except:
    from classes.TimedElementsHolder import Node, LinkedList

class testNode(unittest.TestCase):
    def setUp(self):
        self.item = Node(1,None)

    def testGetDuration(self):
        self.assertEqual(1, self.item.GetDuration())

    def testGetValue(self):
        self.assertEqual(None, self.item.GetValue())

    def testSetDuration(self):
        self.item.SetDuration(2)
        self.assertEqual(2, self.item.GetDuration())

    def testSetValue(self):
        self.item.SetValue("h")
        self.assertEqual("h", self.item.GetValue())

    def testGetNext(self):
        self.assertIsNone(self.item.Next())

    def testGetPrevious(self):
        self.assertIsNone(self.item.Previous())

    def testSetNext(self):
        self.toadd = Node(0,None)
        self.item.SetNext(self.toadd)
        self.assertEqual(self.toadd,self.item.Next())

    def testSetPrevious(self):
        self.toadd = Node(0, None)
        self.item.SetPrevious(self.toadd)
        self.assertEqual(self.toadd, self.item.Previous())

class testLinkedList(unittest.TestCase):
    def setUp(self):
        self.item = LinkedList()

    def testGetHead(self):
        self.assertIsNone(self.item.Head())

    def testGetTail(self):
        self.assertIsNone(self.item.Tail())

    def testAdd1Item(self):
        new_item = Node(1,"hello")
        self.item.Add(new_item)
        self.assertEqual(self.item.Head(),new_item)
        self.assertEqual(self.item.Tail(),new_item)

    def testAdd2Items(self):
        new_item = Node(1,"hello")
        self.item.Add(new_item)
        next = Node(2, "lol")
        self.item.Add(next)
        self.assertEqual(self.item.Head(),new_item)
        self.assertEqual(self.item.Head().Next(),next)

    def testAddWithOffset(self):
        new_item = Node(1, "hello")
        self.item.Add(new_item, offset=2)
        self.assertEqual(self.item.Head().GetDuration(), 2)
        self.assertEqual(self.item.Head().Next(), new_item)