from implementation.primaries.Drawing.tests.testLilyMethods.setup import Lily
from implementation.primaries.Drawing.tests.testLilyMethods.testMeasure import MeasureTests
from implementation.primaries.Drawing.classes import Measure, Note
from implementation.primaries.Drawing.classes.tree_cls.Testclasses import MeasureNode, NoteNode

class testNormalBarline(Lily):
    def setUp(self):
        self.item = Measure.Barline()
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
        self.lilystring = " \\repeat volta 2 { % voice 1\n{ c' } | "

class testMeasureRightBarline(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.item.GetItem().AddBarline(Measure.Barline(repeat="forward"), location="left")
        self.item.GetItem().AddBarline(Measure.Barline(repeat="backward"), location="right")
        self.lilystring = " \\repeat volta 2 { % voice 1\n{ c' }} | "


class testMeasureRightRepeatBarlineNoLeft(MeasureTests):
    def setUp(self):
        self.item = MeasureNode()
        note = Note.Note()
        note.pitch = Note.Pitch()
        self.item.addNote(note)
        self.item.GetItem().AddBarline(Measure.Barline(repeat="backward-barline"), location="right")
        self.lilystring = " % voice 1\n{ c' } \\bar \":|.\" | "

#TODO: look at why this is commented out
# class testPartWithRepeatsAndMultipleAlternativeEndings(MeasureTests):
#     def setUp(self):
#         self.item = Part.Part()
#         self.item.addEmptyMeasure(1,1)
#         measure1 = self.item.getMeasure(1,1)
#         measure1.AddBarline("left", Measure.Barline(repeat="forward"))
#         self.item.addEmptyMeasure(2,1)
#         measure2 = self.item.getMeasure(2,1)
#         measure2.AddBarline("left", Measure.Barline(ending=Measure.EndingMark(number=1,type="start")))
#         measure2.AddBarline("right", Measure.Barline(repeat="backward", ending=Measure.EndingMark(number=1,type="stop")))
#         self.item.addEmptyMeasure(3,1)
#         measure3 = self.item.getMeasure(3,1)
#         measure3.AddBarline("left", Measure.Barline(ending=Measure.EndingMark(number=2,type="start")))
#         measure3.AddBarline("right", Measure.Barline(ending=Measure.EndingMark(number=2,type="stop")))
#         self.item.addEmptyMeasure(4,1)
#         measure4 = self.item.getMeasure(4,1)
#         measure4.AddBarline("left", Measure.Barline(ending=Measure.EndingMark(number=3,type="start")))
#         measure4.AddBarline("right", Measure.Barline(ending=Measure.EndingMark(number=3,type="stop")))
#         self.lilystring = "\\new Staff {\\autoBeamOff  \\repeat volta 3 { r}\n\\alternative {\n{ r}\n{ r}\n{ r}\n}}"