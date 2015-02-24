from implementation.primaries.Drawing.classes.tree_cls.BaseTree import Tree, Node, IndexedNode, Search, FindByIndex, FindPosition, toLily
from implementation.primaries.Drawing.classes import Measure, Note, Part, Piece
class PieceTree(Tree):
    def __init__(self):
        Tree.__init__(self)
        self.root = IndexedNode(rules=[PartNode])
        self.item = Piece.Piece()

    def SetValue(self, item):
        self.root.SetItem(item)

    def addPart(self, item, index=-1):
        node = PartNode()
        node.SetItem(item)
        self.AddNode(node, index=index)

    def getPart(self, key):
        return self.FindNodeByIndex(key)

    def GetItem(self):
        return self.item

    def SetItem(self, i):
        self.item = i

    def toLily(self):
        lilystring = "\\version \"2.18.2\" \n"
        children = self.root.GetChildrenIndexes()
        partstrings = []
        for child in children:
            part = self.getPart(child)
            partstring = part.toLily()
            lilystring += partstring[0]
            partstrings.append(partstring[1])
        lilystring += self.item.toLily()
        lilystring += "<<"
        lilystring += "".join([partstring for partstring in partstrings])
        lilystring += ">>"
        return lilystring


class PartNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[StaffNode])
        if self.item is None:
            self.item = Part.Part()

    def CheckDivisions(self):
        staves = self.GetChildrenIndexes()
        divisions = 1
        for staff in staves:
            child = self.getStaff(staff)
            measures = child.GetChildrenIndexes()
            for m_id in measures:
                measure = child.GetChild(m_id)
                item = measure.GetItem()
                if hasattr(item, "divisions"):
                    divisions = item.divisions
                else:
                    item.divisions = divisions
                voices = measure.GetChildrenIndexes()
                for voice in voices:
                    v = measure.GetChild(voice)
                    notes = v.GetChildrenIndexes()
                    for note in notes:
                        noteNode = v.GetChild(note)
                        note_item = noteNode.GetItem()
                        if not hasattr(note_item, "divisions"):
                            note_item.divisions = item.divisions

    def getMeasure(self, measure=1, staff=1):
        staff_obj = self.GetChild(staff)
        measure_obj = None
        if staff_obj is not None:
            measure_obj = FindByIndex(staff_obj, measure)
        return measure_obj

    def getStaff(self, key):
        return self.GetChild(key)

    def addMeasure(self, item, measure=1, staff=1):
        if self.getStaff(staff) is None:
            self.AddChild(StaffNode(), staff)
        staff_obj = self.getStaff(staff)
        measure_obj = MeasureNode()
        measure_obj.SetItem(item)
        staff_obj.AddChild(measure_obj, measure)

    def addEmptyMeasure(self, measure=1, staff=1):
        measure_obj = Measure.Measure()
        self.addMeasure(measure_obj, measure=measure, staff=staff)

    def toLily(self):
        self.CheckDivisions()
        staves = self.GetChildrenIndexes()
        name = ""
        if hasattr(self.item, "name"):
            name = self.item.name
        if hasattr(self.item, "shortname") and self.item.shortname is not None and (not hasattr(self.item, "name") or len(self.item.name) > 10):
            name = self.item.shortname
        variables = [name.lower() + "S" + Part.NumbersToWords(s) for s in staves]
        first_part = ""
        for staff, variable in zip(staves, variables):
            staffstring = variable + " = \\new Staff"
            if len(staves) == 1:
                if name != "":
                    staffstring += " \with {\n"
                    staffstring += "instrumentName = #\""+ name +" \"\n"
                    staffstring += " }"
            staffstring += "{"+self.GetChild(staff).toLily() + " }\n\n"
            first_part += staffstring

        second_part = ""
        if len(variables) > 1:
            second_part += "\\new StaffGroup "
            if name != "":
                second_part += "\with {\n"
                second_part += "instrumentName = #\""+ name +" \"\n"
                second_part += " }"
            second_part += "<<"
        second_part += "\n".join(["\\"+var for var in variables])
        if len(variables) > 1:
            second_part += ">>"
        return [first_part, second_part]


class StaffNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[MeasureNode])

    def toLily(self):
        lilystring = "\\autoBeamOff"
        children = self.GetChildrenIndexes()
        for child in children:
            lilystring += " % measure "+str(child)+"\n"
            lilystring += self.GetChild(child).toLily()+"\n\n"
        return lilystring

class MeasureNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[VoiceNode])
        self.index = 0
        if self.item is None:
            self.item = Measure.Measure()

    def Forward(self, duration=0):
        for voice in self.GetChildrenIndexes():
            voice_obj = self.getVoice(voice)
            if voice_obj.GetChild(self.index) is None:
                voice_obj.AddChild(NoteNode(duration=duration))
        self.index += 1

    def Backup(self, duration=0):
        total = 0
        children = self.GetChildrenIndexes()
        notes = 0
        for voice in children:
            v = self.GetChild(voice)
            indexes = v.GetChildrenIndexes()
            for index in indexes:
                notes += 1
                note = v.GetChild(index)
                total += note.duration
                if total >=duration:
                    break
        self.index -= notes

    def addVoice(self, item, id):
        self.AddChild(item, id)

    def getVoice(self, key):
        return self.GetChild(key)

    def PositionChild(self, item, key, voice=1):
        voice_obj = self.getVoice(voice)
        children = voice_obj.GetChildrenIndexes()
        if key in children:
            start_index = key
            end_index = children[-1]
            popped = []
            for index in range(start_index, end_index+1):
                popped.append(voice_obj.PopChild(index))
            voice_obj.AddChild(item)
            [voice_obj.AddChild(p) for p in popped]

    def addNote(self, item, voice=1, increment=1):
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.getVoice(voice)
        duration = 0
        if type(item) is not NoteNode and type(item) is not Placeholder:
            if hasattr(item, "duration"):
                duration = item.duration
            node = NoteNode(duration=duration)
            node.SetItem(item)
        else:
            node = item
        placeholder = voice_obj.GetChild(self.index)
        if type(placeholder) is Placeholder and type(node) is not Placeholder:
            if placeholder.duration == 0:
                voice_obj.ReplaceChild(self.index, node)
                if type(node) is not Placeholder:
                    self.index += 1

        elif placeholder is None:
            voice_obj.AddChild(node)
            if type(node) is not Placeholder:
                self.index += 1
        else:
            proposed_node = voice_obj.GetChild(self.index)
            new_duration = voice_obj.GetChild(self.index).duration
            if proposed_node.GetItem() is None:
                if hasattr(item, "duration"):
                    new_duration = item.duration
                if new_duration == proposed_node.duration:
                    node.SetItem(node.GetItem())
                    voice_obj.ReplaceChild(self.index, node)
                elif new_duration > proposed_node.duration:
                    proposed_node.SetItem(node.GetItem())
                    proposed_node.duration = new_duration
                elif new_duration < proposed_node.duration:
                    proposed_node.duration -= new_duration
                    voice_obj.AddChild(node)
                    if type(node) is not Placeholder:
                        self.index += 1
            else:
                self.PositionChild(node, self.index, voice=voice)



    def addPlaceholder(self, duration=0, voice=1):
        holder = Placeholder(duration=duration)
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.getVoice(voice)
        children = voice_obj.GetChildrenIndexes()
        if self.index == len(children):
            self.addNote(holder, voice)
        else:
            self.PositionChild(holder, self.index, voice=voice)
        return None


    def addDirection(self, item, voice=1):
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        direction_obj = DirectionNode()
        direction_obj.SetItem(item)
        voice_obj = self.getVoice(voice)
        note_obj = Search(NoteNode, voice_obj, self.index)
        plcholder = Search(Placeholder, voice_obj, self.index+1)
        if note_obj is not None or plcholder is not None:
            if note_obj is not None:
                note_obj.AttachDirection(direction_obj)
            if plcholder is not None:
                plcholder.AttachDirection(direction_obj)

        else:
            self.addPlaceholder()
            note_obj = Search(Placeholder, voice_obj, self.index+1)
            if type(note_obj) is Placeholder:
                note_obj.AttachDirection(direction_obj)

    def addExpression(self, item, voice=1):
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        direction_obj = ExpressionNode()
        direction_obj.SetItem(item)
        voice_obj = self.getVoice(voice)
        note_obj = voice_obj.GetChild(self.index)
        if type(note_obj) is NoteNode or type(note_obj) is Placeholder:
            note_obj.AttachExpression(direction_obj)
        else:
            self.addPlaceholder()
            note_obj = voice_obj.GetChild(self.index)
            if type(note_obj) is Placeholder:
                note_obj.AttachExpression(direction_obj)

    def toLily(self):
        lilystring = ""
        wrap = self.item.toLily()
        lilystring += wrap[0]
        voices = self.GetChildrenIndexes()
        for voice in voices:
            v_obj = self.getVoice(voice)
            lilystring += " % voice "+str(voice)+"\n"
            lilystring += v_obj.toLily()
        lilystring += wrap[1]
        lilystring += " | "
        return lilystring

class VoiceNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NoteNode, Placeholder])

    def toLily(self):
        lilystring = "{ "
        children = self.GetChildrenIndexes()
        for child in range(len(children)):
            note = self.GetChild(children[child])
            if len(children) == child+1:
                item = note.GetItem()
                if hasattr(item, "chord"):
                    if item.chord != "stop":
                        item.chord = "stop"
                result = item.Search(Note.GraceNote)
                if result is not None:
                    if not hasattr(result, "last") or not result.last:
                        result.last = True
            else:
                item = note.GetItem()
                next = self.GetChild(children[child+1])
                next_item = next.GetItem()
                if hasattr(item, "chord"):
                    if not hasattr(next_item, "chord"):
                        item.chord = "stop"
                    else:
                        item.chord = "start"
                result = item.Search(Note.GraceNote)
                next_result = next_item.Search(Note.GraceNote)
                if result is not None:
                    if next_result is None:
                        if not hasattr(result, "last") or not result.last:
                            result.last = True
                    else:
                        next_result.first = False
            lilystring += note.toLily() + " "

        lilystring += "}"
        return lilystring


class NoteNode(Node):
    """in order to maintain lilypond's output flow, Notes have a specific child order:
    - left: Expression (dynamic or other expressive thing that has to be attached to a note)
    - right: direction (anything that's not a note or expression"""
    def __init__(self, **kwargs):
        if "duration" in kwargs:
            self.duration = kwargs["duration"]
        Node.__init__(self, rules=[DirectionNode,ExpressionNode],limit=2)
        if self.item is None:
            self.item = Note.Note()

    def AttachDirection(self, item):
        if 2 > len(self.GetChildrenIndexes()) > 0:
            if self.GetChild(0) is not ExpressionNode:
                self.AttachExpression(ExpressionNode())
        if 1 > len(self.GetChildrenIndexes()) > 0:
            self.AddChild(item)
        else:
            dir_node = self.GetChild(1)
            if dir_node is not None:
                if dir_node.GetItem() is None:
                    dir_node.SetItem(item.GetItem())
                else:
                    parent = FindPosition(dir_node, item)
                    if parent is not None:
                        parent.AddChild(item)
            else:
                self.AddChild(item)

    def AttachExpression(self, new_node):
        if len(self.GetChildrenIndexes()) > 0:
            node = self.GetChild(0)
            if node is not ExpressionNode and node is not None:
                first_child = self.PopChild(0)
                self.AddChild(new_node)
                if first_child is not None:
                    self.AddChild(first_child)
            elif node is not None and node.GetItem() is None:
                node.SetItem(new_node.GetItem())
            if node is not None and node.GetItem() is not None:
                parent = FindPosition(node, new_node)
                if parent is not None:
                    parent.AddChild(new_node)
        else:
            self.AddChild(new_node)

    def toLily(self):
        lilystring = ""
        lilystring += self.item.toLily()
        children = self.GetChildrenIndexes()
        for child in children:
            lilystring += self.GetChild(child).toLily()
        return lilystring

class Placeholder(NoteNode):
    pass

class SelfNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[type(self)],limit=1)

    def toLily(self):
        lilystring = ""
        if self.item is not None:
            lilystring += self.item.toLily()
        child = self.GetChild(0)
        if child is not None:
            lilystring += child.toLily()
        return lilystring

class DirectionNode(SelfNode):
    pass

class ExpressionNode(SelfNode):
    pass