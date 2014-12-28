import unittest, os
from implementation.primaries.ExtractMetadata.classes import FolderExtractor

folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/metadata'
Extractor = FolderExtractor.FolderExtractor(folder=folder)
Extractor.Load()
ExtractorByTag = FolderExtractor.FolderExtractor(folder=folder,byTag=True)
ExtractorByTag.Load()

class testFolderExtractorByChars(unittest.TestCase):
    def setUp(self):
        self.indexes = ['Flute','Piccolo','C major','F major', 'treble', 'bass']

        Extractor.Load()
        if os.path.exists(os.path.join(folder, '.extractedchars')):
            os.remove(os.path.join(folder, '.extractedchars'))

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

    def testPickler(self):
        if os.path.exists(os.path.join(folder, '.extractedchars')):
            os.remove(os.path.join(folder, '.extractedchars'))
        file = os.path.join(folder, '.extractedchars')
        print(file)
        self.assertFalse(os.path.exists(file))
        Extractor.Save()
        self.assertTrue(os.path.exists(file))

    def testUnpickler(self):
        Extractor.Save()
        Extractor.Empty()
        self.assertEqual(0, len(Extractor.tracked.keys()))
        Extractor.LoadCache()
        self.assertEqual(13, len(Extractor.tracked.keys()))

class testFolderExtractorByTag(unittest.TestCase):
    def setUp(self):
        self.indexes = ['part-name','key','clef']

        ExtractorByTag.Load()
        if os.path.exists(os.path.join(folder, '.extractedtags')):
            os.remove(os.path.join(folder, '.extractedtags'))

    def testIndexes(self):
        for id in self.indexes:
            self.assertTrue(id in ExtractorByTag.tracked)

    def testFilesInPartname(self):
        self.flute_list = ['beams.xml','breathMarks.xml','zip_test_1.xml']
        for name in self.flute_list:
            self.assertTrue(name in ExtractorByTag.tracked['part-name'])

    def testFilesInKey(self):
        self.key_list = ['beams.xml','breathMarks.xml','zip_test_1.xml','zip_test_2.xml']
        for name in self.key_list:
            self.assertTrue(name in ExtractorByTag.tracked['key'])

    def testFilesInClef(self):
        self.clef_list = ['beams.xml','breathMarks.xml','zip_test_1.xml','zip_test_2.xml']
        for name in self.clef_list:
            self.assertTrue(name in ExtractorByTag.tracked['clef'])

    def testPickler(self):
        if os.path.exists(os.path.join(folder, '.extractedtags')):
            os.remove(os.path.join(folder, '.extractedtags'))
        data_file = os.path.join(folder, '.extractedtags')
        print(os.path.exists(data_file))
        self.assertFalse(os.path.exists(data_file))
        ExtractorByTag.Save()
        self.assertTrue(os.path.exists(data_file))

    def testUnpickler(self):
        ExtractorByTag.Save()
        ExtractorByTag.Empty()
        self.assertEqual(0, len(ExtractorByTag.tracked.keys()))
        ExtractorByTag.LoadCache()
        self.assertEqual(3, len(ExtractorByTag.tracked.keys()))
