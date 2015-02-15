from implementation.primaries.Drawing.classes import MxmlParser, Measure, Part, Directions
from implementation.primaries.Drawing.tests.testHandlers import testclass


class testHandleDirections(testclass.TestClass):
    def setUp(self):
        testclass.TestClass.setUp(self)
        self.tags.append("direction")
        self.handler = MxmlParser.HandleDirections
        MxmlParser.part_id = "P1"
        MxmlParser.measure_id = 1
        self.piece.Parts["P1"] = Part.Part()
        self.piece.Parts["P1"].addMeasure(1, Measure.Measure(), 1)
        self.measure = self.piece.Parts["P1"].getMeasure(1, 1)
        self.attrs["measure"] = {"number": "1"}
        self.attrs["part"] = {"id": "P1"}
        MxmlParser.direction = None


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
        
        self.assertEqual("above", MxmlParser.direction.placement)

    def testDirectionTag(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        measure = self.piece.Parts["P1"].getMeasure(1,1)
        
        self.assertIsInstance(MxmlParser.direction, Directions.Direction)
        self.assertEqual("hello, world", MxmlParser.direction.text)

    def testWordsWithFontSizeAttrib(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "size"))
        self.assertEqual("6.5", MxmlParser.direction.size)

    def testWordsWithFontFamAttrib(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "font"))
        self.assertEqual("times", MxmlParser.direction.font)

    def testWordsWithBothAttribs(self):
        self.tags.append("words")
        self.chars["words"] = "hello, world"
        self.attrs["words"] = {"font-family": "times", "font-size": "6.2"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual("times", MxmlParser.direction.font)
        self.assertEqual("6.2", MxmlParser.direction.size)

    def testOctaveShift(self):
        self.tags.append("octave-shift")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertIsInstance(MxmlParser.direction, Directions.OctaveShift)

    def testOctaveShiftType(self):
        self.tags.append("octave-shift")
        self.attrs["octave-shift"] = {"type": "down"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "type"))

    def testOctaveShiftAmount(self):
        self.tags.append("octave-shift")
        self.attrs["octave-shift"] = {"size": "8"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "amount"))
        self.assertEqual(8, MxmlParser.direction.amount)

    def testWavyLine(self):
        self.tags.append("wavy-line")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertIsInstance(MxmlParser.direction, Directions.WavyLine)

    def testWavyLineType(self):
        self.tags.append("wavy-line")
        self.attrs["wavy-line"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual("start", MxmlParser.direction.type)

    def testPedal(self):
        self.tags.append("pedal")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertIsInstance(MxmlParser.direction, Directions.Pedal)

    def testPedalLine(self):
        self.tags.append("pedal")
        self.attrs["pedal"] = {"line": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual(True, MxmlParser.direction.line)

    def testPedalLineType(self):
        self.tags.append("pedal")
        self.attrs["pedal"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual("start", MxmlParser.direction.type)

    def testBracket(self):
        self.tags.append("bracket")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertIsInstance(MxmlParser.direction, Directions.Bracket)

    def testBracketType(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"type": "start"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual("start", MxmlParser.direction.type)

    def testBracketNumber(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"number": "1"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual(1, MxmlParser.direction.number)

    def testBracketLineEnd(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"line-end": "none"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual("none", MxmlParser.direction.lineEnd)

    def testBracketEndLength(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"end-length": "15"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual(15, MxmlParser.direction.endLength)

    def testBracketLineType(self):
        self.tags.append("bracket")
        self.attrs["bracket"] = {"line-type": "solid"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertEqual("solid", MxmlParser.direction.lineType)

class testMetronome(testHandleDirections):
    def setUp(self):
        testHandleDirections.setUp(self)
        self.tags.append("metronome")


    def testMetronomeBeatUnitTag(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "beat"))
        self.assertEqual("quarter", MxmlParser.direction.beat)

    def testBeatUnitWithFontAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "beat"))
        self.assertEqual("quarter", MxmlParser.direction.beat)
        self.assertTrue(hasattr(MxmlParser.direction, "font"))
        self.assertEqual("times", MxmlParser.direction.font)

    def testBeatUnitWithFontSizeAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "beat"))
        self.assertEqual("quarter", MxmlParser.direction.beat)
        self.assertTrue(hasattr(MxmlParser.direction, "size"))
        self.assertEqual("6.5", MxmlParser.direction.size)

    def testBeatUnitWithFontAttrib(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "beat"))
        self.assertEqual("quarter", MxmlParser.direction.beat)
        self.assertTrue(hasattr(MxmlParser.direction, "parentheses"))
        self.assertEqual(True, MxmlParser.direction.parentheses)

    def testBeatUnitAllAttribs(self):
        self.tags.append("beat-unit")
        self.chars["beat-unit"] = "quarter"
        self.attrs["metronome"] = {"font-family": "times", "font-size": "6.5", "parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "beat"))
        self.assertEqual("quarter", MxmlParser.direction.beat)
        self.assertTrue(hasattr(MxmlParser.direction, "font"))
        self.assertEqual("times", MxmlParser.direction.font)
        self.assertTrue(hasattr(MxmlParser.direction, "size"))
        self.assertEqual("6.5", MxmlParser.direction.size)
        self.assertTrue(hasattr(MxmlParser.direction, "parentheses"))
        self.assertEqual(True, MxmlParser.direction.parentheses)

    def testPerMinuteTag(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.direction, Directions.Metronome)
        self.assertTrue(hasattr(MxmlParser.direction, "min"))
        self.assertEqual("85", MxmlParser.direction.min)

    def testPerMinuteFontFamAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "font"))
        self.assertEqual("times", MxmlParser.direction.font)

    def testPerMinuteFontSizeAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"font-size": "6.5"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "size"))
        self.assertEqual(6.5, MxmlParser.direction.size)

    def testPerMinuteParenthesesAttrib(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"parentheses": "yes"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "parentheses"))
        self.assertTrue(MxmlParser.direction.parentheses)

    def testPerMinuteAllAttribs(self):
        self.tags.append("per-minute")
        self.chars["per-minute"] = "85"
        self.attrs["metronome"] = {"parentheses": "yes",
                                   "font-size": "6.5",
                                   "font-family": "times"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.direction, "parentheses"))
        self.assertTrue(MxmlParser.direction.parentheses)
        self.assertTrue(hasattr(MxmlParser.direction, "size"))
        self.assertEqual(6.5, MxmlParser.direction.size)
        self.assertTrue(hasattr(MxmlParser.direction, "font"))
        self.assertEqual("times", MxmlParser.direction.font)

