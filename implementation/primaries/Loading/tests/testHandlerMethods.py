from implementation.primaries.Loading.classes import MxmlParser, Piece
import unittest
from unittest import mock

class testSetupPiece(unittest.TestCase):
    def setUp(self):
        self.handler = MxmlParser.SetupPiece
        self.tags = []
        self.attrs = []
        self.chars = {}
        self.piece = Piece.Piece()

    def testNoTags(self):
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: testNoTags failed: nothing should happen if there are no tags in list")

    def testMetaExists(self):
        self.assertFalse(hasattr(self.piece, "meta"), "ERROR: testMetaExists failed: meta should not be set in piece class at beginning of testing")

    def testIrrelevantTag(self):
        self.tags.append("lol")
        self.assertEqual(None, self.handler(self.tags,self.attrs,self.chars,self.piece), "ERROR: irrelevant tag should do nothing in TestIrrelevance")

    def TestTitleTag(self):
        self.tags.append("movement-title")
        self.chars["movement-title"] = "hehehe"
        self.handler(self.tags, self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.piece, "meta"), "ERROR: Meta should exist in TestTitleTag")
        self.assertEqual("hehehe", self.piece.meta.title, "ERROR: title set incorrectly in TestTitleTag")

    def TestCompTag(self):
        self.tags.append("creator")
        self.attrs["creator"] = {"type":"composer"}
        self.chars["creator"] = "lee"
        self.handler(self.tags, self.attrs,self.chars,self.piece)
        self.assertTrue(hasattr(self.piece, "meta"), "ERROR: meta should exist in piece class in TestCompTag")
        self.assertEqual("lee",self.piece.meta.composer, "ERROR: composer should match expected in TestCompTag")

    def TestTitleCompTag(self):
        self.tags.append("creator")
        self.tags.append("movement-title")
        self.attrs["creator"] = {"type":"composer"}
        self.chars["creator"] = "lee"
        self.chars["movement-title"] = "hello world"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertTrue(hasattr(self.piece.meta, "composer"), "ERROR: meta should have composer attrib in TestTitleCompTag")
        self.assertEqual("lee",self.piece.meta.composer, "ERROR: composer should match test in TestTitleCompTag")
        self.assertTrue(hasattr(self.piece.meta, "title"), "ERROR: meta should have title in TestTitleCompTag")
        self.assertEqual("hello world", self.piece.meta.title, "ERROR: meta title set incorrectly in TestTitleCompTag")

