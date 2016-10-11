import unittest
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MetaParser


class TestMetaParser(object):

    def testStartTag(self, parser):
        parser.startTag("part", {})
        assert parser.tags == ["part"]

    def testNewData(self, parser):
        parser.startTag("part", {})
        parser.newData("hello")
        assert parser.chars == {"part": "hello"}

    def testEndTag(self, parser):
        parser.startTag("part", {})
        parser.endTag("part")
        assert parser.tags == []


class TestAddPart(TestMetaParser):

    def testPartNameHandler(self, parser):
        parser.startTag("score-part", {})
        parser.startTag("part-name", {})
        assert MetaParser.make_new_part == parser.current_handler

    def testPartNameHandlerCall(self, parser):
        parser.startTag("score-part", {})
        parser.startTag("part-name", {})
        parser.current_handler = MagicMock(name="method")
        parser.newData("hello")
        parser.current_handler.assert_called_once_with(
            parser.tags,
            parser.attribs,
            parser.chars,
            parser.parts,
            parser.data)

    def testPartNameCreation(self, parser):
        parser.startTag("score-part", {"id": "P1"})
        parser.startTag("part-name", {})
        parser.newData("laura")
        assert parser.parts == {"P1": {"name": "laura"}}
        assert parser.data == {"instruments": ["laura"]}


