from implementation.primaries.Drawing.classes import MxmlParser, Piece, Measure, Part, Note, Directions
import unittest

class testSetupPiece(unittest.TestCase):
    def setUp(self):
        self.handler = MxmlParser.SetupPiece
        self.tags = []
        self.attrs = {}
        self.chars = {}
        self.piece = Piece.Piece()

    def testNoTags(self):
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: testNoTags failed: nothing should happen if there are no tags in list")

    def testMetaExists(self):
        self.assertFalse(hasattr(self.piece, "meta"), "ERROR: testMetaExists failed: meta should not be set in piece class at beginning of testing")

    def testIrrelevantTag(self):
        self.tags.append("lol")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: irrelevant tag should do nothing in TestIrrelevance")

    def testTitleTag(self):
        self.tags.append("movement-title")
        self.chars["movement-title"] = "hehehe"
        self.handler(self.tags, self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.piece, "meta"), "ERROR: Meta should exist in TestTitleTag")
        self.assertEqual("hehehe", self.piece.meta.title, "ERROR: title set incorrectly in TestTitleTag")

    def testCompTag(self):
        self.tags.append("creator")
        self.attrs["creator"] = {"type":"composer"}
        self.chars["creator"] = "lee"
        self.handler(self.tags, self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.piece, "meta"), "ERROR: meta should exist in piece class in TestCompTag")
        self.assertEqual("lee",self.piece.meta.composer, "ERROR: composer should match expected in TestCompTag")

    def testTitleCompTag(self):
        self.tags.append("creator")
        self.attrs["creator"] = {"type":"composer"}
        self.chars["creator"] = "lee"
        self.chars["movement-title"] = "hello world"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.piece.meta, "composer"), "ERROR: meta should have composer attrib in TestTitleCompTag")
        self.assertEqual("lee",self.piece.meta.composer, "ERROR: composer should match test in TestTitleCompTag")
        self.tags.append("movement-title")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.piece.meta, "title"), "ERROR: meta should have title in TestTitleCompTag")
        self.assertEqual("hello world", self.piece.meta.title, "ERROR: meta title set incorrectly in TestTitleCompTag")

class testHandlePart(unittest.TestCase):
    def setUp(self):
        self.handler = MxmlParser.UpdatePart
        self.tags = []
        self.chars = {}
        self.attrs = {}
        self.piece = Piece.Piece()

    def testNoData(self):
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: no tags should return none in TestNodata")

    def testIrrelevantTag(self):
        self.tags.append("wut")
        MxmlParser.part_id = None
        self.assertEqual(None, self.handler(self.tags, self.attrs,self.chars,self.piece), "ERROR: irrelevant tags should return none in TestIrrelevantTag")

    def testScorePartTag(self):
        MxmlParser.part_id = None
        self.assertEqual(None,MxmlParser.part_id,"ERROR: part_id not none in testScorePartTag")
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id":"P1"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual(1, len(self.piece.Parts.keys()))

    def testPnameTag(self):
        self.assertEqual(0, len(self.piece.Parts.keys()))
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id":"P1"}
        self.tags.append("part-name")
        self.chars["part-name"] = "will"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual("will", self.piece.Parts["P1"].name)

    def testPNameWithShortName(self):
        self.assertEqual(0, len(self.piece.Parts.keys()))
        self.tags.append("score-part")
        self.attrs["score-part"] = {"id":"P1"}
        self.tags.append("part-abbreviation")
        self.chars["part-abbreviation"] = "w"
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.assertEqual("w", self.piece.Parts["P1"].shortname)



