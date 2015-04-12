
import unittest
import os
from implementation.primaries.ExtractMetadata.classes import MusicManager

manager = MusicManager.MusicManager()
result_set = manager.parseApiFiles()
file_list = manager.unzipApiFiles()
class TestMusicManagerWithApiIntegration(unittest.TestCase):
    """
    tests which confirm functionality of API manager inside the musicmanager class
    separated from music manager tests because these take longer on a slow internet connection
    """
    def setUp(self):
        self.manager = MusicManager.MusicManager()
        self.result_set = result_set

    def testUnzipData(self):
        for source in file_list:
            for file in file_list[source]:
                self.assertTrue(os.path.exists(file))

    def testParseData(self):
        self.assertTrue(len(self.result_set) > 0)
        for source in self.result_set:
            comp = {fname: self.result_set[source][fname] for fname in self.result_set[
                source] if "source" in self.result_set[source][fname]}
            self.assertEqual(len(comp), len(self.result_set[source]))

    def testTitleInResult(self):
        for source in self.result_set:
            for file in self.result_set[source]:
                self.assertTrue("title" in self.result_set[source][file])

    def testComposerInResult(self):
        for source in self.result_set:
            for file in self.result_set[source]:
                self.assertTrue("composer" in self.result_set[source][file])

    def testLyricistInResult(self):
        for source in self.result_set:
            for file in self.result_set[source]:
                self.assertTrue("lyricist" in self.result_set[source][file])

    def testParseAddAndFind(self):
        self.manager.addApiFiles(result_set)
        results = self.manager.getFileList(online=True)
        self.assertEqual(len(results), len(self.result_set["MuseScore"]))
