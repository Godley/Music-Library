from implementation.primaries.ExtractMetadata.classes import Extractor
import unittest
from xml.sax import make_parser, handler

test_file = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/accidentals.xml'

class Dummy(object):
    def __init__(self, byTag = False, file='/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/accidentals.xml'):
        self.tags = ["key","part-name","fifths","mode"]
        self.byTag = byTag
        self.tracked = {}
        self.file = file.split('/')[-1]

class byTag(object):
    def __init__(self):
        self.parse_class = Dummy(byTag=True)
        self.extractor = Extractor.Extractor(self.parse_class, byTag = self.parse_class.byTag)
        self.parser = make_parser()
        self.parser.setFeature(handler.feature_external_ges, False)
        self.parser.setContentHandler(self.extractor)
        self.fob = open(test_file, 'r')
        self.parser.parse(self.fob)

class byChars(object):
    def __init__(self):
        self.parse_class = Dummy()
        self.extractor = Extractor.Extractor(self.parse_class, byTag = self.parse_class.byTag)
        self.parser = make_parser()
        self.parser.setFeature(handler.feature_external_ges, False)
        self.parser.setContentHandler(self.extractor)
        self.fob = open(test_file, 'r')
        self.parser.parse(self.fob)

ByTagExtractor = byTag()
byCharsExtractor = byChars()

class testExtractorByChars(unittest.TestCase):
    def setUp(self):
        self.tags = ["key","part-name","fifths","mode"]
        self.byTag = False

    def testKeys(self):
        self.assertTrue("C major" in byCharsExtractor.parse_class.tracked)

    def testPartname(self):
        self.assertTrue("Flute" in byCharsExtractor.parse_class.tracked)

    def testKeysChars(self):
        self.assertEqual("key", byCharsExtractor.parse_class.tracked["C major"]["accidentals.xml"]["tag"])

    def testKeysFile(self):
        self.assertTrue("accidentals.xml" in byCharsExtractor.parse_class.tracked["C major"])

    def testPartChars(self):
        self.assertEqual("part-name", byCharsExtractor.parse_class.tracked["Flute"]["accidentals.xml"]["tag"])

    def testPartFile(self):
        self.assertTrue("accidentals.xml" in byCharsExtractor.parse_class.tracked["Flute"])


class testExtractorByTags(unittest.TestCase):
    def setUp(self):
        self.tags = ["key","part-name","fifths","mode"]
        self.byTag = False

    def testKeys(self):

        self.assertTrue("key" in ByTagExtractor.parse_class.tracked)

    def testPartname(self):
        self.assertTrue("part-name" in ByTagExtractor.parse_class.tracked)

    def testKeysChars(self):
        self.assertEqual("C major", ByTagExtractor.parse_class.tracked["key"]["accidentals.xml"]["value"])

    def testKeysFile(self):
        self.assertTrue("accidentals.xml" in ByTagExtractor.parse_class.tracked["key"])

    def testPartChars(self):
        self.assertEqual("Flute", ByTagExtractor.parse_class.tracked["part-name"]["accidentals.xml"]["value"])

    def testPartFile(self):
        self.assertTrue("accidentals.xml" in ByTagExtractor.parse_class.tracked["part-name"])