class TestAddKey(TestMetaParser):

    def testPartNameHandler(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("key", {})
        assert MetaParser.handle_clef_or_key == parser.current_handler

    def testKeyHandlerCall(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("key", {})
        parser.current_handler = MagicMock(name="method")
        parser.newData("hello")
        parser.current_handler.assert_called_once_with(
            parser.tags,
            parser.attribs,
            parser.chars,
            parser.parts,
            parser.data)

    def testFifthsCreation(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("key", {})
        parser.startTag("fifths", {})
        parser.newData("5")
        assert parser.parts == {"P1": {"key": [{"fifths": 5}]}}

    def testModeCreation(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("key", {})
        parser.startTag("mode", {})
        parser.newData("major")
        assert parser.parts == {"P1": {"key": [{"mode": "major"}]}}

    def testFifthsAndModeCreation(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("key", {})
        parser.startTag("fifths", {})
        parser.newData("5")
        parser.endTag("fifths")
        parser.startTag("mode", {})
        parser.newData("major")
        assert parser.parts == {
            "P1": {"key": [{"fifths": 5, "mode": "major"}]}}


class TestAddClef(TestMetaParser):

    def setUp(self, parser):
        TestMetaParser.setUp(self, parser)

    def testClefHandler(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("clef", {})
        assert MetaParser.handle_clef_or_key == parser.current_handler

    def testClefHandlerCall(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("clef", {})
        parser.current_handler = MagicMock(name="method")
        parser.newData("hello")
        parser.current_handler.assert_called_once_with(
            parser.tags,
            parser.attribs,
            parser.chars,
            parser.parts,
            parser.data)

    def testSignCreation(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("clef", {})
        parser.startTag("sign", {})
        parser.newData("G")
        assert parser.parts == {"P1": {"clef": [{"sign": "G"}]}}

    def testLineCreation(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("clef", {})
        parser.startTag("line", {})
        parser.newData("2")
        assert parser.parts == {"P1": {"clef": [{"line": 2}]}}

    def testSignAndLineCreation(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("clef", {})
        parser.startTag("sign", {})
        parser.newData("G")
        parser.endTag("sign")
        parser.startTag("line", {})
        parser.newData("2")
        parser.endTag("line")
        assert parser.parts == {"P1": {"clef": [{"sign": "G", "line": 2}]}}


class TestAddTransposition(TestMetaParser):

    def setUp(self, parser):
        TestMetaParser.setUp(self, parser)

    def testTransHandler(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("transpose", {})
        assert parser.current_handler == MetaParser.handleTransposition

    def testTransCall(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("transpose", {})
        parser.startTag("diatonic", {})
        parser.current_handler = MagicMock(name="method")
        parser.newData("0")
        parser.current_handler.assert_called_once_with(
            parser.tags,
            parser.attribs,
            parser.chars,
            parser.parts,
            parser.data)

    def testTransDiatonic(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("transpose", {})
        parser.startTag("diatonic", {})
        parser.newData("0")
        assert parser.parts == {
            "P1": {
                "transposition": {
                    "diatonic": 0}}}

    def testTransChromatic(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("transpose", {})
        parser.startTag("chromatic", {})
        parser.newData("1")
        assert parser.parts == {
            "P1": {
                "transposition": {
                    "chromatic": 1}}}

    def testTransChromaticAndDiatonic(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("transpose", {})
        parser.startTag("diatonic", {})
        parser.newData("0")
        parser.endTag("diatonic")
        parser.startTag("chromatic", {})
        parser.newData("1")
        assert parser.parts == {
            "P1": {
                "transposition": {
                    "diatonic": 0, "chromatic": 1}}}


class TestAddMeter(TestMetaParser):

    def testMeterHandler(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("time", {})
        assert parser.current_handler == MetaParser.handleMeter

    def testMeterCall(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("time", {})
        parser.startTag("beats", {})
        parser.current_handler = MagicMock(name="method")
        parser.newData("4")
        parser.current_handler.assert_called_once_with(
            parser.tags,
            parser.attribs,
            parser.chars,
            parser.parts,
            parser.data)

    def testMeterBeat(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("time", {})
        parser.startTag("beats", {})
        parser.newData("4")
        assert parser.data == {"time_signatures": [{"beat": 4}]}

    def testMeterBeatType(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("time", {})
        parser.startTag("beat-type", {})
        parser.newData("4")
        assert parser.data == {"time_signatures": [{"beat_type": 4}]}

    def testMeterBeatAndBeatType(self, parser):
        parser.startTag("time", {})
        parser.startTag("beats", {})
        parser.newData("3")
        parser.endTag("beats")
        parser.startTag("beat-type", {})
        parser.newData("4")
        assert parser.data == {
            "time_signatures": [{"beat": 3, "beat_type": 4}]}

    def testMeterBeatTypeThenBeat(self, parser):
        parser.startTag("time", {})
        parser.startTag("beat-type", {})
        parser.newData("4")
        parser.endTag("beat-type")
        parser.startTag("beats", {})
        parser.newData("3")

        assert parser.data == {
            "time_signatures": [{"beat_type": 4, "beat": 3}]}


class TestAddTempo(TestMetaParser):

    def testTempoHandler(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("metronome", {})
        assert parser.current_handler == MetaParser.handle_tempo

    def testTempoCall(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("metronome", {})
        parser.startTag("beat-unit", {})
        parser.current_handler = MagicMock(name="method")
        parser.newData("quarter")
        parser.current_handler.assert_called_once_with(
            parser.tags,
            parser.attribs,
            parser.chars,
            parser.parts,
            parser.data)

    def testTempoBeat(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("metronome", {})
        parser.startTag("beat-unit", {})
        parser.newData("quarter")
        assert parser.data == {"tempos": [{"beat": "quarter"}]}

    def testTempoBeatType(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("metronome", {})
        parser.startTag("per-minute", {})
        parser.newData("100")
        assert parser.data == {"tempos": [{"minute": 100}]}

    def testTempoBeatAndPerMinute(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("metronome", {})
        parser.startTag("beat-unit", {})
        parser.newData("quarter")
        parser.endTag("beat-unit")
        parser.startTag("per-minute", {})
        parser.newData("100")
        assert parser.data == {"tempos": [{"beat": "quarter", "minute": 100}]}

    def testTempoBeatAndSecondBeat(self, parser):
        parser.startTag("part", {"id": "P1"})
        parser.startTag("metronome", {})
        parser.startTag("beat-unit", {})
        parser.newData("quarter")
        parser.endTag("beat-unit")
        parser.startTag("beat-unit", {})
        parser.newData("half")
        assert parser.data == {"tempos": [
            {"beat": "quarter", "beat_2": "half"}]}


class TestAddBibliography(TestMetaParser):

    def testBibHandler(self, parser):
        parser.startTag("movement-title", {})
        assert parser.current_handler == MetaParser.handleBibliography

    def testBibCall(self, parser):
        parser.startTag("movement-title", {})
        parser.current_handler = MagicMock(name="method")
        parser.newData("hello, world")
        parser.current_handler.assert_called_once_with(
            parser.tags,
            parser.attribs,
            parser.chars,
            parser.parts,
            parser.data)

    def testCreator(self, parser):
        parser.startTag("creator", {"type": "composer"})
        parser.newData("quarter")
        assert parser.data == {"composer": "quarter"}

    def testTitle(self, parser):
        parser.startTag("movement-title", {})
        parser.newData("100")
        assert parser.data == {"title": "100"}


class TestPartCollation(object):

    def testCollationOfTranspositions(self, parser):
        parser.parts = {"P1": {"name": "clarinet", "transposition": {}}}
        parser.data = {"instruments": ["clarinet"]}
        parser.collate_parts()
        assert parser.data == {"instruments": [{"name": "clarinet"}]}

    def testCollationOfKeys(self, parser):
        parser.parts = {"P1": {"name": "clarinet", "key": [{}]}}
        parser.data = {"instruments": ["clarinet"]}
        parser.collate_parts()
        assert parser.data == {"instruments": [{"name": "clarinet"}],
                               "keys": {"clarinet": [{}]}}

    def testCollationOfClefs(self, parser):
        parser.parts = {"P1": {"name": "clarinet", "clef": [{}]}}
        parser.data = {"instruments": ["clarinet"]}
        parser.collate_parts()
        assert parser.data == {"instruments": [{"name": "clarinet"}],
                               "clefs": {"clarinet": [{}]}}
