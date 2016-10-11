import unittest
from implementation.primaries.ExtractMetadata.classes import MetaParser
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict
import os
import inspect


class TestCase1(unittest.TestCase):

    def setUp(self):
        self.file = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)),
            'test_files/extractor_test/testcase1.xml')
        self.parser = MetaParser.MetaParser()
        self.result = self.parser.parse(self.file)

    def testInstruments(self):
        self.assertEqual(self.result["instruments"], [{"name": "Piano"}])

    def testClefs(self):
        expected = {
            "Piano": [
                {'sign': "G", 'line': 2},
                {'sign': "F", 'line': 4},
                {'line': 3, 'sign': "C"}]}
        for instrument in expected:
            assert instrument in self.result["clefs"]
            for elem in expected[instrument]:
                assert elem in self.result["clefs"][instrument]

    def testKeys(self):
        self.assertEqual(
            self.result["keys"], {"Piano": [{'fifths': 2, 'mode': "major"}]})

    def testTempos(self):
        self.assertEqual(self.result["tempos"], [{"beat": "half", "minute": 80}, {
                         "minute": 80, "beat": "eighth."}])

    def testTitle(self):
        self.assertEqual(self.result["title"], "my metaparsing testcase")

    def testLyricist(self):
        self.assertEqual(self.result["lyricist"], "fran godley")

    def testComposer(self):
        self.assertEqual(self.result["composer"], "charlotte godley")


class TestCase2(unittest.TestCase):

    def setUp(self):
        self.file = os.path.join(
            os.path.dirname(
                os.path.realpath(__file__)),
            'test_files/extractor_test/testcase2.xml')
        self.parser = MetaParser.MetaParser()
        self.result = self.parser.parse(self.file)

    def testInstruments(self):
        self.assertEqual(self.result["instruments"], [{"name": "Piano"}])

    def testClefs(self):
        expected = {"Piano": [{'sign': "G", 'line': 2}, {
            'line': 3, 'sign': "C"}, {'sign': "F", 'line': 4}]}
        for instrument in expected:
            assert instrument in self.result["clefs"]
            for elem in expected[instrument]:
                assert elem in self.result["clefs"][instrument]

    def testKeys(self):
        self.assertEqual(
            self.result["keys"], {"Piano": [{'fifths': 2, 'mode': "major"}]})

    def testTempos(self):
        self.assertEqual(self.result["tempos"], [
                         {"beat": "half", "beat_2": "quarter"}, {"minute": 80, "beat": "eighth."}])

    def testTitle(self):
        self.assertEqual(self.result["title"], "my metaparsing testcase")

    def testLyricist(self):
        self.assertEqual(self.result["lyricist"], "fran godley")

    def testComposer(self):
        self.assertEqual(self.result["composer"], "charlotte godley")
