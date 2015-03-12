import unittest
from unittest.mock import MagicMock
from implementation.primaries.ExtractMetadata.classes import MetaParser

class testMetaParser(unittest.TestCase):
    def setUp(self):
        self.parser = MetaParser.MetaParser()

    def testStartTag(self):
        self.parser.StartTag("part", {})
        self.assertEqual(self.parser.tags, ["part"])

    def testNewData(self):
        self.parser.StartTag("part", {})
        self.parser.NewData("hello")
        self.assertEqual(self.parser.chars, {"part":"hello"})

    def testEndTag(self):
        self.parser.StartTag("part",{})
        self.parser.EndTag("part")
        self.assertEqual(self.parser.tags, [])

    def tearDown(self):
        self.parser = None

class testAddPart(testMetaParser):
    def setUp(self):
        testMetaParser.setUp(self)

    def testPartNameHandler(self):
        self.parser.StartTag("score-part", {})
        self.parser.StartTag("part-name",{})
        self.assertEqual(MetaParser.makeNewPart, self.parser.current_handler)

    def testPartNameHandlerCall(self):
        self.parser.StartTag("score-part", {})
        self.parser.StartTag("part-name",{})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.NewData("hello")
        self.parser.current_handler.assert_called_once_with(self.parser.tags, self.parser.attribs, self.parser.chars, self.parser.parts, self.parser.data)

    def testPartNameCreation(self):
        self.parser.StartTag("score-part", {"id":"P1"})
        self.parser.StartTag("part-name", {})
        self.parser.NewData("laura")
        self.assertEqual(self.parser.parts, {"P1":{"name":"laura"}})
        self.assertEqual(self.parser.data, {"instruments":["laura"]})

