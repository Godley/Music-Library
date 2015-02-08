from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
import os

partname = "duration_and_stem_direction.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testFile(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

class testNoteDurations(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testMeasure1Note1(self):
        measure = piece.Parts["P1"].measures[1]
        self.assertEqual(1, len(measure.items))

    def testMeasure1Note1Duration(self):
        item = piece.Parts["P1"].measures[1].notes[0]
        self.assertEqual(64, item.duration)

    def testMeasure2Notes(self):
        measure = piece.Parts["P1"].measures[2]
        self.assertEqual(3, len(measure.notes))

    def testMeasure2Note1(self):
        item = piece.Parts["P1"].measures[2].notes[0]
        self.assertEqual(32, item.duration)

    def testMeasure2Note2(self):
        item = piece.Parts["P1"].measures[2].notes[1]
        self.assertEqual(16, item.duration)

    def testMeasure2Note3(self):
        item = piece.Parts["P1"].measures[2].notes[2]
        self.assertEqual(16, item.duration)

    def testMeasure3Notes(self):
        measure = piece.Parts["P1"].measures[3]
        self.assertEqual(7, len(measure.notes))

    def testMeasure3Note1(self):
        item = piece.Parts["P1"].measures[3].notes[0]
        self.assertEqual(8, item.duration)

    def testMeasure3Note2(self):
        item = piece.Parts["P1"].measures[3].notes[1]
        self.assertEqual(4, item.duration)

    def testMeasure3Note3(self):
        item = piece.Parts["P1"].measures[3].notes[2]
        self.assertEqual(2, item.duration)

    def testMeasure3Note4(self):
        item = piece.Parts["P1"].measures[3].notes[3]
        self.assertEqual(1, item.duration)

    def testMeasure3Note5(self):
        item = piece.Parts["P1"].measures[3].notes[4]
        self.assertEqual(1, item.duration)

    def testMeasure3Note6(self):
        item = piece.Parts["P1"].measures[3].notes[5]
        self.assertEqual(16, item.duration)

    def testMeasure3Note7(self):
        item = piece.Parts["P1"].measures[3].notes[6]
        self.assertEqual(32, item.duration)

class testStems(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"

    def testMeasure1(self):
        note = piece.Parts[self.p_id].measures[1].notes[0]
        self.assertFalse(hasattr(note, "stem"))

    def testMeasure2Note1(self):
        note = piece.Parts[self.p_id].measures[2].notes[0]
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure2Note1Direction(self):
        note = piece.Parts[self.p_id].measures[2].notes[0]
        self.assertEqual("up", note.stem.type)

    def testMeasure2Note2(self):
        note = piece.Parts[self.p_id].measures[2].notes[1]
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure2Note2Direction(self):
        note = piece.Parts[self.p_id].measures[2].notes[1]
        self.assertEqual("up", note.stem.type)

    def testMeasure2Note3(self):
        note = piece.Parts[self.p_id].measures[2].notes[2]
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure2Note3Direction(self):
        note = piece.Parts[self.p_id].measures[2].notes[2]
        self.assertEqual("up", note.stem.type)

    def testMeasure3Note1(self):
        note = piece.Parts[self.p_id].measures[3].notes[0]
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure3Note1Direction(self):
        note = piece.Parts[self.p_id].measures[3].notes[0]
        self.assertEqual("down", note.stem.type)

    def testMeasure3Note2(self):
        note = piece.Parts[self.p_id].measures[3].notes[1]
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure3Note2Direction(self):
        note = piece.Parts[self.p_id].measures[3].notes[1]
        self.assertEqual("down", note.stem.type)

    def testMeasure3Note3(self):
        note = piece.Parts[self.p_id].measures[3].notes[2]
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure3Note3Direction(self):
        note = piece.Parts[self.p_id].measures[3].notes[2]
        self.assertEqual("down", note.stem.type)

    def testMeasure3Note4(self):
        note = piece.Parts[self.p_id].measures[3].notes[3]
        self.assertTrue(hasattr(note, "stem"))

    def testMeasure3Note4Direction(self):
        note = piece.Parts[self.p_id].measures[3].notes[3]
        self.assertEqual("down", note.stem.type)
