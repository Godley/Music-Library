try:
    from implementation.primaries.Drawing.classes.tree_cls.BaseTree import Tree, Node, IndexedNode, Search, BackwardSearch, FindByIndex, FindPosition, toLily
    from implementation.primaries.Drawing.classes.tree_cls import MeasureNode, NoteNode
    from implementation.primaries.Drawing.classes import Measure, Note, Part, Piece, Directions
    from implementation.primaries.Drawing.classes.Directions import OctaveShift
    from implementation.primaries.Drawing.classes.Note import GraceNote, Arpeggiate, NonArpeggiate
except:
    from classes.tree_cls.BaseTree import Tree, Node, IndexedNode, Search, BackwardSearch, FindByIndex, FindPosition, toLily
    from classes import Measure, Note, Part, Piece, Directions
    from classes.Directions import OctaveShift
    from classes.Note import GraceNote, Arpeggiate, NonArpeggiate

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
            mItem = mNode.GetItem()
            mItemTotal = mItem.GetTotalValue()
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
            item = measure.GetItem()
            if hasattr(item, "divisions"):
                divisions = item.divisions
            else:
                item.divisions = divisions
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


class VoiceNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NoteNode.NoteNode, NoteNode.Placeholder])

    def GetNoteTotal(self):
        """gets the total duration of all notes in the current voice"""
        children = self.GetChildrenIndexes()
        int_total = 0
        for child_id in children:
            child = self.GetChild(child_id)
            if hasattr(child, "duration"):
                int_total += child.duration
        return int_total
    
    def RunNoteChecks(self):
        children = self.GetChildrenIndexes()
        previous = None
        for child in range(len(children)):
            note = self.GetChild(children[child])
            item = note.GetItem()
            if item is not None and type(note) == NoteNode.NoteNode:
                # look for arpeggiates or non-arpeggiates, and update the note's childnodes
                # used where a note is part of a chord (usually the case in arpeggiates)
                arpeg = item.Search(Arpeggiate)
                narpeg = item.Search(NonArpeggiate)
                if arpeg is not None or narpeg is not None:
                    note.UpdateArpeggiates()
                
                # now look for gracenotes    
                result = item.Search(GraceNote)
                if result is not None and previous is None:
                    # if this is the first note in the bar, it must be the first gracenote
                    result.first = True
                    
                if len(children) == child+1:
                    # if we're at the last note...
                    if result is not None:
                        # same check as arpeggiates - handles the case where notes are part of a chord
                        note.CheckForGraceNotes()

                    # look for timemods
                    if hasattr(item, "timeMod"):
                        result = item.Search(Note.Tuplet)
                        if result is None:
                            item.close_timemod = True
                        if previous is not None:
                            if hasattr(previous.GetItem(), "timeMod"):
                                item.timeMod.first = False
                            else:
                                item.timeMod.first = True
                        else:
                            item.timeMod.first = True
                    else:
                        item.close_timemod = False
                else:
                    # otherwise check the next item for gracenotes and time mods
                    next = self.GetChild(children[child+1])
                    next_item = next.GetItem()
                    if next_item is not None and type(next) is NoteNode.NoteNode:
                        result = item.Search(GraceNote)
                        next_result = next_item.Search(GraceNote)
                        if result is not None:
                            if next_result is None:
                                note.CheckForGraceNotes()
                            else:
                                result.last = False
                                next_result.first = False
                        if hasattr(item, "timeMod"):
                            res = item.Search(Note.Tuplet)

                            if not hasattr(next_item, "timeMod") and res is None:
                                item.close_timemod = True
                            else:
                                item.close_timemod = False
                            
                            # not sure if checking next and previous is necessary?
                            if previous is not None and type(previous) is NoteNode.NoteNode:
                                if hasattr(previous.GetItem(), "timeMod"):
                                    item.timeMod.first = False
                                else:
                                    item.timeMod.first = True
                            else:
                                item.timeMod.first = True
            previous = note

    def toLily(self):
        lilystring = ""
        children = self.GetChildrenIndexes()
        total= self.GetNoteTotal()
        counter = 0
        for child in range(len(children)):
            note = self.GetChild(children[child])
            item = note.GetItem()
            if item is not None:
                item.autoBeam = self.autoBeam
            if hasattr(note, "duration"):
                counter += note.duration
            if counter > total/2:
                if hasattr(self, "mid_barline"):
                    lilystring += self.mid_barline.toLily()
                    self.__delattr__("mid_barline")
            if hasattr(self, "rest") and hasattr(self, "total"):
                lilystring += "R"+self.total
            else:
                lilystring += note.toLily() + " "
        return lilystring