from implementation.primaries.Drawing.tests.testUsingXML.setup import xmlSet, parsePiece
import os

partname = "accidentals.xml"
folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases"
piece = parsePiece(os.path.join(folder, partname))

class testAccidentals(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.fname = "accidentals.xml"
        self.m_num = 32
        self.p_id = "P1"
        self.p_name = "Flute"
        self.note_num = {1: 4,2: 4,3: 4,4: 4,5: 4,6: 4,7: 4,8: 1,9: 1,10: 1,
                         11: 1,12: 1,13: 1,14: 1,15: 1,16: 1,17: 1,18: 1,19: 1,
                         20: 1,21: 1,22: 1,23: 1,24: 1,25: 1,26: 1,27: 1,28: 1,
                         29: 1,30: 1,31: 1,32: 1}

    def testParts(self):
        global piece
        self.assertTrue(self.p_id in piece.Parts)
        self.assertEqual(self.p_name, piece.Parts[self.p_id].name)

    def testMeasures(self):
        self.assertTrue(self.m_num in piece.Parts[self.p_id].measures)

    def testNotes(self):

        for measure in piece.Parts[self.p_id].measures.keys():
            if measure in self.note_num:
                self.assertEqual(self.note_num[measure], len(piece.Parts[self.p_id].measures[measure].items[1]))

class NoteTests(xmlSet):
    def setUp(self):
        xmlSet.setUp(self)
        self.p_id = "P1"
        self.measure_id = None
        self.step = ""
        self.alter = None
        self.octave = None
        self.accidental = None
        self.note = None

    def testNoteStep(self):
        note_obj = None
        if piece is not None and self.measure_id is not None and self.note is not None:
            note_obj = piece.Parts[self.p_id].measures[self.measure_id].items[1][self.note]
        if note_obj is not None and self.step is not None:
            self.assertEqual(self.step, note_obj.pitch.step)

    def testNoteAlter(self):
        note_obj = None
        if piece is not None and self.measure_id is not None and self.note is not None:
            note_obj = piece.Parts[self.p_id].measures[self.measure_id].items[1][self.note]
        if note_obj is not None and self.alter is not None:
            self.assertEqual(self.alter, int(note_obj.pitch.alter))

    def testNoteOctave(self):
        note_obj = None
        if piece is not None and self.measure_id is not None and self.note is not None:
            note_obj = piece.Parts[self.p_id].measures[self.measure_id].items[1][self.note]
        if note_obj is not None and self.octave is not None:
            self.assertEqual(self.octave, int(note_obj.pitch.octave))

    def testNoteAccidental(self):
        note_obj = None
        if piece is not None and self.measure_id is not None and self.note is not None:
            note_obj = piece.Parts[self.p_id].measures[self.measure_id].items[1][self.note]
        if note_obj is not None and self.accidental is not None:
            self.assertEqual(self.accidental, note_obj.pitch.accidental)


class testNote1M1(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.step = "E"
        self.alter = 1
        self.octave = 4
        self.accidental = "sharp"
        self.measure_id = 1
        self.note = 0
class testNote2M1(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 1
        self.step = "F"
        self.alter = -1
        self.octave = 4
        self.accidental = "flat"
        self.note = 1
class testNote3M1(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 1
        self.step = "A"
        self.alter = 2
        self.octave = 4
        self.accidental = "double-sharp"
        self.note = 2
class testNote4M1(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 1
        self.step = "C"
        self.alter = -2
        self.octave = 5
        self.accidental = "flat-flat"
        self.note = 3
class testNote1M2(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 2
        self.step = "C"
        self.alter = None
        self.octave = 5
        self.accidental = "natural"
        self.note = 0
class testNote2M2(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 2
        self.step = "A"
        self.alter = None
        self.octave = 4
        self.accidental = "quarter-flat"
        self.note = 1
class testNote3M2(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.step = "F"
        self.alter = None
        self.octave = 4
        self.accidental = None
        self.measure_id = 2
        self.note = 2
class testNote4M2(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 2
        self.step = "C"
        self.alter = None
        self.octave = 5
        self.accidental = "three-quarters-flat"
        self.note = 3
class testNote1M3(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 3
        self.step = "G"
        self.alter = None
        self.octave = 4
        self.accidental = "quarter-flat"
        self.note = 0
class testNote2M3(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 3
        self.step = "B"
        self.alter = None
        self.octave = 4
        self.accidental = None
        self.note = 1
class testNote3M3(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 3
        self.step = "B"
        self.alter = None
        self.octave = 4
        self.accidental = "three-quarters-flat"
        self.note = 2
class testNote4M3(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 3
        self.step = "G"
        self.alter = None
        self.octave = 4
        self.accidental = "quarter-sharp"
        self.note = 3
class testNote1M4(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.step = "F"
        self.alter = None
        self.octave = 4
        self.accidental = None
        self.measure_id = 4
        self.note = 0
class testNote2M4(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 4
        self.step = "B"
        self.alter = None
        self.octave = 4
        self.accidental = None
        self.note = 1
class testNote3M4(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 4
        self.step = "A"
        self.alter = None
        self.octave = 4
        self.accidental = "three-quarters-sharp"
        self.note = 2

class testNote4M4(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 4
        self.step = "G"
        self.alter = None
        self.octave = 4
        self.accidental = "three-quarters-sharp"
        self.note = 3
class testNote1M5(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 5
        self.step = "F"
        self.alter = None
        self.octave = 4
        self.accidental = "quarter-sharp"
        self.note = 0
class testNote2M5(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 5
        self.step = "G"
        self.alter = None
        self.octave = 4
        self.accidental = None
        self.note = 1
class testNote3M5(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.step = "F"
        self.alter = None
        self.octave = 4
        self.accidental = "quarter-flat"
        self.measure_id = 5
        self.note = 2
class testNote4M5(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 5
        self.step = "B"
        self.alter = None
        self.octave = 4
        self.accidental = "three-quarters-flat"
        self.note = 3
class testNote1M6(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 6
        self.step = "G"
        self.alter = None
        self.octave = 4
        self.accidental = None
        self.note = 0
class testNote2M6(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 6
        self.step = "D"
        self.alter = None
        self.octave = 5
        self.accidental = "quarter-sharp"
        self.note = 1
class testNote3M6(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 6
        self.step = "A"
        self.alter = None
        self.octave = 4
        self.accidental = "quarter-flat"
        self.note = 2
class testNote4M6(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 6
        self.step = "G"
        self.alter = None
        self.octave = 4
        self.accidental = None
        self.note = 3
class testNote1M7(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 7
        self.step = "G"
        self.alter = None
        self.octave = 4
        self.accidental = "sori"
        self.note = 0
class testNote2M7(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 7
        self.step = "G"
        self.alter = None
        self.octave = 4
        self.accidental = "koron"
        self.note = 1
class testNote3M7(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 7
        self.step = "C"
        self.alter = -1
        self.octave = 5
        self.accidental = "flat"
        self.note = 2
class testNote4M7(NoteTests):
    def setUp(self):
        NoteTests.setUp(self)
        self.measure_id = 7
        self.step = "A"
        self.alter = None
        self.octave = 4
        self.accidental = None
        self.note = 3

