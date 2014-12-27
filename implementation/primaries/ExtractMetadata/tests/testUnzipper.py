import unittest, os
from implementation.primaries.ExtractMetadata.classes import Unzipper

folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/real scores'
zip_folder = os.path.join(folder, "zipped")
unzipper = Unzipper.Unzipper(zip_folder = zip_folder, dest=folder)
unzipper.Load()
unzipper.Unzip()

class testUnzipper(unittest.TestCase):
    def setUp(self):
        self.file_list = ['zip_test_1.mxl', 'zip_test_2.mxl']
    def testFileList(self):
        self.assertEqual(2, len(unzipper.fileList))

    def testFileNames(self):
        for file in self.file_list:
            self.assertTrue(file in unzipper.fileList)

    def testFilesCreated(self):
        for file in self.file_list:
            new_file = file.split('.')[0] + ".xml"
            self.assertTrue(os.path.exists(os.path.join(folder, new_file)))

    def testFilesAreFiles(self):
        for file in self.file_list:
            new_file = file.split('.')[0] + ".xml"
            self.assertTrue(os.path.isfile(os.path.join(folder, new_file)))
