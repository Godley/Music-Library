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
        self.assertEqual({"time_signature":["4/4"]}, self.processor.process(input))

    def testTempo(self):
        input = "quarter=half"
        self.assertEqual({"tempo":["quarter=half"]}, self.processor.process(input))

    def testInstrument(self):
        input = "instrument:clarinet"
        self.assertEqual({"instrument":["clarinet"]}, self.processor.process(input))
