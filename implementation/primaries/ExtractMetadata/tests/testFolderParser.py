import unittest
from implementation.primaries.ExtractMetadata.classes import FolderParser
import shutil, os

folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/metadata'
parser = FolderParser.FolderParser(folder=folder)


class testFolderParser(unittest.TestCase):



    def testUnzipThenBrowse(self):
        parser.LoadFiles()
        parser.MoveZipFiles()
        parser.UnzipFiles()

        self.assertEqual(0, len(parser.ZipFiles))
        self.assertEqual(5, len(parser.MusicFiles))

    def testBrowse(self):
        shutil.copyfile(os.path.join(folder, "zipped", "zip_test_1.mxl"), os.path.join(folder, "zip_test_1.mxl"))
        shutil.copyfile(os.path.join(folder, "zipped", "zip_test_2.mxl"), os.path.join(folder, "zip_test_2.mxl"))
        os.remove(os.path.join(folder, "zip_test_2.xml"))
        os.remove(os.path.join(folder, "zip_test_1.xml"))
        parser.LoadFiles()
        self.assertEqual(2, len(parser.ZipFiles))
        self.assertEqual(3, len(parser.MusicFiles))

    def testMetaLoads(self):
        parser.MetaParse()
        self.assertEqual(13, len(parser.MusicData))
