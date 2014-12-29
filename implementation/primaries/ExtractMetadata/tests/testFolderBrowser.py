import unittest, os, shutil
from implementation.primaries.ExtractMetadata.classes import FolderBrowser

folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/metadata'
folderBrowser = FolderBrowser.Browser(folder=folder)

folderBrowser.CopyZippedFiles()

class testFolderBrowser(unittest.TestCase):
    def setUp(self):
        file_list = ['zip_test_1.mxl', 'zip_test_2.mxl']
        main_files = [os.path.join(folder, file) for file in file_list]

    def testXMLFileList(self):
        folderBrowser.Load()
        self.assertEqual(5, len(folderBrowser.xmlFiles))

    def testXMLFileNames(self):

        self.assertTrue("beams.xml" in folderBrowser.xmlFiles)
        self.assertTrue("breathMarks.xml" in folderBrowser.xmlFiles)

    def testMXLFileList(self):

        file_list = ['zip_test_1.mxl', 'zip_test_2.mxl']
        main_files = [os.path.join(folder, file) for file in file_list]
        for i in range(len(main_files)):
            if not os.path.exists(main_files[i]):
                shutil.copyfile(os.path.join(folder, "zipped", file_list[i]), main_files[i])
        folderBrowser.Load()
        self.assertEqual(2, len(folderBrowser.mxlFiles))

    def testMXLFileNames(self):
        self.assertTrue("zip_test_1.mxl" in folderBrowser.mxlFiles)
        self.assertTrue("zip_test_2.mxl" in folderBrowser.mxlFiles)

    def testHasZippedFolder(self):
        self.assertTrue(os.path.exists(os.path.join(folder, "zipped")))

    def testFilesCopied(self):
        self.assertTrue(os.path.exists(os.path.join(folder, "zipped", "zip_test_1.mxl")))
        self.assertTrue(os.path.exists(os.path.join(folder, "zipped", "zip_test_2.mxl")))

    def testFilesRemoved(self):
        folderBrowser.Load()
        folderBrowser.CopyZippedFiles()
        folderBrowser.removeCopiedFilesFromMainFolder()
        self.assertFalse(os.path.exists(os.path.join(folder, "zip_test_1.mxl")))
        self.assertFalse(os.path.exists(os.path.join(folder, "zip_test_2.mxl")))