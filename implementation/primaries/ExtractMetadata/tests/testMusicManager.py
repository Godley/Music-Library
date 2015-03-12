import unittest
from implementation.primaries.ExtractMetadata.classes import MusicManager

class testMusicManager(unittest.TestCase):
    def setUp(self):
        self.manager = MusicManager.MusicManager()
