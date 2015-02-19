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

    def testAddExpression(self):
        exp = "2"
        self.measure.addExpression(exp)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetChild(0).GetItem(), exp)

    def testAddPlaceholder(self):
        self.measure.addPlaceholder()
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), None)

    def testAddNoteWithPlaceholderBeforeIt(self):
        note=2
        self.measure.addNote(note)
        self.measure.index = 0
        self.measure.addPlaceholder()
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), None)

    def testForward(self):
        self.measure.addNote(1)
        self.measure.Forward(duration=16)
        self.assertEqual(self.measure.index, 2)

    def testBackup(self):
        self.measure.addNote(1)
        self.measure.Backup(duration=15)
        self.assertEqual(self.measure.index, 0)

    def testForwardCreatesAPlaceholder(self):
        self.measure.addNote(1)
        self.measure.Forward(duration=16)
        voice = self.measure.getVoice(1)
        self.assertIsInstance(voice.GetChild(1), Testclasses.NoteNode)

    def testBackupAndAddNote(self):
        self.measure.addNote(1)
        self.measure.Backup(duration=15)
        self.measure.addNote(2)
        voice = self.measure.getVoice(1)
        self.assertEqual(voice.GetChild(0).GetItem(), 2)