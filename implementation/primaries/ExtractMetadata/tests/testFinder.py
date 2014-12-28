import unittest
from implementation.primaries.ExtractMetadata.classes import Finder

folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/metadata'

finder = Finder.Finder(folder=folder)
finder.Run()

class testFinder(unittest.TestCase):

    def testInvalidEntry(self):
        self.assertFalse(finder.IsValidInput(""))

    def testNoMatch(self):
        self.assertEqual(0, len(finder.Match("wibble")))

    def testMatch(self):
        results = finder.Match("C major")
        count = 0
        for thing in results.keys():
            count += len(results[thing].keys())
        self.assertEqual(3, count)

    def testPartialMatch(self):
        results = finder.Match("Flu")
        count = 0
        for thing in results.keys():
            count += len(results[thing].keys())
        self.assertEqual(3, count)