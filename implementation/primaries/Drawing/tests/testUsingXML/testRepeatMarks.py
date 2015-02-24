from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Directions
from implementation.primaries.Drawing.classes.tree_cls.PieceTree import PieceTree, NoteNode, MeasureNode, PartNode, Search, DirectionNode
import os

partname = "repeatmarks.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))
class testFile(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testParts(self):
        global piece
        self.assertIsInstance(piece.getPart(self.p_id), PartNode)
        self.assertEqual(self.p_name, piece.getPart(self.p_id).GetItem().name)

    def testMeasures(self):
        self.assertIsInstance(piece.getPart(self.p_id).getMeasure(self.m_num, 1), MeasureNode)


class testSegno(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"
        self.segno = "segno"
        self.measure_id = 2
        self.item_id = 0
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measure, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure.GetItem(), "segno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.segno, self.measure.GetItem().segno)


class testCoda(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"
        self.measure_id = 3
        self.item_id = 0
        self.coda = "coda"
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measure, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure.GetItem(), "coda"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.coda, self.measure.GetItem().coda)

class testFine(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"
        self.measure_id = 6
        self.item_id = 1
        self.fine = True
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measure, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure.GetItem(), "fine"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.fine, self.measure.GetItem().fine)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("Fine", self.item.text)

class testDaCapo(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.measure_id = 7
        self.item_id = 1
        self.dacapo = True
        if hasattr(self, "measure_id"):
            self.measure = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measure, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure.GetItem(), "dacapo"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dacapo, self.measure.GetItem().dacapo)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.C.", self.item.text)


class testDaCapoAlFine(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.measure_id = 8
        self.item_id = 1
        self.dacapo = True
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)
            self.measure = self.measureNode.GetItem()

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "dacapo"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dacapo, self.measure.dacapo)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.C. al Fine", self.item.text)


class testDaCapoAlCoda(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.measure_id = 9
        self.item_id = 1
        self.dacapo = True
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)
            self.measure = self.measureNode.GetItem()

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "dacapo"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dacapo, self.measure.dacapo)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.C. al Coda", self.item.text)

class testDalSegnoAlCoda(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.measure_id = 10
        self.item_id = 1
        self.dalsegno = "segno"
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)
            self.measure = self.measureNode.GetItem()

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "dalsegno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dalsegno, self.measure.dalsegno)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.S. al Coda", self.item.text)

class testDalSegnoAlFine(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.measure_id = 12
        self.item_id = 1
        self.dalsegno = "segno"
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)
            self.measure = self.measureNode.GetItem()

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "dalsegno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dalsegno, self.measure.dalsegno)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.S. al Fine", self.item.text)

class testDalSegno(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.measure_id = 13
        self.item_id = 1
        self.dalsegno = "segno"
        self.m_num = 32
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)
            self.measure = self.measureNode.GetItem()

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "dalsegno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.dalsegno, self.measure.dalsegno)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("D.S.", self.item.text)

class testToCoda(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.measure_id = 14
        self.item_id = 1
        self.tocoda = "coda"
        self.m_num = 32
        self.p_id = "P1"
        if hasattr(self, "measure_id"):
            self.measureNode = piece.getPart(self.p_id).getMeasure(self.measure_id, 1)
            self.measure = self.measureNode.GetItem()

        if hasattr(self, "item_id"):
            note = Search(NoteNode, self.measureNode, 1)
            self.item = Search(DirectionNode, note, 1).GetItem()

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "tocoda"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.tocoda, self.measure.tocoda)

    def testItem(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Direction)

    def testItemType(self):
        if hasattr(self, "item"):
            self.assertEqual("To Coda", self.item.text)
