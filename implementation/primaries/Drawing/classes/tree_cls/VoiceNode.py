from implementation.primaries.Drawing.classes.tree_cls.BaseTree import IndexedNode, Node
from implementation.primaries.Drawing.classes.tree_cls import NoteNode
from implementation.primaries.Drawing.classes.Note import Arpeggiate, NonArpeggiate, GraceNote, Tuplet


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
                        result = item.Search(Tuplet)
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
                            res = item.Search(Tuplet)

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