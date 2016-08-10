import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.MusicData import TempoParser

class TestTempoParser(unittest.TestCase):
    def setUp(self):
        self.parser = TempoParser()

    def testPartSplitter(self):
        entry = 'crotchet=80'
        expected = ['crotchet', '80']
        result = self.parser.splitParts(entry)
        self.assertEqual(result, expected)

    def testHalverWithSemi(self):
        entry = 'semiquaver'
        expected = 16
        result = self.parser.parseHalvers(entry)
        self.assertEqual(int(result), expected)

    def testHalverWithDemi(self):
        entry = 'demiquaver'
        expected = 16
        result = self.parser.parseHalvers(entry)
        self.assertEqual(int(result), expected)

    def testHalverWithHemi(self):
        entry = 'hemiquaver'
        expected = 16
        result = self.parser.parseHalvers(entry)
        self.assertEqual(int(result), expected)

    def testHalverWithHemiSemi(self):
        entry = 'hemisemiquaver'
        expected = 32
        result = self.parser.parseHalvers(entry)
        self.assertEqual(int(result), expected)

    def testHalverWithDemiSemi(self):
        entry = 'demisemiquaver'
        expected = 32
        result = self.parser.parseHalvers(entry)
        self.assertEqual(int(result), expected)

    def testHalverWithHemiDemi(self):
        entry = 'hemidemiquaver'
        expected = 32
        result = self.parser.parseHalvers(entry)
        self.assertEqual(int(result), expected)

    def testHalverWithHemDemiSemi(self):
        entry = 'hemidemisemiquaver'
        expected = 64
        result = self.parser.parseHalvers(entry)
        self.assertEqual(int(result), expected)

    def testHalverWithSemiHemiDemiSemi(self):
        entry = 'semihemidemisemiquaver'
        expected = 128
        result = self.parser.parseHalvers(entry)
        self.assertEqual(int(result), expected)

    def testQuaver(self):
        entry = 'quaver'
        expected = 'eighth'
        result = self.parser.convertToAmerican(entry)
        self.assertEqual(result, expected)

    def testCrotchet(self):
        entry = 'crotchet'
        expected = 'quarter'
        result = self.parser.convertToAmerican(entry)
        self.assertEqual(result, expected)

    def testMinim(self):
        entry = 'minim'
        expected = 'half'
        result = self.parser.convertToAmerican(entry)
        self.assertEqual(result, expected)

    def testSemibreve(self):
        entry = 'semibreve'
        expected = 'whole'
        result = self.parser.convertToAmerican(entry)
        self.assertEqual(result, expected)

    def testDots(self):
        entry = 'quaver.'
        expected = '.'
        result, remaining = self.parser.getDots(entry)
        self.assertEqual(result, expected)
        self.assertEqual(entry[:-1], remaining)

    def testMultipleDots(self):
        entry = 'quaver..'
        expected = '..'
        result, remaining = self.parser.getDots(entry)
        self.assertEqual(result, expected)
        self.assertEqual(entry[:-2], remaining)

    def testParseOneWordTempo(self):
        entry = 'quaver=80'
        expected = {'beat': 'eighth', 'minute': 80,
                    'beat_2': -1}
        result = self.parser.decode(entry)
        self.assertDictEqual(expected, result)

    def testParseTwoWordTempo(self):
        entry = 'quaver=crotchet'
        expected = {'beat': 'eighth', 'minute': -1,
                    'beat_2': 'quarter'}
        result = self.parser.decode(entry)
        self.assertDictEqual(expected, result)

    def testParseOneWordDottedTempo(self):
        entry = 'quaver.=80'
        expected = {'beat': 'eighth.', 'minute': 80,
                    'beat_2': -1}
        result = self.parser.decode(entry)
        self.assertDictEqual(expected, result)

    def testParseTwoWordDottedTempo(self):
        entry = 'quaver.=crotchet.'
        expected = {'beat': 'eighth.', 'minute': -1,
                    'beat_2': 'quarter.'}
        result = self.parser.decode(entry)
        self.assertDictEqual(expected, result)

    def testParseOneWordHalvedTempo(self):
        entry = 'semiquaver=80'
        expected = {'beat': '16th', 'minute': 80,
                    'beat_2': -1}
        result = self.parser.decode(entry)
        self.assertDictEqual(expected, result)

    def testParseHalvedDottedTempo(self):
        entry = 'semiquaver.=80'
        expected = {'beat': '16th.', 'minute': 80,
                    'beat_2': -1}
        result = self.parser.decode(entry)
        self.assertDictEqual(expected, result)