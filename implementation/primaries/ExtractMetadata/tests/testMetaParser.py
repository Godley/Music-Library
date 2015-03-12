import unittest
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MetaParser

class testMetaParser(unittest.TestCase):
    def setUp(self):
        self.parser = MetaParser.MetaParser()

    def testStartTag(self):
        self.parser.StartTag("part", {})
        self.assertEqual(self.parser.tags, ["part"])

    def testNewData(self):
        self.parser.StartTag("part", {})
        self.parser.NewData("hello")
        self.assertEqual(self.parser.chars, {"part":"hello"})

    def testEndTag(self):
        self.parser.StartTag("part",{})
        self.parser.EndTag("part")
        self.assertEqual(self.parser.tags, [])

    def tearDown(self):
        self.parser = None

class testAddPart(testMetaParser):
    def setUp(self):
        testMetaParser.setUp(self)

    def testPartNameHandler(self):
        self.parser.StartTag("score-part", {})
        self.parser.StartTag("part-name",{})
        self.assertEqual(MetaParser.makeNewPart, self.parser.current_handler)

    def testPartNameHandlerCall(self):
        self.parser.StartTag("score-part", {})
        self.parser.StartTag("part-name",{})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.NewData("hello")
        self.parser.current_handler.assert_called_once_with(self.parser.tags, self.parser.attribs, self.parser.chars)

    def testPartNameCreation(self):
        self.parser.StartTag("score-part", {"id":"P1"})
        self.parser.StartTag("part-name", {})
        self.parser.NewData("laura")
        self.assertEqual(self.parser.parts, {"P1":{"name":"laura"}})
        self.assertEqual(self.parser.data, {"instruments":["laura"]})
