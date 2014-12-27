import unittest
from implementation.primaries.ExtractMetadata.classes import FolderExtractor

folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/real scores'
Extractor = FolderExtractor.FolderExtractor(folder=folder)
Extractor.Load()

class testFolderExtractorByChars(unittest.TestCase):
    def setUp(self):

        self.indexes = ['Flute','Piccolo','C major','F major', 'treble', 'bass']

    def testIndexes(self):
        for id in self.indexes:
            self.assertTrue(id in Extractor.tracked)

    def testFilesInFlute(self):
        self.flute_list = ['beams.xml','breathMarks.xml']
        for name in self.flute_list:
            self.assertTrue(name in Extractor.tracked['Flute'])

    def testFilesInPiccolo(self):
        self.picc_list = ['zip_test_1.xml']
        for name in self.picc_list:
            self.assertTrue(name in Extractor.tracked['Piccolo'])

    def testFilesInCMajor(self):
        self.files = ['zip_test_1.xml','breathMarks.xml','beams.xml']
        for name in self.files:
            self.assertTrue(name in Extractor.tracked['C major'])

    def testFileInFMajor(self):
        self.assertTrue('zip_test_2.xml' in Extractor.tracked['F major'])

    def testFileInBass(self):
        self.assertTrue('zip_test_2.xml' in Extractor.tracked['bass'])

    def testFilesInTreble(self):
        self.files = ['zip_test_1.xml','breathMarks.xml','beams.xml', 'zip_test_2.xml']
        for file in self.files:
            self.assertTrue(file in Extractor.tracked['treble'])