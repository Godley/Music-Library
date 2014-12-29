import unittest, os, shutil
from implementation.primaries.ExtractMetadata.classes import Unzipper

folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/metadata'
zip_folder = os.path.join(folder, "zipped")
unzipper = Unzipper.Unzipper(zip_folder = zip_folder, dest=folder)


class testUnzipper(unittest.TestCase):
    def setUp(self):
        self.file_list = ['zip_test_1.mxl', 'zip_test_2.mxl']

    def testFileList(self):
        file_list = ['zip_test_1.mxl', 'zip_test_2.mxl']
        main_files = [os.path.join(folder, file) for file in file_list]
        for i in range(len(main_files)):
            if not os.path.exists(main_files[i]):
                shutil.copyfile(os.path.join(folder, "zipped", file_list[i]), main_files[i])
        unzipper.Load()
        self.assertEqual(2, len(unzipper.fileList))

    def testFileNames(self):
        for file in self.file_list:
            self.assertTrue(file in unzipper.fileList)

    def testFilesCreated(self):
        unzipper.Load()
        unzipper.Unzip()
        for file in self.file_list:
            new_file = file.split('.')[0] + ".xml"
            self.assertTrue(os.path.exists(os.path.join(folder, new_file)))

    def testFilesAreFiles(self):
        unzipper.Load()
        unzipper.Unzip()
        for file in self.file_list:
            new_file = file.split('.')[0] + ".xml"
            self.assertTrue(os.path.isfile(os.path.join(folder, new_file)))
