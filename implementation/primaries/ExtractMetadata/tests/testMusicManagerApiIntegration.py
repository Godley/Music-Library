import unittest, os
from implementation.primaries.ExtractMetadata.classes import MusicManager

class testMusicManagerWithApiIntegration(unittest.TestCase):
    def setUp(self):
        self.manager = MusicManager.MusicManager()

    def testUnzipData(self):
        file_list = self.manager.unzipApiFiles()
        for source in file_list:
            for file in file_list[source]:
                self.assertTrue(os.path.exists(file))

    def testParseData(self):
        result_set = self.manager.parseApiFiles()
        self.assertTrue(len(result_set) > 0)
        for source in result_set:
            comp = {fname:result_set[source][fname] for fname in result_set[source] if "source" in result_set[source][fname]}
            self.assertEqual(len(comp), len(result_set[source]))
