import unittest
from implementation.primaries.ExtractMetadata.classes import SearchProcessor


class TestSearchProcessor(unittest.TestCase):
    def testSplittingByColon(self):
        token = "instrument:world"
        result, remaining = SearchProcessor.handleColonsAndSemiColons(token)
        expected = {"instrument":{"other": ["world"]}}
        self.assertDictEqual(result, expected)

    def testSplittingByColonAndSemicolon(self):
        token = "instrument:world;paw"
        expected = {"instrument": {"other":["world", "paw"]}}
        result, remaining = SearchProcessor.handleColonsAndSemiColons(token)
        self.assertDictEqual(result, expected)

    def testSplittingByTwoColonsAndOneSemi(self):
        token = "instrument:clarinet;key:Cmaj"
        expected = {"instrument": {"other": ["clarinet"]}, "key": {"clarinet": ["Cmaj"]}}
        result, remaining = SearchProcessor.handleColonsAndSemiColons(token)
        self.assertDictEqual(result, expected)

    def testSplittingByTwoColonsAndSpaces(self):
        token = "instrument:clarinet key:Cmaj"
        expected = {"instrument": {"other": ["clarinet"]}, "key": {"other": ["Cmaj"]}}
        result = SearchProcessor.split_tokens(token)
        self.assertDictEqual(result, expected)

    def testSplittingBySpaceNoColons(self):
        token = "C major"
        expected = {"key": {"other": ["C major"]}}
        result = SearchProcessor.split_tokens(token)
        self.assertDictEqual(result, expected)

    def testSplittingBySpaceColonTokens(self):
        token = "\"C major\" key:Cmaj"
        expected = {"key": {"other": ["Cmaj", "C major"]}}
        result = SearchProcessor.split_tokens(token)
        self.assertDictEqual(result, expected)

    def testCombineDictionaries(self):
        dict1 = {"key": {"other": ["Hello"]}}
        dict2 = {"key": {"other": ["World"]}}
        result = SearchProcessor.combine_dictionaries(dict1, dict2)
        self.assertEqual(list(result.keys()), ["key"])
        self.assertEqual(list(result["key"].keys()), ["other"])
        self.assertEqual(result["key"]["other"], ["Hello", "World"])

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
        result = SearchProcessor.split_tokens(token)
        self.assertEqual(list(result.keys()), ["tempo"])
        self.assertEqual(list(result["tempo"].keys()), ["other"])
        self.assertEqual(result["tempo"]["other"], [token])

    def testCreatesMeter(self):
        token = "2/4"
        result = SearchProcessor.split_tokens(token)
        self.assertEqual(list(result.keys()), ["meter"])
        self.assertEqual(list(result["meter"].keys()), ["other"])
        self.assertEqual(result["meter"]["other"], [token])

    def testTitleOrComposerOrLyricist(self):
        input = "hello, world"
        self.assertEqual(
            {"text": ["hello,", "world"]}, SearchProcessor.process(input))

    def testFilename(self):
        input = "lottie.xml"
        self.assertEqual({"filename": [input]}, SearchProcessor.process(input))

    def testTimeSig(self):
        input = "4/4"
        self.assertEqual({"time": ["4/4"]}, SearchProcessor.process(input))

    def testTimeSigWithMeterLabel(self):
        input = "meter:4/4"
        self.assertEqual({"time": ["4/4"]}, SearchProcessor.process(input))

    def testTempo(self):
        input = "quarter=half"
        self.assertEqual(
            {"tempo": ["quarter=half"]}, SearchProcessor.process(input))

    def testInstrument(self):
        input = "instrument:clarinet"
        self.assertEqual(
            {"instrument": ["clarinet"]}, SearchProcessor.process(input))

    def testKey(self):
        input = "C major"
        self.assertEqual(
            {"key": {"other": ["C major"]}}, SearchProcessor.process(input))

    def testTransposition(self):
        input = "transposition:clarinet"
        self.assertEqual(
            {"transposition": ["clarinet"]}, SearchProcessor.process(input))

    def testWithKey(self):
        input = "instrument:clarinet with:key:\"C major\""
        self.assertEqual({"instrument": ["clarinet"],
                          "key": {"clarinet": ["C major"]}},
                         SearchProcessor.process(input))

    def testWithClef(self):
        input = "instrument:clarinet with:clef:bass"
        self.assertEqual({"instrument": ["clarinet"],
                          "clef": {"clarinet": ["bass"]}},
                         SearchProcessor.process(input))

    def testSemiColon(self):
        input = "instrument:clarinet with:clef:bass;key:\"C major\""
        result = SearchProcessor.process(input)
        self.assertEqual({"clef": {"clarinet": ["bass"]}, "key": {
                         "clarinet": ["C major"]}, "instrument": ["clarinet"]}, result)

    def testSemiColonKeyThenClef(self):
        input = "instrument:clarinet with:key:\"C major\";clef:bass"
        result = SearchProcessor.process(input)
        self.assertEqual({"instrument": ["clarinet"],
                          "clef": {"clarinet": ["bass"]},
                          "key": {"clarinet": ["C major"]}},
                         result)

    def testSpecificAndGeneralUsingWithKeyword(self):
        input = "instrument:clarinet with:clef:bass clef:treble"
        self.assertEqual({"instrument": ["clarinet"], "clef": {
                         "clarinet": ["bass"], "other": ["treble"]}}, SearchProcessor.process(input))

    def testSpecificKeyAndGeneralUsingWithKeyword(self):
        input = "instrument:clarinet with:key:\"C major\" key:\"D major\""
        self.assertEqual({"instrument": ["clarinet"],
                          "key": {"clarinet": ["C major"],
                                  "other": ["D major"]}},
                         SearchProcessor.process(input))

    def testSpecificInstrumentInclSpace(self):
        input = "instrument:\"MusicXML Part\""
        self.assertEqual(
            {"instrument": ["MusicXML Part"]}, SearchProcessor.process(input))
