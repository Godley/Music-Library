from implementation.primaries.Drawing.classes.tree_cls.BaseTree import IndexedNode
from implementation.primaries.Drawing.classes.tree_cls import MeasureNode
from implementation.primaries.Drawing.classes import Measure

class StaffNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[MeasureNode.MeasureNode])
        self.autoBeam = True

    def NewBeam(self, type):
        if type == "end":
            self.autoBeam = False

    def CheckTotals(self):
        measures = self.GetChildrenIndexes()
        total = "1"
        for m_id in measures:
            mNode = self.GetChild(m_id)
            mItemTotal = mNode.GetTotalValue()
            if mItemTotal == "":
                mNode.value = total
            else:
                total = mItemTotal
                mNode.value = mItemTotal

    def toLily(self):
        lilystring = ""

        if not self.autoBeam:
            lilystring += "\\autoBeamOff"
        children = self.GetChildrenIndexes()
        if not hasattr(self, "transpose"):
            self.transpose = None
        for child in range(len(children)):
            measureNode = self.GetChild(children[child])
            measureNode.autoBeam = self.autoBeam
            lilystring += " % measure "+str(children[child])+"\n"
            lilystring += measureNode.toLily()+"\n\n"
        return lilystring

    def CheckDivisions(self):
        children = self.GetChildrenIndexes()
        divisions = 1
        for child in children:
            measure = self.GetChild(child)
            if hasattr(measure, "divisions"):
                divisions = measure.divisions
            else:
                measure.divisions = divisions
            measure.CheckDivisions()

    def DoBarlineChecks(self):
        measure_indexes = self.GetChildrenIndexes()
        if hasattr(self, "backward_repeats"):
            if len(self.backward_repeats) > 0:
                measure = self.GetChild(measure_indexes[0])
                for repeat in self.backward_repeats:
                    measure.AddBarline(Measure.Barline(repeat="forward", repeatNum=repeat), location="left-1")
        if hasattr(self, "forward_repeats"):
            if len(self.forward_repeats) > 0:
                measure = self.GetChild(measure_indexes[-1])
                for repeat in self.forward_repeats:
                    measure.AddBarline(Measure.Barline(repeat="backward", repeatNum=repeat), location="right-1")

    def AddBarline(self, item=None, measure_id=1, location="left"):
        measure = self.GetChild(measure_id)
        if measure is None:
            self.AddChild(MeasureNode.MeasureNode(), measure_id)
            measure = self.GetChild(measure_id)
        if hasattr(item, "repeat"):
            num = item.repeatNum
            if item.repeat == "forward":
                if not hasattr(self, "forward_repeats"):
                    self.forward_repeats = []
                self.forward_repeats.append(num)
            if item.repeat == "backward":
                num = item.repeatNum
                if not hasattr(self, "backward_repeat"):
                    self.backward_repeats = []
                self.backward_repeats.append(num)
                if hasattr(self, "forward_repeats") and (len(self.forward_repeats) == len(self.backward_repeats) and len(self.forward_repeats) > 0):
                    self.forward_repeats.pop()
                    self.backward_repeats.pop()
        measure.AddBarline(item, location=location)