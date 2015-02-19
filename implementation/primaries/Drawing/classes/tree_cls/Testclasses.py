from implementation.primaries.Drawing.classes.tree_cls.PieceTree import Tree, Node, IndexedNode, EmptyNode

class PieceTree(Tree):
    def __init__(self):
        self.meta = None
        Tree.__init__(self)
        self.root = IndexedNode(rules=[PartNode])

    def getPart(self, key):
        return self.FindNodeByIndex(key)

    def getMeasure(self, measure=1, staff=1, part=None):
        staff_obj = self.getStaff(staff, part)
        measure_obj = self.FindByIndex(staff_obj, measure)
        return measure_obj

    def getStaff(self, key, part):
        part_obj = self.getPart(part)
        staff = self.FindByIndex(part_obj, key)
        return staff

    def addMeasure(self, item, measure=1, staff=1, part=None):
        staff_obj = self.getStaff(staff, part)
        measure_node = MeasureNode()
        measure_node.SetItem(item)
        staff_obj.AddChild(measure_node, index=measure)

class PartNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[StaffNode])




class StaffNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[MeasureNode])

class MeasureNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[VoiceNode])

class VoiceNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NoteNode, PlaceHolder])

class PlaceHolder(Node):
    def __init__(self, **kwargs):
        if "duration" in kwargs:
            self.duration = kwargs["duration"]
        Node.__init__(rules=[NoteNode, DirectionNode,ExpressionNode], limit=3)

class NoteNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NoteNode,DirectionNode,ExpressionNode],limit=3)

class SelfNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[type(self)],limit=1)

class DirectionNode(SelfNode):
    pass

class ExpressionNode(SelfNode):
    pass