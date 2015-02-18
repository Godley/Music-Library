from implementation.primaries.Drawing.classes.tree_cls.PieceTree import Tree, Node, IndexedNode, EmptyNode

class PieceTree(Tree):
    def __init__(self):
        self.meta = None
        Tree.__init__(self)
        self.root = IndexedNode(rules=[PartNode])

class PartNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[MeasureNode])

class MeasureNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NoteNode], limit=3)

class PlaceHolder(EmptyNode):
    def __init__(self, **kwargs):
        duration = 0
        if "duration" in kwargs:
            duration = kwargs["duration"]
        EmptyNode.__init__(duration, rules=[NoteNode, DirectionNode,ExpressionNode], limit=3)

class NoteNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NotationNode,NoteNode,DirectionNode,ExpressionNode],limit=4)

class DirectionNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[DirectionNode], limit=2)

class ExpressionNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[ExpressionNode], limit=2)

class NotationNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NotationNode], limit=2)

