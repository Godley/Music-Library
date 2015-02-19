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

    def addVoice(self, item, id):
        self.AddChild(item, id)

    def getVoice(self, key):
        return self.GetChild(key)

    def addNote(self, item, voice=1):
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.getVoice(voice)
        duration = None
        if hasattr(item, "duration"):
            duration = item.duration
        node = NoteNode(duration=duration)
        node.SetItem(item)
        voice_obj.AddChild(node)

    def addPlaceHolder(self, duration=0, voice=1):
        self.addNote(NoteNode(duration=duration), voice)

    def addDirection(self, item, note=1, voice=1):
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        direction_obj = DirectionNode()
        direction_obj.SetItem(item)
        voice_obj = self.getVoice(voice)
        note_obj = Search(NoteNode, voice_obj, note)
        if note_obj is not None:
            note_obj.AttachDirection(direction_obj)
        else:
            self.addPlaceHolder()
            note_obj = Search(NoteNode, voice_obj, note)
            note_obj.AttachDirection(direction_obj)

    def addExpression(self):
        pass

    def JumpForward(self, duration, current_note):
        pass

    def Backup(self, duration):
        pass

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
        wrapper = DirectionNode()
        wrapper.SetItem(item)
        if self.GetChild(0) is not ExpressionNode:
            self.AttachExpression(None)
        parent = FindPosition(self, wrapper)
        if parent is not None:
            parent.AddChild(wrapper)

    def AttachExpression(self, item):
        wrapper = ExpressionNode()
        wrapper.SetItem(item)
        if self.GetChild(0) is not ExpressionNode:
            first_child = None
            if len(self.GetChildrenIndexes()) > 0:
                first_child = self.PopChild(0)
            self.AddChild(wrapper)
            if first_child is not None:
                self.AddChild(first_child)
        parent = FindPosition(self, wrapper)
        if parent is not None:
            parent.AddChild(wrapper)

class SelfNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[type(self)],limit=1)

class DirectionNode(SelfNode):
    pass

class ExpressionNode(SelfNode):
    pass