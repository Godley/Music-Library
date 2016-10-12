import unittest
import os
import sys
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MusicManager


class TestMusicManager(object):

    def assert_dict(self, data, expected):
        for key in expected:
            assert key in data
            assert data[key] == expected[key]

    def testFindPieceByTitleAndComposer(self, manager, dummy):
        data = {
            "title": "Blabla", "composer": "Bartok"}
        data.update(dummy)
        data2 = {"title": "Blabla"}
        data2.update(dummy)
        manager.add_piece(
            "file.xml", data)
        manager.add_piece("file1.xml", data2)
        results = manager.runQueries(
            {"title": ["Blabla"], "composer": ["Bartok"]})
        expected_results = {
            'Composer: Bartok': [
                ('title: Blabla composer: Bartok filename: file.xml',
                 'file.xml')],
            'Exact Matches': [
                ('title: Blabla composer: Bartok filename: file.xml',
                 'file.xml')],
            'Title: Blabla': [
                ('title: Blabla composer: Bartok filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')]}
        self.assert_dict(
            expected_results,
            results)

    def testFindPieceByTitleAndLyricist(self, manager, dummy):
        data = {
            "title": "Blabla", "lyricist": "Bartok"}
        data.update(dummy)
        data2 = {"title": "Blabla"}
        data2.update(dummy)
        manager.add_piece("file.xml", data)
        manager.add_piece("file1.xml", data2)
        expected_results = {
            "Exact Matches": [
                ('title: Blabla lyricist: Bartok filename: file.xml',
                 'file.xml')],
            "Title: Blabla": [
                ('title: Blabla lyricist: Bartok filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')],
            "Lyricist: Bartok": [
                ('title: Blabla lyricist: Bartok filename: file.xml',
                 'file.xml')]}
        results = manager.runQueries(
            {"title": ["Blabla"], "lyricist": ["Bartok"]})
        self.assert_dict(
            expected_results,
            results)

    def testFindPieceByTitleAndKey(self, manager, clef_in, dummy):
        data = {"title": "Blabla", "instruments": [
            {"name": "Clarinet"}], "keys": {"Clarinet": [{"fifths": 1, "mode": "major"}]},
            "clefs": {"Clarinet": [clef_in]}}
        data2 = {"title": "Blabla"}
        data2.update(dummy)
        manager.add_piece("file.xml", data)
        manager.add_piece("file1.xml", data2)
        expected_results = {
            "Exact Matches": [
                ('title: Blabla filename: file.xml',
                 'file.xml')],
            "Title: Blabla": [
                ('title: Blabla filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')],
            "Keys": [
                ('title: Blabla filename: file.xml',
                 'file.xml')]}
        results = manager.runQueries(
            {
                "title": ["Blabla"], "keys": {
                    "other": [{"name": "G major"}]}})
        self.assert_dict(results, expected_results)

    def testFindPieceByTitleAndKeyAndClef(self, manager):
        manager.add_piece("file.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Clarinet"}],
                           "clefs": {"Clarinet": [{"name": "treble"}]},
                           "keys": {"Clarinet": [{"name": "C major"}]}})
        manager.add_piece("file1.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Clarinet"}],
                           "keys": {"Clarinet": [{"name": "C major"}]},
                           "clefs": {"Clarinet": [{"name": "bass"}]}})
        expected_results = {
            "Title: Blabla": [
                ('title: Blabla filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')],
            "Keys": [
                ('title: Blabla filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')],
            "Clefs": [
                ('title: Blabla filename: file.xml',
                 'file.xml')],
            "Exact Matches": [
                ('title: Blabla filename: file.xml',
                 'file.xml')]}
        results = manager.runQueries(
            {
                "title": ["Blabla"], "keys": {
                    "other": [{"name": "C major"}]}, "clefs": {
                    "other": [{"name": "treble"}]}})
        self.assert_dict(
            expected_results, results)

    def testFindPieceByTitleAndKeyAndClefAndInstrument(self, manager):
        manager.add_piece("file.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Clarinet"}],
                           "clefs": {"Clarinet": [{"name": "treble"}]},
                           "keys": {"Clarinet": [{"name": "C major"}]}})
        data = {"title": "Blabla",
                "instruments": [{"name": "Sax"}],
                "keys": {"Sax": [{"name": "C major"}]},
                "clefs": {"Sax": [{"name": "bass"}]}}

        manager.add_piece("file1.xml",
                          data)
        expected_results = {
            "Title: Blabla": [
                ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], "Clefs": [
                ('title: Blabla filename: file.xml', 'file.xml')], "Exact Matches": [
                ('title: Blabla filename: file.xml', 'file.xml')], "Keys": [
                ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], "Instruments": [
                ('title: Blabla filename: file.xml', 'file.xml')]}
        results = manager.runQueries(
            {
                "title": ["Blabla"], "keys": {
                    "other": [{"name": "C major"}]}, "clefs": {
                    "other": [{"name": "treble"}]}, "instrument": {
                    "Clarinet": {}}})
        self.assert_dict(results, expected_results)

    def testFindPieceByTitleAndInstrumentWithClef(self, manager):
        manager.add_piece("file.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Clarinet"}],
                           "clefs": {"Clarinet": [{"name": "treble"}]},
                           "keys": {"Clarinet": [{"name": "C major"}]}})
        manager.add_piece("file1.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Sax"},
                                           {"name": "Clarinet"}],
                           "clefs": {"Sax": [{"name": "treble"}],
                                     "Clarinet": [{"name": "bass"}]},
                           "keys": {"Sax": [{"name": "D major"}],
                                    "Clarinet": [{"name": "E major"}]}})
        expected_results = {
            'Instruments in Clefs': [
                ('title: Blabla filename: file.xml', 'file.xml')], 'Exact Matches': [
                ('title: Blabla filename: file.xml', 'file.xml')], 'Instruments': [
                ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], 'Keys': [
                ('title: Blabla filename: file.xml', 'file.xml')], 'Title: Blabla': [
                ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')]}

        results = manager.runQueries(
            {
                "title": ["Blabla"], "keys": {
                    "other": [{"name": "C major"}]}, "clefs": {
                    "Clarinet": [{"name": "treble"}]}, "instrument": {
                    "Clarinet": {}}})
        self.assert_dict(results, expected_results)

    def testFindPieceByTitleAndInstrumentWithClefAndOther(self, manager):
        manager.add_piece("file.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Clarinet"},
                                           {"name": "Sax"}],
                           "clefs": {"Clarinet": [{"sign": "G",
                                                   "line": 2}],
                                     "Sax": [{"line": 4,
                                              "sign": "F"}]},
                           "keys": {"Clarinet": [{"name": "C major"}],
                                    "Sax": [{"name": "A major"}]}})
        manager.add_piece("file1.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Sax"},
                                           {"name": "Clarinet"}],
                           "clefs": {"Sax": [{"line": 4,
                                              "sign": "F"}],
                                     "Clarinet": [{"name": "alto"}]},
                           "keys": {"Sax": [{"name": "A major"}],
                                    "Clarinet": [{"name": "A major"}]}})
        expected_results = {
            'Exact Matches': [
                ('title: Blabla filename: file.xml', 'file.xml')], 'Title: Blabla': [
                ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], 'Instruments in Clefs': [
                ('title: Blabla filename: file.xml', 'file.xml')], 'Keys': [
                ('title: Blabla filename: file.xml', 'file.xml')], 'Instruments': [
                ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')], 'Clefs': [
                ('title: Blabla filename: file.xml', 'file.xml'), ('title: Blabla filename: file1.xml', 'file1.xml')]}

        results = manager.runQueries(
            {
                "title": ["Blabla"], "keys": {
                    "other": [{"name": "C major"}]}, "clefs": {
                    "Clarinet": [{"name": "treble"}], "other": [{"name": "bass"}]}, "instrument": {
                    "Clarinet": {}}})
        self.assert_dict(results, expected_results)

    def testFindPieceByTitleAndInstrumentWithKey(self, manager):
        manager.add_piece("file.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Clarinet"},
                                           {"name": "Sax"}],
                           "clefs": {"Clarinet": [{"sign": "G",
                                                   "line": 2}],
                                     "Sax": [{"line": 4,
                                              "sign": "F"}]},
                           "keys": {"Clarinet": [{"fifths": 2,
                                                  "mode": "major"}],
                                    "Sax": [{"name": "C major"}]}})
        manager.add_piece("file1.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Sax"},
                                           {"name": "Clarinet"}],
                           "keys": {"Sax": [{"fifths": 2,
                                             "mode": "major"}],
                                    "Clarinet": [{"name": "A major"}]},
                           "clefs": {"Sax": [{"line": 4,
                                              "sign": "F"}],
                                     "Clarinet": [{"name": "treble"}]}})
        expected_results = {
            "Title: Blabla": [
                ('title: Blabla filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')],
            "Exact Matches": [
                ('title: Blabla filename: file.xml',
                 'file.xml')],
            "Instruments in Keys": [
                ('title: Blabla filename: file.xml',
                 'file.xml')]}

        results = manager.runQueries(
            {
                "title": ["Blabla"], "keys": {
                    "Clarinet": [{"name": "D major"}]}, "instrument": {"Clarinet": {}}})
        self.assert_dict(results, expected_results)

    def testFindPieceByTitleAndInstrumentWithKeyAndOther(self, manager):
        manager.add_piece("file.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Clarinet"},
                                           {"name": "Sax"}],
                           "clefs": {"Clarinet": [{"sign": "G",
                                                   "line": 2}],
                                     "Sax": [{"line": 4,
                                              "sign": "F"}]},
                           "keys": {"Clarinet": [{"fifths": 2,
                                                  "mode": "major"}],
                                    "Sax": [{"fifths": 0,
                                             "mode": "major"}]}})
        manager.add_piece("file1.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Sax"},
                                           {"name": "Clarinet"}],
                           "keys": {"Sax": [{"fifths": 0,
                                             "mode": "major"},
                                            {"fifths": 2,
                                             "mode": "major"}],
                                    "Clarinet": [{"name": "A major"}]},
                           "clefs": {"Sax": [{"line": 4,
                                              "sign": "F"}],
                                     "Clarinet": [{"name": "treble"}]}})
        expected_results = {
            "Title: Blabla": [
                ('title: Blabla filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')],
            "Exact Matches": [
                ('title: Blabla filename: file.xml',
                 'file.xml')],
            "Keys": [
                ('title: Blabla filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')],
            "Instruments in Keys": [
                ('title: Blabla filename: file.xml',
                 'file.xml')]}
        results = manager.runQueries(
            {
                "title": ["Blabla"], "keys": {
                    "Clarinet": [{"name": "D major"}],
                    "other": [{"name": "C major"}]},
                "instrument": [{"name": "Clarinet"}]})
        self.assert_dict(results, expected_results)

    def testFindPieceByTitleAndInstrumentWithKeyAndClef(self, manager):
        manager.add_piece("file.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Clarinet"},
                                           {"name": "Sax"}],
                           "clefs": {"Clarinet": [{"sign": "G",
                                                   "line": 2}],
                                     "Sax": [{"line": 4,
                                              "sign": "F"}]},
                           "keys": {"Clarinet": [{"fifths": 2,
                                                  "mode": "major"}],
                                    "Sax": [{"name": "D major"}]}})
        manager.add_piece("file1.xml",
                          {"title": "Blabla",
                           "instruments": [{"name": "Sax"},
                                           {"name": "Clarinet"}],
                           "keys": {"Clarinet": [{"fifths": 2,
                                                  "mode": "major"}],
                                    "Sax": [{"name": "A major"}]},
                           "clefs": {"Sax": [{"line": 4,
                                              "sign": "F"}],
                                     "Clarinet": [{"name": "treble"}]}})
        expected_results = {
            "Title: Blabla": [
                ('title: Blabla filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')],
            "Exact Matches": [
                ('title: Blabla filename: file.xml',
                 'file.xml')],
            "Instruments in Clefs": [
                ('title: Blabla filename: file.xml',
                 'file.xml')],
            "Instruments in Keys": [
                ('title: Blabla filename: file.xml',
                 'file.xml'),
                ('title: Blabla filename: file1.xml',
                 'file1.xml')]}
        results = manager.runQueries(
            {
                "title": ["Blabla"], "keys": {
                    "Clarinet": [{"name": "D major"}]}, "instrument": ["Clarinet"], "clefs": {
                    "Clarinet": [{"name": "treble"}]}})
        self.assert_dict(results, expected_results)

    def testFindByTextTitle(self, manager, dummy):
        title = "hello, world"
        data = {"title": "hello"}
        data.update(dummy)
        data2 = {"title": "hello, world"}
        data2.update(dummy)
        manager.add_piece("file.xml", data)
        manager.add_piece("file1.xml", data2)
        result = manager.runQueries({"text": title.split(" ")})
        expected_result = {
            "Title": [
                ('title: hello, world filename: file1.xml', 'file1.xml')], "Exact Matches": [
                ('title: hello, world filename: file1.xml', 'file1.xml')]}
        self.assert_dict(result, expected_result)

    def testFindByInstrumentsWithNoLabel(self, manager, dummy):
        query = {"text": ["clarinet", "flute"]}
        data = {"instruments": [{"name": "clarinet"}],
                "clefs": {"clarinet": [{"name": "treble"}]},
                "keys": {"clarinet": [{"name": "C major"}]}}

        manager.add_piece("file1.xml", data)
        manager.add({"name": "flute"}, table="instruments")
        expected_results = {
            "Instrument: clarinet": [('filename: file1.xml', 'file1.xml')]}
        results = manager.runQueries(query)
        self.assert_dict(results, expected_results)

    def testFindByInstrumentsWithNoLabel2Entries(self, manager):
        query = {"text": ["clarinet", "flute"]}
        data = {"instruments": [{"name": "clarinet"}],
                "clefs": {"clarinet": [{"name": "treble"}]},
                "keys": {"clarinet": [{"name": "C major"}]}}
        data2 = {"instruments": [
            {"name": "clarinet"}, {"name": "flute"}],
            "clefs": {"clarinet": [{"name": "treble"}],
                      "flute": [{"name": "treble"}]},
            "keys": {"clarinet": [{"name": "C major"}],
                     "flute": [{"name": "C major"}]}}
        manager.add_piece("file1.xml",
                          data)
        manager.add_piece("file2.xml", data2)
        expected_results = {
            "All Instruments": [
                ('filename: file2.xml', 'file2.xml')], "Exact Matches": [
                ('filename: file2.xml', 'file2.xml')], "Instrument: clarinet": [
                ('filename: file1.xml', 'file1.xml'), ('filename: file2.xml', 'file2.xml')], "Instrument: flute": [
                    ('filename: file2.xml', 'file2.xml')]}
        results = manager.runQueries(query)
        self.assert_dict(results, expected_results)
