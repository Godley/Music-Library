import unittest
import os
import sys
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MusicManager
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict


class TestMusicManager(object):

    def testRunUnzipper(self, manager, manager_folder):
        manager.handleZips()
        assert os.path.exists(os.path.join(manager_folder, "file5.xml"))
        assert not os.path.exists(os.path.join(manager_folder, 'META-INF'))

    def testParseXMLFiles(self, manager, dummy):
        manager.addPiece("file.xml", dummy)
        manager.refreshWithoutDownload()
        manager.parseNewFiles = MagicMock(name='method')
        manager.parseOldFiles = MagicMock(name='method')
        manager.handleXMLFiles()
        expected = sorted(["file5.xml", "testcase2.xml"])
        manager.parseNewFiles.assert_called_once_with(expected)
        manager.parseOldFiles.assert_called_once_with(["file.xml"])

    def testParseFile(self, manager):
        manager.parseNewFiles(["testcase2.xml"])
        result = manager.getPieceInfo(["testcase2.xml"])[0]
        expected_result = {
            'filename': 'testcase2.xml',
            'keys': {
                'Piano': ['D major']},
            'tempos': [
                'half=quarter',
                'eighth.=80'],
            'clefs': {
                'Piano': [
                    'bass',
                    'alto',
                    'treble']},
            'title': 'my metaparsing testcase',
            'composer': 'charlotte godley',
            'lyricist': 'fran godley',
            'instruments': [
                            {'name': 'Piano',
                            'chromatic': None,
                            'diatonic': None}],
            'timesigs': ['4/4']}

        for key in expected_result:
            assert key in result
            assert type(result[key]) == type(expected_result[key])
            if isinstance(expected_result[key], dict):
                for elem in expected_result[key]:
                    assert elem in result[key]
                    assert type(
                            result[key]) == type(
                            expected_result[key])

                    if isinstance(expected_result[key][elem], list):
                        for member in expected_result[key][elem]:
                            assert member in result[key][elem]

                    else:
                        assert result[key][elem] == expected_result[key][elem]

            elif isinstance(expected_result[key], list):
                for elem in expected_result[key]:
                    assert elem in result[key]

            else:
                assert result[key] == expected_result[key]

        assert ["testcase2.xml"] == manager.get_file_list()

    def testHandleOldFiles(self, manager):
        manager.parseOldFiles(["file.xml"])
        assert manager.getPieceInfo(["file.xml"]) == []

    def testRefresh(self, manager, dummy):
        manager.addPiece("file.xml", dummy)
        manager.refreshWithoutDownload()
        assert manager.folder_browser.getNewAndOldFiles(
            manager.folder_browser.getFolderFiles())["old"] == ["file.xml"]

    def testCopyFiles(self, manager, manager_folder):
        path_to_primaries = []
        value = ''
        filepath = os.path.dirname(os.path.realpath(__file__))
        while value != 'ExtractMetadata':
            pair = os.path.split(filepath)
            filepath = pair[0]
            value = pair[1]
        path_to_primaries.append(filepath)
        path_to_primaries.append("SampleMusicXML")
        path_to_primaries.append("testcases")
        path_to_primaries.append("3repeats.xml")
        file = os.path.join(*path_to_primaries)
        manager.copyFiles([file])
        assert os.path.exists(
                os.path.join(
                    manager_folder,
                    "3repeats.xml"))
