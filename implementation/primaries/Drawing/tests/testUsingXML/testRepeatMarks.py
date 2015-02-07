from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
from implementation.primaries.Drawing.classes import Directions, Note, Mark
import os

partname = "repeatmarks.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))
#TODO: handle forward tags
class testFile(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

class testFwd(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.measure_id = 19
        self.item_id = 0
        self.p_id = "P1"
        self.p_name = "Flute"
        if hasattr(self, "measure_id"):
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.forwards[1][0]
    def testHasFwd(self):
        if hasattr(self, "item"):
            self.assertIsInstance(self.item, Directions.Forward)

    def testDuration(self):
        if hasattr(self, "item"):
            self.assertEqual(1920, self.item.duration)

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "segno"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.segno, self.measure.segno)


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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "coda"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.coda, self.measure.coda)

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

    def testHasAttr(self):
        if hasattr(self, "measure"):
            self.assertTrue(hasattr(self.measure, "fine"))

    def testValue(self):
        if hasattr(self, "measure"):
            self.assertEqual(self.fine, self.measure.fine)

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

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
            self.measure = piece.Parts[self.p_id].measures[self.measure_id]

        if hasattr(self, "item_id"):
            self.item = self.measure.items[1][0][0]

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
