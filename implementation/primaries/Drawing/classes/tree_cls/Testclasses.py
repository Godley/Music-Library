from implementation.primaries.Drawing.classes.tree_cls.PieceTree import Tree, Node, IndexedNode, Search, FindByIndex, FindPosition

class PieceTree(Tree):
    def __init__(self):
        self.meta = None
        Tree.__init__(self)
        self.root = IndexedNode(rules=[PartNode])

    def getPart(self, key):
        return self.FindNodeByIndex(key)


class PartNode(IndexedNode):
    def __init__(self, parent):
        IndexedNode.__init__(self, rules=[StaffNode])

    def getMeasure(self, measure=1, staff=1):
        staff_obj = self.GetChild(staff)
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
        self.addMeasure(None, measure=measure, staff=staff)


class StaffNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[MeasureNode])

class MeasureNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[VoiceNode])
        self.index = 0

    def Forward(self, duration=0):
        for voice in self.GetChildrenIndexes():
            voice_obj = self.getVoice(voice)
            if voice_obj.GetChild(self.index) is None:
                voice_obj.AddChild(NoteNode(duration=duration))
        self.index += 1

    def Backup(self, duration=0):
        self.index -= 1

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
            self.addNote(item, voice)
            [self.addNote(p, voice) for p in popped]

    def addNote(self, item, voice=1):
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.getVoice(voice)
        duration = None
        if type(item) is not NoteNode:
            if hasattr(item, "duration"):
                duration = item.duration
            node = NoteNode(duration=duration)
            node.SetItem(item)
        else:
            node = item
        if voice_obj.GetChild(self.index) is None:
            voice_obj.AddChild(node)
        else:
            proposed_node = voice_obj.GetChild(self.index)
            new_duration = voice_obj.GetChild(self.index).duration
            if proposed_node.GetItem() is None:
                if hasattr(item, "duration"):
                    new_duration = item.duration
                if new_duration == proposed_node.duration:
                    node.SetItem(node.GetItem())
                elif new_duration > proposed_node.duration:
                    proposed_node.SetItem(node.GetItem())
                    proposed_node.duration = new_duration
                elif new_duration < proposed_node.duration:
                    proposed_node.duration -= new_duration
                    voice_obj.AddChild(node)
            else:
                self.PositionChild(node, self.index, voice=voice)
        self.index += 1


    def addPlaceholder(self, duration=0, voice=1):
        holder = NoteNode(duration=duration)
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
        if note_obj is not None:
            note_obj.AttachDirection(direction_obj)
        else:
            self.addPlaceholder()
            note_obj = Search(NoteNode, voice_obj, self.index)
            note_obj.AttachDirection(direction_obj)

    def addExpression(self, item, voice=1):
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        exp_obj = ExpressionNode()
        exp_obj.SetItem(item)
        voice_obj = self.getVoice(voice)
        note_obj = Search(NoteNode, voice_obj, self.index)
        if note_obj is not None:
            note_obj.AttachExpression(exp_obj)
        else:
            self.addPlaceholder()
            note_obj = Search(NoteNode, voice_obj, self.index)
            note_obj.AttachExpression(exp_obj)

class VoiceNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NoteNode])



class NoteNode(Node):
    """in order to maintain lilypond's output flow, Notes have a specific child order:
    - left: Expression (dynamic or other expressive thing that has to be attached to a note)
    - right: direction (anything that's not a note or expression"""
    def __init__(self, **kwargs):
        if "duration" in kwargs:
            self.duration = kwargs["duration"]
        Node.__init__(self, rules=[DirectionNode,ExpressionNode],limit=2)

    def AttachDirection(self, item):
        if self.GetChild(0) is not ExpressionNode:
            self.AttachExpression(ExpressionNode())
        parent = FindPosition(self, item)
        if parent is not None:
            parent.AddChild(item)

    def AttachExpression(self, item):
        if len(self.GetChildrenIndexes()) > 0:
            if self.GetChild(0) is not ExpressionNode:
                first_child = self.PopChild(0)
                self.AddChild(item)
                if first_child is not None:
                    self.AddChild(first_child)
        parent = FindPosition(self, item)
        if parent is not None:
            parent.AddChild(item)

class SelfNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[type(self)],limit=1)

class DirectionNode(SelfNode):
    pass

class ExpressionNode(SelfNode):
    pass