class testDynamicsAndSound(testHandleDirections):
    def testDynamicTag(self):
        self.tags.append("dynamics")
        self.tags.append("p")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        self.assertIsInstance(MxmlParser.expression, Directions.Dynamic)
        self.assertEqual("p", MxmlParser.expression.mark)

    def testSoundTag(self):
        self.tags.append("sound")
        self.assertEqual(1, self.handler(self.tags, self.attrs, self.chars, self.piece))

    def testSoundDynamicAttr(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dynamics": "80"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(self.measure, "volume"))
        self.assertEqual("80", self.measure.volume)

    def testSoundTempoAttr(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"tempo": "80"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(self.measure, "tempo"))
        self.assertEqual("80", self.measure.tempo)

    def testSoundAttrs(self):
        self.tags.append("sound")
        self.attrs["sound"] = {"dynamics": "60", "tempo": "50"}
        self.handler(self.tags,self.attrs,self.chars,self.piece)
        
        self.assertTrue(hasattr(self.measure, "tempo"))
        self.assertEqual("50", self.measure.tempo)
        self.assertTrue(hasattr(self.measure, "volume"))
        self.assertEqual("60", self.measure.volume)

    def testWedgeTag(self):
        self.tags.append("wedge")
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertIsInstance(MxmlParser.expression, Directions.Wedge)

    def testWedgeVal(self):
        self.tags.append("wedge")
        self.attrs["wedge"] = {"type": "crescendo"}
        self.handler(self.tags, self.attrs, self.chars, self.piece)
        
        self.assertTrue(hasattr(MxmlParser.expression, "type"))
        self.assertEqual("crescendo", MxmlParser.expression.type)