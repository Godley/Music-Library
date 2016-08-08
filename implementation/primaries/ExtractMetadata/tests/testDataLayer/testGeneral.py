"""
there's a lot of tests in here, so I've sorted them a bit:
testDataLayerAdd: as the title suggests, checks adding pieces puts stuff in the right tables
testDataLayerUserPlaylists: anything relating to user created playlists, so stuff in the playlist and playlist join table
testDataLayerUserQueries: anything which will be used when a user types something into the search bar
testDataLayerGeneratePlaylists: anything which will be used to generate playlists of related data
testDataLayerGeneral: anything which doesn't fit into the other class categories so generally searching for specific pieces
testDataLayerOnlineSearching: anything relating to the diff between each method when online is set to false or true.
                                This is to confirm that API searching does not get mixed up with local searching
"""
import unittest
from implementation.primaries.ExtractMetadata.classes.DataLayer.MusicData import MusicData
import os

class TestDataLayerGeneral(unittest.TestCase):

    def setUp(self):
        self.data = MusicData("example.db")

    def tearDown(self):
        os.remove("example.db")

    def testGetAllPieces(self):
        self.data.addPiece("file.xml", {})
        self.data.addPiece("file2.xml", {})
        expecting = ["file.xml", "file2.xml"]
        result = self.data.getFileList()
        for item in expecting:
            self.assertTrue(item in result)

    def testGetAllPiecesWhereNoneExist(self):
        self.assertEqual([], self.data.getFileList())

    def testFindPieceByFname(self):
        self.data.addPiece("file.xml", {})
        self.assertEqual(
            (1, "file.xml", "", -1, -1), self.data.getExactPiece("file.xml"))

    def testFindAllInfoForAPiece(self):
        self.data.addPiece(
            "file.xml", {"tempo": [{"beat": "quarter", "beat_2": "half"}]})
        self.assertEqual([{"title": "",
                           "composer": -1,
                           "lyricist": -1,
                           "tempos": ["quarter=half"],
                           "filename":"file.xml"}],
                         self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasKeys(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "key": {
                           "clarinet": [{"mode": "major", "fifths": 2}]}})
        self.assertEqual([{"title": "",
                           "composer": -1,
                           "lyricist": -1,
                           "instruments": [{"name": "clarinet"}],
                           "keys": {"clarinet": ["D major"]},
                           "filename":"file.xml"}],
                         self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasClefs(self):
        self.data.addPiece("file.xml", {"instruments": [{"name": "clarinet"}], "clef": {
                           "clarinet": [{"sign": "G", "line": 2}]}})
        self.assertEqual([{"title": "",
                           "composer": -1,
                           "lyricist": -1,
                           "instruments": [{"name": "clarinet"}],
                           "clefs": {"clarinet": ["treble"]},
                           "filename":"file.xml"}],
                         self.data.getAllPieceInfo(["file.xml"]))

    def testFindAllInfoForAPieceWhereHasTransposedInstruments(self):
        self.data.addPiece("file.xml", {"instruments": [
                           {"name": "clarinet", "transposition": {"diatonic": -1, "chromatic": -2}}]})
        self.assertEqual([{"title": "",
                           "composer": -1,
                           "lyricist": -1,
                           "instruments": [{"name": "clarinet",
                                            "transposition": {"diatonic": -1,
                                                              "chromatic": -2}}],
                           "filename": "file.xml"}],
                         self.data.getAllPieceInfo(["file.xml"]))




