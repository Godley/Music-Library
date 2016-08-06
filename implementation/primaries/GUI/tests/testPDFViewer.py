import unittest
from implementation.primaries.GUI.pdfViewer import PDFViewer
import os


class testPDFViewer(unittest.TestCase):
    def setUp(self):
        self.viewer = PDFViewer()
        self.test_file = os.path.join(os.getcwd(), 'resources',
            'FortheDancingandtheDreaming_update.pdf')
        self.viewer.setPDF(self.test_file)

    def testGetPages(self):
        expected_pages = 3
        result = self.viewer.getNumPages()
        self.assertEqual(expected_pages, result)

    def testGetPairings(self):
        expected_pairings = 2
        result = self.viewer.getNumGroups()
        self.assertEqual(expected_pairings, result)

    def testGetPageNotInDoc(self):
        self.assertIsNone(self.viewer.getPage(2))