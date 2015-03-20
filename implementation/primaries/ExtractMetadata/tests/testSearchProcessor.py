import unittest
from implementation.primaries.ExtractMetadata.classes import SearchProcessor

class testSearchProcessor(unittest.TestCase):

    def testTitleOrComposerOrLyricist(self):
        input = "hello, world"
        self.assertEqual({"text":["hello,","world"]}, SearchProcessor.process(input))

    def testFilename(self):
        input = "lottie.xml"
        self.assertEqual({"filename":[input]}, SearchProcessor.process(input))

    def testTimeSig(self):
        input = "4/4"
        self.assertEqual({"time":["4/4"]}, SearchProcessor.process(input))

    def testTimeSigWithMeterLabel(self):
        input = "meter:4/4"
        self.assertEqual({"time":["4/4"]}, SearchProcessor.process(input))

    def testTempo(self):
        input = "quarter=half"
        self.assertEqual({"tempo":["quarter=half"]}, SearchProcessor.process(input))

    def testInstrument(self):
        input = "instrument:clarinet"
        self.assertEqual({"instrument":["clarinet"]}, SearchProcessor.process(input))

    def testKey(self):
        input = "C major"
        self.assertEqual({"key":{"other":["C major"]}}, SearchProcessor.process(input))

    def testTransposition(self):
        input = "transposition:clarinet"
        self.assertEqual({"transposition":["clarinet"]}, SearchProcessor.process(input))

    def testWithKey(self):
        input = "instrument:clarinet with:key:\"C major\""
        self.assertEqual({"instrument":["clarinet"], "key":{"clarinet":["C major"]}}, SearchProcessor.process(input))

    def testWithClef(self):
        input = "instrument:clarinet with:clef:bass"
        self.assertEqual({"instrument":["clarinet"], "clef":{"clarinet":["bass"]}}, SearchProcessor.process(input))

    def testSemiColon(self):
        input = "instrument:clarinet with:clef:bass;key:\"C major\""
        result = SearchProcessor.process(input)
        self.assertEqual({"clef":{"clarinet":["bass"]}, "key":{"clarinet":["C major"]}, "instrument":["clarinet"]}, result)

    def testSemiColonKeyThenClef(self):
        input = "instrument:clarinet with:key:\"C major\";clef:bass"
        result = SearchProcessor.process(input)
        self.assertEqual({"instrument":["clarinet"], "clef":{"clarinet":["bass"]}, "key":{"clarinet":["C major"]}}, result)

    def testSpecificAndGeneralUsingWithKeyword(self):
        input = "instrument:clarinet with:clef:bass clef:treble"
        self.assertEqual({"instrument":["clarinet"], "clef":{"clarinet":["bass"], "other":["treble"]}}, SearchProcessor.process(input))

    def testSpecificKeyAndGeneralUsingWithKeyword(self):
        input = "instrument:clarinet with:key:\"C major\" key:\"D major\""
        self.assertEqual({"instrument":["clarinet"], "key":{"clarinet":["C major"], "other":["D major"]}}, SearchProcessor.process(input))

    def testSpecificInstrumentInclSpace(self):
        input = "instrument:\"MusicXML Part\""
        self.assertEqual({"instrument":["MusicXML Part"]}, SearchProcessor.process(input))