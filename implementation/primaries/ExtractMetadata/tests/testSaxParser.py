from implementation.primaries.ExtractMetadata.classes import Extractor
import unittest
from xml.sax import make_parser, handler


test_file = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/accidentals.xml'
class Dummy(object):
    def __init__(self):
        self.tags = ["key","part-name","fifths","mode"]
        self.byTag = False
        self.tracked = {}
        self.file = test_file.split('/')[-1]

d = Dummy()
e = Extractor.Extractor(d, byTag = d.byTag)
parser = make_parser()
parser.setFeature(handler.feature_external_ges, False)
parser.setContentHandler(e)
fob = open(test_file, 'r')
parser.parse(fob)

class testExtractorByChars(unittest.TestCase):
    def setUp(self):
        self.tags = ["key","part-name","fifths","mode"]
        self.byTag = False

    def testKeys(self):
        self.assertTrue("C major" in d.tracked)

    def testPartname(self):
        self.assertTrue("Flute" in d.tracked)

    def testKeysChars(self):
        self.assertEqual("key", d.tracked["C major"]["tags"][0])

    def testKeysFile(self):
        self.assertEqual("accidentals.xml", d.tracked["C major"]["files"][0])

    def testPartChars(self):
        self.assertEqual("part-name", d.tracked["Flute"]["tags"][0])

    def testPartFile(self):
        self.assertEqual("accidentals.xml", d.tracked["Flute"]["files"][0])