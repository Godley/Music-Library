import unittest
from implementation.primaries.ExtractMetadata.classes import SearchProcessor


class TestSearchProcessor(unittest.TestCase):
    def testSplittingByColon(self):
        token = "instrument:world"
        result = SearchProcessor.handle_colons_and_semicolons(token)
        expected = {"instrument":["world"]}
        self.assertDictEqual(result, expected)

    def testSplittingByColonAndSemicolon(self):
        token = "instrument:world;paw"
        expected = {"instrument": ["world", "paw"]}
        result = SearchProcessor.handle_colons_and_semicolons(token)
        self.assertDictEqual(result, expected)

    def testSplittingByTwoColonsAndOneSemi(self):
        token = "instrument:clarinet;key:Cmaj"
        expected = {"instrument": ["clarinet"], "key": {"clarinet": ["Cmaj"]}}
        result = SearchProcessor.handle_colons_and_semicolons(token)
        self.assertDictEqual(result, expected)

    def testSplittingByTwoColonsAndSpaces(self):
        token = "instrument:clarinet key:Cmaj"
        expected = {"instrument": ["clarinet"], "key": ["Cmaj"]}
        result = SearchProcessor.process(token)
        self.assertDictEqual(result, expected)

    def testSplittingBySpaceNoColons(self):
        token = "C major"
        expected = {"key": ["C major"]}
        result = SearchProcessor.process(token)
        self.assertDictEqual(result, expected)

    def testSplittingBySpaceColonTokens(self):
        token = "\"C major\" key:Cmaj"
        expected = {"key": ["C major", "Cmaj"]}
        result = SearchProcessor.process(token)
        self.assertDictEqual(result, expected)

    def testCombineDictionaries(self):
        dict1 = {"key": {"other": ["Hello"]}}
        dict2 = {"key": {"other": ["World"]}}
        result = SearchProcessor.combine_dictionaries(dict1, dict2)
        self.assertEqual(list(result.keys()), ["key"])
        self.assertEqual(list(result["key"].keys()), ["other"])
        self.assertEqual(result["key"]["other"], ["Hello", "World"])

    def testCombineDictionariesWithMixOfTypes(self):
        dict1 = {"key": ["hello"]}
        dict2 = {"key": {"clarinet": ["hello"]}}
        result = SearchProcessor.combine_dictionaries(dict1, dict2)
        expected = {"key": {"other": ["hello"], "clarinet": ["hello"]}}
        self.assertDictEqual(result, expected)

    def testIsMeter(self):
        token = "4/4"
        self.assertTrue(SearchProcessor.is_meter(token))

    def testIsNotMeterChars(self):
        token = "h/1"
        self.assertFalse(SearchProcessor.is_meter(token))

    def testIsNotMeter2Chars(self):
        token = "h/c"
        self.assertFalse(SearchProcessor.is_meter(token))

    def testIsNotMeterNoDivide(self):
        token = "lol"
        self.assertFalse(SearchProcessor.is_meter(token))

    def testIsKey(self):
        token = ["C","major"]
        self.assertTrue(SearchProcessor.is_key(token))

    def testIsKeyMinor(self):
        token = ["C", "minor"]
        self.assertTrue(SearchProcessor.is_key(token))

    def testIsKeySharp(self):
        token = ["Csharp", "minor"]
        self.assertTrue(SearchProcessor.is_key(token))

    def testIsKeyFlat(self):
        token = ["Cflat", "minor"]
        self.assertTrue(SearchProcessor.is_key(token))

    def testIsNotKey(self):
        token = ["Hello"]
        self.assertFalse(SearchProcessor.is_key(token))

    def testIsTempoOneWord(self):
        token = "quaver=80"
        self.assertTrue(SearchProcessor.is_tempo(token))

    def testIsNotTempo(self):
        token = "1=2"
        self.assertFalse(SearchProcessor.is_tempo(token))

    def testIsTempoTwoWords(self):
        token = "quaver=crotchet"
        self.assertTrue(SearchProcessor.is_tempo(token))

    def testCreatesTempo(self):
        token = "quaver=crotchet"
        result = SearchProcessor.process(token)
        self.assertEqual(result["tempo"], [token])

    def testCreatesMeter(self):
        token = "2/4"
        result = SearchProcessor.process(token)
        self.assertEqual(result["meter"], [token])

    def testCreatesText(self):
        token = "nothing"
        result = SearchProcessor.process(token)
        self.assertEqual(result["text"], [token])

    def testFilenameOnNewMethod(self):
        token = "hello.xml"
        result = SearchProcessor.process(token)
        self.assertEqual(result["filename"], [token])

    def testTitleOrComposerOrLyricist(self):
        input = "hello, world"
        self.assertDictEqual(
            {"text": ["hello,", "world"]}, SearchProcessor.process(input))

    def testFilename(self):
        input = "lottie.xml"
        self.assertEqual({"filename": [input]}, SearchProcessor.process(input))

    def testTimeSig(self):
        input = "4/4"
        self.assertEqual({"meter": ["4/4"]}, SearchProcessor.process(input))

    def testTimeSigWithMeterLabel(self):
        input = "meter:4/4"
        self.assertEqual({"meter": ["4/4"]}, SearchProcessor.process(input))

    def testKey(self):
        input = "C major"
        self.assertEqual(
            {"key": ["C major"]}, SearchProcessor.process(input))

    def testTransposition(self):
        input = "transposition:clarinet"
        self.assertEqual(
            {"transposition": ["clarinet"]}, SearchProcessor.process(input))
