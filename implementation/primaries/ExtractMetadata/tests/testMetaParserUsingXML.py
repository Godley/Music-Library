import unittest
from implementation.primaries.ExtractMetadata.classes import MetaParser

class testCase1(unittest.TestCase):
    def setUp(self):
        self.file = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/ExtractMetadata/tests/test_files/extractor_test/testcase1.xml'
        self.parser = MetaParser.MetaParser()
        self.result = self.parser.parse(self.file)

    def testInstruments(self):
        self.assertEqual(self.result["instruments"], [{"name":"Piano"}])

    def testClefs(self):
        self.assertEqual(self.result["clef"], {"Piano":[{"sign":"G","line":2},{"sign":"F","line":4},{"line":3,"sign":"C"}]})

    def testKeys(self):
        self.assertEqual(self.result["key"], {"Piano":[{"fifths":2,"mode":"major"}]})

    def testTempos(self):
        self.assertEqual(self.result["tempo"], [{"beat":"half","minute":80},{"minute":80,"beat":"eighth."}])

    def testTitle(self):
        self.assertEqual(self.result["title"], "My MetaParsing Testcase")

    def testLyricist(self):
        self.assertEqual(self.result["lyricist"], "Fran Godley")

    def testComposer(self):
        self.assertEqual(self.result["composer"], "Charlotte Godley")