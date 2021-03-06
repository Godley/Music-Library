from implementation.primaries.ExtractMetadata.classes import MusicManager
import unittest
import os
from implementation.primaries import ExtractMetadata


class TestUnzipper(unittest.TestCase):

    def setUp(self):
        self.folder = os.path.join(
            os.path.dirname(
                ExtractMetadata.__file__),
            'tests',
            'test_files',
            'unzip_tests')
        files = ['zip_test_1.mxl', 'zip_test_2.mxl']
        self.unzipper = MusicManager.Unzipper(folder=self.folder, files=files)

    def testOutputList(self):
        self.assertEqual(
            self.unzipper.createOutputList(), [
                'zip_test_1.xml', 'zip_test_2.xml'])

    def testXMLFileCreation(self):
        xml_files = []
        self.unzipper.unzipInputFiles()
        for root, dirs, files in os.walk(os.path.join(self.folder)):
            for file in files:
                if file.endswith(".xml"):
                    xml_files.append(file)
        self.assertEqual(len(xml_files), 3)

    def testXMLFileRenaming(self):
        expected = ['zip_test_2.xml', 'zip_test_1.xml', 'META-INF']
        expected_paths = [
            os.path.join(
                self.folder,
                new_file) for new_file in expected]
        self.unzipper.unzip()
        self.assertTrue(os.path.exists(expected_paths[0]))
        self.assertTrue(os.path.exists(expected_paths[1]))
        self.assertFalse(os.path.exists(expected_paths[2]))

    def tearDown(self):
        new_files = ['zip_test_2.xml', 'zip_test_1.xml']
        paths = [os.path.join(self.folder, new_file) for new_file in new_files]
        for path in paths:
            if os.path.exists(path):
                os.remove(path)
