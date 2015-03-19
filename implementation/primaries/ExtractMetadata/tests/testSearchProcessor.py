import unittest
from implementation.primaries.ExtractMetadata.classes import SearchProcessor

class testSearchProcessor(unittest.TestCase):
    def setUp(self):
        self.processor = SearchProcessor.SearchProcessor()

    def testTitleOrComposerOrLyricist(self):
        input = "hello, world"
        self.assertEqual({"text":["hello,","world"]}, self.processor.process(input))

    def testFilename(self):
        input = "lottie.xml"
        self.assertEqual({"filename":[input]}, self.processor.process(input))

    def testTimeSig(self):
        input = "4/4"
        self.assertEqual({"time":["4/4"]}, self.processor.process(input))

    def testTimeSigWithMeterLabel(self):
        input = "meter:4/4"
        self.assertEqual({"time":["4/4"]}, self.processor.process(input))

    def testTempo(self):
        input = "quarter=half"
        self.assertEqual({"tempo":["quarter=half"]}, self.processor.process(input))

    def testInstrument(self):
        input = "instrument:clarinet"
        self.assertEqual({"instrument":["clarinet"]}, self.processor.process(input))

    def testKey(self):
        input = "C major"
        self.assertEqual({"key":{"other":["C major"]}}, self.processor.process(input))

    def testTransposition(self):
        input = "transposition:clarinet"
        self.assertEqual({"transposition":["clarinet"]}, self.processor.process(input))

    def testWithKey(self):
        input = "instrument:clarinet with:key:\"C major\""
        self.assertEqual({"instrument":["clarinet"], "key":{"clarinet":["C major"]}}, self.processor.process(input))

    def testWithClef(self):
        input = "instrument:clarinet with:clef:bass"
        self.assertEqual({"instrument":["clarinet"], "clef":{"clarinet":["bass"]}}, self.processor.process(input))

    def testSemiColon(self):
        input = "instrument:clarinet with:clef:bass;key:\"C major\""
        result = self.processor.process(input)
        self.assertEqual({"clef":{"clarinet":["bass"]}, "key":{"clarinet":["C major"]}, "instrument":["clarinet"]}, result)

    def testSemiColonKeyThenClef(self):
        input = "instrument:clarinet with:key:\"C major\";clef:bass"
        result = self.processor.process(input)
        self.assertEqual({"instrument":["clarinet"], "clef":{"clarinet":["bass"]}, "key":{"clarinet":["C major"]}}, result)

    def testSpecificAndGeneralUsingWithKeyword(self):
        input = "instrument:clarinet with:clef:bass clef:treble"
        self.assertEqual({"instrument":["clarinet"], "clef":{"clarinet":["bass"], "other":["treble"]}}, self.processor.process(input))

    def testSpecificKeyAndGeneralUsingWithKeyword(self):
        input = "instrument:clarinet with:key:\"C major\" key:\"D major\""
        self.assertEqual({"instrument":["clarinet"], "key":{"clarinet":["C major"], "other":["D major"]}}, self.processor.process(input))