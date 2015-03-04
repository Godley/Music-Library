from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.tests.testLilyMethods.testMeasure import MeasureTests
from implementation.primaries.Drawing.classes import Measure, Note
from implementation.primaries.Drawing.classes.tree_cls.PieceTree import MeasureNode, StaffNode

class testNormalBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="normal")
        self.lilystring = " \\bar \"|\""

class testDottedBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="dotted")
        self.lilystring = " \\bar \";\""

class testDashedBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="dashed")
        self.lilystring = " \\bar \"!\""

class testHeavyLightBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-light")
        self.lilystring = " \\bar \".|\""

class testLightHeavyBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-heavy")
        self.lilystring = " \\bar \"|.\""

class testLightLightBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-light")
        self.lilystring = " \\bar \"||\""

class testHeavyHeavyBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-heavy")
        self.lilystring = " \\bar \"..\""

class testForwardRepeat(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-light", repeat="forward")
        self.lilystring = " \\repeat volta 2 {"

class testBackwardRepeat(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="light-heavy", repeat="backward")
        self.lilystring = "}"

class testEndingMark(Lily):
    def setUp(self):
        self.item = Measure.EndingMark()
        self.lilystring = "}\n\\alternative {\n{"

class testEndingMark2(Lily):
    def setUp(self):
        self.item = Measure.EndingMark(number=2)
        self.lilystring = "{"

class testEndingMarkEnd(Lily):
    def setUp(self):
        self.item = Measure.EndingMark(type="stop")
        self.lilystring = "}\n"

class testBarlineWithEndingStart(Lily):
    def setUp(self):
        self.item = Measure.Barline(style="heavy-light",ending=Measure.EndingMark())
        self.lilystring = "}\n\\alternative {\n{"

class testMeasureLeftBarline(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.item.GetItem().AddBarline(Measure.Barline(repeat="forward"),location="left")
        self.lilystring = " \\repeat volta 2 {c'  | "

class testMeasureRightBarline(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.item.GetItem().AddBarline(Measure.Barline(repeat="forward"), location="left")
        self.item.GetItem().AddBarline(Measure.Barline(repeat="backward"), location="right")
        self.lilystring = " \\repeat volta 2 {c' }"


class testMeasureRightRepeatBarlineNoLeft(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.item.GetItem().AddBarline(Measure.Barline(repeat="backward-barline"), location="right")
        self.lilystring = "c'  \\bar \":|.\""


class testMeasureRightRepeatBarlineNoLeftWithAlternatives(MeasureTests):
    def setUp(self):
        self.item = StaffNode()
        m2 = MeasureNode()
        note2 = Note.Note()
        note2.pitch = Note.Pitch()
        m2.addNote(note2)
        self.item.AddChild(m2, index=1)
        m = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        m.addNote(note)
        m.GetItem().AddBarline(Measure.Barline(repeat="backward", ending=Measure.EndingMark(number=1)), location="right")
        self.item.AddChild(m, index=2)
        self.lilystring = "\\autoBeamOff % measure 1\n\\repeat volta 2{c'}\n\\alternative{{c' \\bar \":|.\" }} "
