
import unittest
import os
from implementation.primaries.ExtractMetadata.classes import MusicManager

manager = MusicManager.MusicManager(None, folder=os.getcwd())
result_set = manager.parseApiFiles()

class TestMusicManagerWithApiIntegration(unittest.TestCase):
    """
    tests which confirm functionality of API manager inside the musicmanager class
    separated from music manager tests because these take longer on a slow internet connection
    """
    def setUp(self):
        self.manager = MusicManager.MusicManager(None, folder=os.getcwd())
        self.result_set = result_set
        self.file_list = manager.unzipApiFiles(self.result_set)

    def testUnzipData(self):
        dir = os.getcwd()
        for source in self.file_list:
            for file in self.file_list[source]:
                self.assertTrue(os.path.exists(os.path.join(dir, file)))

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

    def testCleanup(self):
        dir = os.getcwd()
        extensions = ['mxl', 'xml']
        for source in result_set:
            for file in result_set[source]:
                for ext in extensions:
                    file_ext = file.split(".")[0]+"."+ext
                    self.assertTrue(os.path.exists(os.path.join(dir, file_ext)))

        self.manager.cleanupApiFiles(result_set, extensions=extensions)
        for source in result_set:
            for file in result_set[source]:
                for ext in extensions:
                    file_ext = file.split(".")[0]+"."+ext
                    self.assertFalse(os.path.exists(os.path.join(dir, file_ext)))

    def tearDown(self):
        self.manager.cleanupApiFiles(result_set)
        os.remove(os.path.join(os.getcwd(), "music.db"))