class testAddKey(testMetaParser):
    def setUp(self):
        testMetaParser.setUp(self)

    def testPartNameHandler(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("key", {})
        self.assertEqual(MetaParser.handleKey, self.parser.current_handler)

    def testKeyHandlerCall(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("key", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.NewData("hello")
        self.parser.current_handler.assert_called_once_with(self.parser.tags, self.parser.attribs, self.parser.chars, self.parser.parts, self.parser.data)

    def testFifthsCreation(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("key", {})
        self.parser.StartTag("fifths",{})
        self.parser.NewData("5")
        self.assertEqual(self.parser.parts, {"P1":{"key":[{"fifths":5}]}})

    def testModeCreation(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("key", {})
        self.parser.StartTag("mode",{})
        self.parser.NewData("major")
        self.assertEqual(self.parser.parts, {"P1":{"key":[{"mode":"major"}]}})

    def testFifthsAndModeCreation(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("key", {})
        self.parser.StartTag("fifths",{})
        self.parser.NewData("5")
        self.parser.StartTag("mode",{})
        self.parser.NewData("major")
        self.assertEqual(self.parser.parts, {"P1":{"key":[{"fifths":5,"mode":"major"}]}})

class testAddClef(testMetaParser):
    def setUp(self):
        testMetaParser.setUp(self)

    def testClefHandler(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("clef", {})
        self.assertEqual(MetaParser.handleClef, self.parser.current_handler)

    def testClefHandlerCall(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("clef", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.NewData("hello")
        self.parser.current_handler.assert_called_once_with(self.parser.tags, self.parser.attribs, self.parser.chars, self.parser.parts, self.parser.data)

    def testSignCreation(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("clef", {})
        self.parser.StartTag("sign",{})
        self.parser.NewData("G")
        self.assertEqual(self.parser.parts, {"P1":{"clef":[{"sign":"G"}]}})

    def testLineCreation(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("clef", {})
        self.parser.StartTag("line",{})
        self.parser.NewData("2")
        self.assertEqual(self.parser.parts, {"P1":{"clef":[{"line":2}]}})

    def testSignAndLineCreation(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("clef", {})
        self.parser.StartTag("sign",{})
        self.parser.NewData("G")
        self.parser.EndTag("sign")
        self.parser.StartTag("line",{})
        self.parser.NewData("2")
        self.parser.EndTag("line")
        self.assertEqual(self.parser.parts, {"P1":{"clef":[{"sign":"G","line":2}]}})

class testAddTransposition(testMetaParser):
    def setUp(self):
        testMetaParser.setUp(self)

    def testTransHandler(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("transpose", {})
        self.assertEqual(self.parser.current_handler, MetaParser.handleTransposition)

    def testTransCall(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("transpose", {})
        self.parser.StartTag("diatonic", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.NewData("0")
        self.parser.current_handler.assert_called_once_with(self.parser.tags,self.parser.attribs,self.parser.chars,self.parser.parts,self.parser.data)

    def testTransDiatonic(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("transpose", {})
        self.parser.StartTag("diatonic", {})
        self.parser.NewData("0")
        self.assertEqual(self.parser.parts, {"P1":{"transposition":{"diatonic":0}}})

    def testTransChromatic(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("transpose", {})
        self.parser.StartTag("chromatic", {})
        self.parser.NewData("1")
        self.assertEqual(self.parser.parts, {"P1":{"transposition":{"chromatic":1}}})

    def testTransChromaticAndDiatonic(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("transpose", {})
        self.parser.StartTag("diatonic", {})
        self.parser.NewData("0")
        self.parser.EndTag("diatonic")
        self.parser.StartTag("chromatic",{})
        self.parser.NewData("1")
        self.assertEqual(self.parser.parts, {"P1":{"transposition":{"diatonic":0,"chromatic":1}}})

class testAddMeter(testMetaParser):
    def setUp(self):
        testMetaParser.setUp(self)

    def testMeterHandler(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("time", {})
        self.assertEqual(self.parser.current_handler, MetaParser.handleMeter)

    def testMeterCall(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("time", {})
        self.parser.StartTag("beats", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.NewData("4")
        self.parser.current_handler.assert_called_once_with(self.parser.tags,self.parser.attribs,self.parser.chars,self.parser.parts,self.parser.data)

    def testMeterBeat(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("time", {})
        self.parser.StartTag("beats", {})
        self.parser.NewData("4")
        self.assertEqual(self.parser.data, {"time":[{"beat":4}]})

    def testMeterBeatType(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("time", {})
        self.parser.StartTag("beat-type", {})
        self.parser.NewData("4")
        self.assertEqual(self.parser.data, {"time":[{"type":4}]})

    def testMeterBeatAndBeatType(self):
        self.parser.StartTag("time", {})
        self.parser.StartTag("beats", {})
        self.parser.NewData("3")
        self.parser.EndTag("beats")
        self.parser.StartTag("beat-type",{})
        self.parser.NewData("4")
        self.assertEqual(self.parser.data, {"time":[{"beat":3,"type":4}]})

    def testMeterBeatTypeThenBeat(self):
        self.parser.StartTag("time", {})
        self.parser.StartTag("beat-type",{})
        self.parser.NewData("4")
        self.parser.EndTag("beat-type")
        self.parser.StartTag("beats", {})
        self.parser.NewData("3")

        self.assertEqual(self.parser.data, {"time":[{"type":4,"beat":3}]})

class testAddTempo(testMetaParser):
    def setUp(self):
        testMetaParser.setUp(self)

    def testTempoHandler(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("metronome", {})
        self.assertEqual(self.parser.current_handler, MetaParser.handleTempo)

    def testTempoCall(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("metronome", {})
        self.parser.StartTag("beat-unit", {})
        self.parser.current_handler = MagicMock(name="method")
        self.parser.NewData("quarter")
        self.parser.current_handler.assert_called_once_with(self.parser.tags,self.parser.attribs,self.parser.chars,self.parser.parts,self.parser.data)

    def testTempoBeat(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("metronome", {})
        self.parser.StartTag("beat-unit", {})
        self.parser.NewData("quarter")
        self.assertEqual(self.parser.data, {"tempo":[{"beat":"quarter"}]})

    def testTempoBeatType(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("metronome", {})
        self.parser.StartTag("per-minute", {})
        self.parser.NewData("100")
        self.assertEqual(self.parser.data, {"tempo":[{"minute":100}]})

    def testTempoBeatAndPerMinute(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("metronome", {})
        self.parser.StartTag("beat-unit", {})
        self.parser.NewData("quarter")
        self.parser.EndTag("beat-unit")
        self.parser.StartTag("per-minute",{})
        self.parser.NewData("100")
        self.assertEqual(self.parser.parts, {"tempo":[{"beat":"quarter","minute":100}]})

    def testTempoBeatAndSecondBeat(self):
        self.parser.StartTag("part", {"id":"P1"})
        self.parser.StartTag("metronome", {})
        self.parser.StartTag("beat-unit", {})
        self.parser.NewData("quarter")
        self.parser.EndTag("beat-unit")
        self.parser.StartTag("beat-unit",{})
        self.parser.NewData("half")
        self.assertEqual(self.parser.parts, {"tempo":[{"beat":"quarter","beat_2":"half"}]})

