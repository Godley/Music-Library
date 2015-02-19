import unittest
from implementation.primaries.Drawing.classes.tree_cls import PieceTree,Testclasses

class testPieceTree(unittest.TestCase):
    def setUp(self):
        self.item = Testclasses.PieceTree()

    def testAddPart(self):
        part = Testclasses.PartNode(self.item)
        self.item.AddNode(part, index="P1")
        self.assertEqual(self.item.FindNodeByIndex("P1"), part)

    def testAddInvalidMeasure(self):
        measure = Testclasses.MeasureNode()
        with self.assertRaises(PieceTree.CannotAddToTreeException):
            self.item.AddNode(measure, index=1)

    def testFindStaff(self):
        part = Testclasses.PartNode(self.item)
        staff = Testclasses.StaffNode()
        self.item.AddNode(part, index="P1")
        self.item.AddNode(staff, index=1)
        self.assertEqual(part.getStaff(1), staff)

    def testFindMeasure(self):
        part = Testclasses.PartNode(self.item)
        staff = Testclasses.StaffNode()
        self.item.AddNode(part, index="P1")
        self.item.AddNode(staff, index=1)
        measure = Testclasses.MeasureNode()
        self.item.AddNode(measure, index=1)
        self.assertEqual(part.getMeasure(1, 1), measure)

    def testAddMeasureOnSecondStave(self):
        part = Testclasses.PartNode(self.item)
        staff = Testclasses.StaffNode()
        staff2 = Testclasses.StaffNode()
        measure = None
        self.item.AddNode(part, index="P1")
        self.item.AddNode(staff, index=1)
        self.item.AddNode(staff2, index=2)
        part.addMeasure(measure,staff=2)
        self.assertEqual(part.getMeasure(1,2).GetItem(),measure)

class testAddToMeasure(unittest.TestCase):
    def setUp(self):
        self.item = Testclasses.PieceTree()
        self.part = Testclasses.PartNode(self.item)
        self.item.AddNode(self.part, index="P1")
        self.part.addEmptyMeasure()
        self.measure = self.part.getMeasure()

    def testAddNote(self):
        note = "3"
        self.measure.addNote(note)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), note)

    def testAddDirection(self):
        direction = "2"
        self.measure.addDirection(direction)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetChild(1).GetItem(), direction)
        pass

    def testAddExpression(self):
        exp = "2"
        self.measure.addExpression(exp)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetChild(0).GetItem(), exp)
        pass