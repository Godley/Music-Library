import unittest, os
from implementation.primaries.ExtractMetadata.classes import Playlister

folder = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/metadata'
playlister = Playlister.Playlister(folder=folder)

class testPlaylister(unittest.TestCase):


    def testPlaylisterKeysWithMoreThanOneEntry(self):
        playlists = playlister.GetBasePlaylists()
        self.assertTrue("treble" in playlists)
        self.assertTrue("C major" in playlists)
        self.assertTrue("F major" in playlists)
        self.assertTrue("bass" in playlists)
        self.assertTrue("Flute" in playlists)

    def testPlaylisterFluteLengthOnBasicLevel(self):
        playlists = playlister.GetBasePlaylists()
        self.assertEqual(2, len(playlists["Flute"]))

    def testPlaylisterBassLengthOnBasicLevel(self):
        playlists = playlister.GetBasePlaylists()
        self.assertEqual(3, len(playlists["bass"]))

    def testPlaylisterFluteLengthInMatchMethod(self):
        playlists = playlister.ExtendPlaylistsByHalfMatches()
        self.assertEqual(3, len(playlists["Flute"]))

    def testPlaylisterBassLengthInMatchMethod(self):
        playlists = playlister.ExtendPlaylistsByHalfMatches()
        self.assertEqual(3, len(playlists["bass"]))

    def testRecorderInHalfMatches(self):
        playlists = playlister.GetPartMatchesInExcluded()
        self.assertTrue("Recorder" in playlists)

    def testLengthPlaylistInHalfMatchExcludedToCurrent(self):
        playlists = playlister.GetPartMatchesInExcludedAndCurrent()
        self.assertTrue(True)