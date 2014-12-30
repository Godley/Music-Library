from implementation.primaries.Loading.classes import MxmlParser, Measure, Part, Directions
from implementation.primaries.Loading.tests.testHandlers import testclass


class testHandleDirections(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
        self.tags.append("direction")
        self.handler = MxmlParser.HandleDirections
        MxmlParser.part_id = "P1"
        MxmlParser.measure_id = 1
        self.piece.Parts["P1"] = Part.Part()
        self.piece.Parts["P1"].measures[1] = Measure.Measure()
        self.measure = self.piece.Parts["P1"].measures[1]
        self.measure.items[1] = []
        self.attrs["measure"] = {"number": "1"}
        self.attrs["part"] = {"id": "P1"}

    def copy(self):
        for item in MxmlParser.item_list:
            self.measure.items[1].append(item)
            MxmlParser.item_list.pop()

    def testNoTags(self):
        self.tags.remove("direction")
        self.assertEqual(None, self.handler(self.tags, self.attrs, self.chars, self.piece))

    def testIrrelevantTags(self):
        self.tags.remove("direction")
        self.tags.append("hello")
        self.assertEqual(None, self.handler(self.tags, self.attrs, self.chars, self.piece))


    def testDirectionAttribTag(self):
        self.tags.append("words")
        self.attrs["direction"] = {"placement": "above"}
        self.chars["words"] = "sup"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("above", self.measure.items[1][0].placement)

    def testDirectionTag(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        measure = self.piece.Parts["P1"].measures[1]
        self.copy()
        self.assertEqual(1, len(measure.items[1]))
        self.assertEqual("hello, world", measure.items[1][0].text)

    def testWordsWithFontSizeAttrib(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "size"))
        self.assertEqual("6.5", self.measure.items[1][0].size)

    def testWordsWithFontFamAttrib(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "font"))
        self.assertEqual("times", self.measure.items[1][0].font)

    def testWordsWithBothAttribs(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-family": "times", "font-size": "6.2"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("times", self.measure.items[1][0].font)
        self.assertEqual("6.2", self.measure.items[1][0].size)

    def testOctaveShift(self):
        self.tags.append("octave-shift")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertIsInstance(self.measure.items[1][0], Directions.OctaveShift)

    def testOctaveShiftType(self):
        self.tags.append("octave-shift")
        self.attrs["octave-shift"] = {"type": "down"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "type"))

    def testOctaveShiftAmount(self):
        self.tags.append("octave-shift")
        self.attrs["octave-shift"] = {"size": "8"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "amount"))
        self.assertEqual(8, self.measure.items[1][0].amount)

    def testWavyLine(self):
        self.tags.append("wavy-line")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertIsInstance(self.measure.items[1][0], Directions.WavyLine)

    def testWavyLineType(self):
        self.tags.append("wavy-line")
        self.attrs["wavy-line"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("start", self.measure.items[1][0].type)

    def testPedal(self):
        self.tags.append("pedal")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertIsInstance(self.measure.items[1][0], Directions.Pedal)

    def testPedalLine(self):
        self.tags.append("pedal")
        self.attrs["pedal"] = {"line": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual(True, self.measure.items[1][0].line)

    def testPedalLineType(self):
        self.tags.append("pedal")
        self.attrs["pedal"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("start", self.measure.items[1][0].type)

    def testBracket(self):
        self.tags.append("bracket")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertIsInstance(self.measure.items[1][0], Directions.Bracket)

    def testBracketType(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("start", self.measure.items[1][0].type)

    def testBracketNumber(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual(1, self.measure.items[1][0].number)

    def testBracketLineEnd(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"line-end": "none"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("none", self.measure.items[1][0].lineEnd)

    def testBracketEndLength(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"end-length": "15"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual(15, self.measure.items[1][0].endLength)

    def testBracketLineType(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"line-type": "solid"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("solid", self.measure.items[1][0].lineType)

class testMetronome(testHandleDirections):
    def setUp(self):
        testHandleDirections.setUp(self)
        self.tags.append("metronome")

    def testMetronomeBeatUnitTag(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "beat"))
        self.assertEqual("quarter", self.measure.items[1][0].beat)

    def testBeatUnitWithFontAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "beat"))
        self.assertEqual("quarter", self.measure.items[1][0].beat)
        self.assertTrue(hasattr(self.measure.items[1][0], "font"))
        self.assertEqual("times", self.measure.items[1][0].font)

    def testBeatUnitWithFontSizeAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "beat"))
        self.assertEqual("quarter", self.measure.items[1][0].beat)
        self.assertTrue(hasattr(self.measure.items[1][0], "size"))
        self.assertEqual("6.5", self.measure.items[1][0].size)

    def testBeatUnitWithFontAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "beat"))
        self.assertEqual("quarter", self.measure.items[1][0].beat)
        self.assertTrue(hasattr(self.measure.items[1][0], "parentheses"))
        self.assertEqual(True, self.measure.items[1][0].parentheses)

    def testBeatUnitAllAttribs(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"font-family": "times", "font-size": "6.5", "parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        print(self.measure.items[1][0])
        self.assertTrue(hasattr(self.measure.items[1][0], "beat"))
        self.assertEqual("quarter", self.measure.items[1][0].beat)
        self.assertTrue(hasattr(self.measure.items[1][0], "font"))
        self.assertEqual("times", self.measure.items[1][0].font)
        self.assertTrue(hasattr(self.measure.items[1][0], "size"))
        self.assertEqual("6.5", self.measure.items[1][0].size)
        self.assertTrue(hasattr(self.measure.items[1][0], "parentheses"))
        self.assertEqual(True, self.measure.items[1][0].parentheses)

    def testPerMinuteTag(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual(1, len(self.measure.items[1]))
        self.assertTrue(hasattr(self.measure.items[1][0], "min"))
        self.assertEqual("85", self.measure.items[1][0].min)

    def testPerMinuteFontFamAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "font"))
        self.assertEqual("times", self.measure.items[1][0].font)

    def testPerMinuteFontSizeAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "size"))
        self.assertEqual(6.5, self.measure.items[1][0].size)

    def testPerMinuteParenthesesAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "parentheses"))
        self.assertTrue(self.measure.items[1][0].parentheses)

    def testPerMinuteAllAttribs(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"parentheses": "yes",
                                   "font-size": "6.5",
                                   "font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][0], "parentheses"))
        self.assertTrue(self.measure.items[1][0].parentheses)
        self.assertTrue(hasattr(self.measure.items[1][0], "size"))
        self.assertEqual(6.5, self.measure.items[1][0].size)
        self.assertTrue(hasattr(self.measure.items[1][0], "font"))
        self.assertEqual("times", self.measure.items[1][0].font)

class testDynamicsAndSound(testHandleDirections):
    def testDynamicTag(self):
        self.tags.append("dynamics")
        self.tags.append("p")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(len(self.measure.items[1]) > 0)
        self.assertEqual(Directions.Dynamic, type(self.measure.items[1][-1]))
        self.assertEqual("p", self.measure.items[1][-1].mark)

    def testSoundTag(self):
        self.tags.append("sound")
        self.assertEqual(1, self.handler(self.tags, self.attrs, self.chars, self.piece))

    def testSoundDynamicAttr(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dynamics": "80"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure, "volume"))
        self.assertEqual("80", self.measure.volume)

    def testSoundTempoAttr(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"tempo": "80"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure, "tempo"))
        self.assertEqual("80", self.measure.tempo)

    def testSoundAttrs(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dynamics": "60", "tempo": "50"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure, "tempo"))
        self.assertEqual("50", self.measure.tempo)
        self.assertTrue(hasattr(self.measure, "volume"))
        self.assertEqual("60", self.measure.volume)

    def testWedgeTag(self):
        self.tags.append("wedge")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertIsInstance(self.measure.items[1][-1], Directions.Wedge)

    def testWedgeVal(self):
        self.tags.append("wedge")
        self.attrs["wedge"] = {"type": "crescendo"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertTrue(hasattr(self.measure.items[1][-1], "type"))
        self.assertEqual("crescendo", self.measure.items[1][-1].type)

    def testOffset(self):
        self.tags.append("wedge")
        self.attrs["wedge"] = {"type": "crescendo"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.tags.append("offset")
        self.chars["offset"] = "2"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.copy()
        self.assertEqual("2", self.measure.items[1][-1].offset)