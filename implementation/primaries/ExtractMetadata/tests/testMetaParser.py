import unittest
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MetaParser
from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict


class TestMetaParser(unittest.TestCase):

    def setUp(self):
        self.parser = MetaParser.MetaParser()

    def testStartTag(self):
        self.parser.startTag("part", {})
        self.assertEqual(self.parser.tags, ["part"])

    def testNewData(self):
        self.parser.startTag("part", {})
        self.parser.newData("hello")
        self.assertEqual(self.parser.chars, {"part": "hello"})

    def testEndTag(self):
        self.parser.startTag("part", {})
        self.parser.endTag("part")
        self.assertEqual(self.parser.tags, [])

    def tearDown(self):
        self.parser = None


class TestAddPart(TestMetaParser):

    def setUp(self):
        TestMetaParser.setUp(self)

    def testPartNameHandler(self):
        self.parser.startTag("score-part", {})
        self.parser.startTag("part-name", {})
        self.assertEqual(MetaParser.makeNewPart, self.parser.current_handler)

    def testPartNameHandlerCall(self):
        self.parser.startTag("score-part", {})
        self.parser.startTag("part-name", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.newData("hello")
        self.parser.current_handler.assert_called_once_with(
            self.parser.tags,
            self.parser.attribs,
            self.parser.chars,
            self.parser.parts,
            self.parser.data)

    def testPartNameCreation(self):
        self.parser.startTag("score-part", {"id": "P1"})
        self.parser.startTag("part-name", {})
        self.parser.newData("laura")
        self.assertEqual(self.parser.parts, {"P1": {"name": "laura"}})
        self.assertEqual(self.parser.data, {"instruments": ["laura"]})


class TestAddKey(TestMetaParser):

    def setUp(self):
        TestMetaParser.setUp(self)

    def testPartNameHandler(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("key", {})
        self.assertEqual(MetaParser.handle_clef_or_key, self.parser.current_handler)

    def testKeyHandlerCall(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("key", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.newData("hello")
        self.parser.current_handler.assert_called_once_with(
            self.parser.tags,
            self.parser.attribs,
            self.parser.chars,
            self.parser.parts,
            self.parser.data)

    def testFifthsCreation(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("key", {})
        self.parser.startTag("fifths", {})
        self.parser.newData("5")
        self.assertEqual(self.parser.parts, {"P1": {"key": [{"fifths": 5}]}})

    def testModeCreation(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("key", {})
        self.parser.startTag("mode", {})
        self.parser.newData("major")
        self.assertEqual(
            self.parser.parts, {"P1": {"key": [{"mode": "major"}]}})

    def testFifthsAndModeCreation(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("key", {})
        self.parser.startTag("fifths", {})
        self.parser.newData("5")
        self.parser.startTag("mode", {})
        self.parser.newData("major")
        self.assertEqual(
            self.parser.parts, {"P1": {"key": [{"fifths": 5, "mode": "major"}]}})


class TestAddClef(TestMetaParser):

    def setUp(self):
        TestMetaParser.setUp(self)

    def testClefHandler(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("clef", {})
        self.assertEqual(MetaParser.handle_clef_or_key, self.parser.current_handler)

    def testClefHandlerCall(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("clef", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.newData("hello")
        self.parser.current_handler.assert_called_once_with(
            self.parser.tags,
            self.parser.attribs,
            self.parser.chars,
            self.parser.parts,
            self.parser.data)

    def testSignCreation(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("clef", {})
        self.parser.startTag("sign", {})
        self.parser.newData("G")
        self.assertEqual(self.parser.parts, {"P1": {"clef": [{"sign": "G"}]}})

    def testLineCreation(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("clef", {})
        self.parser.startTag("line", {})
        self.parser.newData("2")
        self.assertEqual(self.parser.parts, {"P1": {"clef": [{"line": 2}]}})

    def testSignAndLineCreation(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("clef", {})
        self.parser.startTag("sign", {})
        self.parser.newData("G")
        self.parser.endTag("sign")
        self.parser.startTag("line", {})
        self.parser.newData("2")
        self.parser.endTag("line")
        self.assertEqual(
            self.parser.parts, {"P1": {"clef": [{"sign": "G", "line": 2}]}})


class TestAddTransposition(TestMetaParser):

    def setUp(self):
        TestMetaParser.setUp(self)

    def testTransHandler(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("transpose", {})
        self.assertEqual(
            self.parser.current_handler,
            MetaParser.handleTransposition)

    def testTransCall(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("transpose", {})
        self.parser.startTag("diatonic", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.newData("0")
        self.parser.current_handler.assert_called_once_with(
            self.parser.tags,
            self.parser.attribs,
            self.parser.chars,
            self.parser.parts,
            self.parser.data)

    def testTransDiatonic(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("transpose", {})
        self.parser.startTag("diatonic", {})
        self.parser.newData("0")
        self.assertEqual(
            self.parser.parts, {
                "P1": {
                    "transposition": {
                        "diatonic": 0}}})

    def testTransChromatic(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("transpose", {})
        self.parser.startTag("chromatic", {})
        self.parser.newData("1")
        self.assertEqual(
            self.parser.parts, {
                "P1": {
                    "transposition": {
                        "chromatic": 1}}})

    def testTransChromaticAndDiatonic(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("transpose", {})
        self.parser.startTag("diatonic", {})
        self.parser.newData("0")
        self.parser.endTag("diatonic")
        self.parser.startTag("chromatic", {})
        self.parser.newData("1")
        self.assertEqual(
            self.parser.parts, {
                "P1": {
                    "transposition": {
                        "diatonic": 0, "chromatic": 1}}})


class TestAddMeter(TestMetaParser):

    def setUp(self):
        TestMetaParser.setUp(self)

    def testMeterHandler(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("time", {})
        self.assertEqual(self.parser.current_handler, MetaParser.handleMeter)

    def testMeterCall(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("time", {})
        self.parser.startTag("beats", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.newData("4")
        self.parser.current_handler.assert_called_once_with(
            self.parser.tags,
            self.parser.attribs,
            self.parser.chars,
            self.parser.parts,
            self.parser.data)

    def testMeterBeat(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("time", {})
        self.parser.startTag("beats", {})
        self.parser.newData("4")
        self.assertEqual(self.parser.data, {"time": [{"beat": 4}]})

    def testMeterBeatType(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("time", {})
        self.parser.startTag("beat-type", {})
        self.parser.newData("4")
        self.assertEqual(self.parser.data, {"time": [{"type": 4}]})

    def testMeterBeatAndBeatType(self):
        self.parser.startTag("time", {})
        self.parser.startTag("beats", {})
        self.parser.newData("3")
        self.parser.endTag("beats")
        self.parser.startTag("beat-type", {})
        self.parser.newData("4")
        self.assertEqual(self.parser.data, {"time": [{"beat": 3, "type": 4}]})

    def testMeterBeatTypeThenBeat(self):
        self.parser.startTag("time", {})
        self.parser.startTag("beat-type", {})
        self.parser.newData("4")
        self.parser.endTag("beat-type")
        self.parser.startTag("beats", {})
        self.parser.newData("3")

        self.assertEqual(self.parser.data, {"time": [{"type": 4, "beat": 3}]})


class TestAddTempo(TestMetaParser):

    def setUp(self):
        TestMetaParser.setUp(self)

    def testTempoHandler(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("metronome", {})
        self.assertEqual(self.parser.current_handler, MetaParser.handle_tempo)

    def testTempoCall(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("metronome", {})
        self.parser.startTag("beat-unit", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.newData("quarter")
        self.parser.current_handler.assert_called_once_with(
            self.parser.tags,
            self.parser.attribs,
            self.parser.chars,
            self.parser.parts,
            self.parser.data)

    def testTempoBeat(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("metronome", {})
        self.parser.startTag("beat-unit", {})
        self.parser.newData("quarter")
        self.assertEqual(self.parser.data, {"tempo": [{"beat": "quarter"}]})

    def testTempoBeatType(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("metronome", {})
        self.parser.startTag("per-minute", {})
        self.parser.newData("100")
        self.assertEqual(self.parser.data, {"tempo": [{"minute": 100}]})

    def testTempoBeatAndPerMinute(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("metronome", {})
        self.parser.startTag("beat-unit", {})
        self.parser.newData("quarter")
        self.parser.endTag("beat-unit")
        self.parser.startTag("per-minute", {})
        self.parser.newData("100")
        self.assertEqual(
            self.parser.data, {"tempo": [{"beat": "quarter", "minute": 100}]})

    def testTempoBeatAndSecondBeat(self):
        self.parser.startTag("part", {"id": "P1"})
        self.parser.startTag("metronome", {})
        self.parser.startTag("beat-unit", {})
        self.parser.newData("quarter")
        self.parser.endTag("beat-unit")
        self.parser.startTag("beat-unit", {})
        self.parser.newData("half")
        self.assertEqual(
            self.parser.data, {"tempo": [{"beat": "quarter", "beat_2": "half"}]})


class TestAddBibliography(TestMetaParser):

    def setUp(self):
        TestMetaParser.setUp(self)

    def testBibHandler(self):
        self.parser.startTag("movement-title", {})
        self.assertEqual(
            self.parser.current_handler,
            MetaParser.handleBibliography)

    def testBibCall(self):
        self.parser.startTag("movement-title", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.newData("hello, world")
        self.parser.current_handler.assert_called_once_with(
            self.parser.tags,
            self.parser.attribs,
            self.parser.chars,
            self.parser.parts,
            self.parser.data)

    def testCreator(self):
        self.parser.startTag("creator", {"type": "composer"})
        self.parser.newData("quarter")
        self.assertEqual(self.parser.data, {"composer": "quarter"})

    def testTitle(self):
        self.parser.startTag("movement-title", {})
        self.parser.newData("100")
        self.assertEqual(self.parser.data, {"title": "100"})


class TestPartCollation(unittest.TestCase):

    def setUp(self):
        self.parser = MetaParser.MetaParser()

    def testCollationOfTranspositions(self):
        self.parser.parts = {"P1": {"name": "clarinet", "transposition": {}}}
        self.parser.data = {"instruments": ["clarinet"]}
        self.parser.collatePartsIntoData()
        self.assertEqual(
            self.parser.data, {"instruments": [{"name": "clarinet", "transposition": {}}]})

    def testCollationOfKeys(self):
        self.parser.parts = {"P1": {"name": "clarinet", "key": [{}]}}
        self.parser.data = {"instruments": ["clarinet"]}
        self.parser.collatePartsIntoData()
        self.assertEqual(self.parser.data,
                         {"instruments": [{"name": "clarinet"}],
                          "key": {"clarinet": {hashdict()}}})

    def testCollationOfClefs(self):
        self.parser.parts = {"P1": {"name": "clarinet", "clef": [{}]}}
        self.parser.data = {"instruments": ["clarinet"]}
        self.parser.collatePartsIntoData()
        self.assertEqual(self.parser.data,
                         {"instruments": [{"name": "clarinet"}],
                          "clef": {"clarinet": {hashdict()}}})
