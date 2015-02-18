class CannotAddToTreeException(BaseException):
    '''error in tree addition!'''

class Node(object):
    def __init__(self, **kwargs):
        self.children = []
        if "limit" in kwargs:
            self.limit = kwargs["limit"]
        else:
            self.limit = 0
        self.item = None
        if "rules" in kwargs:
            self.rules = kwargs["rules"]
        else:
            self.rules = []

    def SetItem(self, new_item):
        self.item = new_item

    def GetItem(self):
        return self.item

    def GetChild(self, index):
        if index < len(self.children):
            return self.children[index]

    def AddChild(self, item, index=-1):
        self.children.append(item)

    def AddRule(self, rule):
        self.rules.append(rule)

class IndexedNode(Node):
    def __init__(self, **kwargs):
        limit = 0
        rules = []
        if "limit" in kwargs:
            limit = kwargs["limit"]
        if "rules" in kwargs:
            rules = kwargs["rules"]
        Node.__init__(self, rules=rules, limit=limit)
        self.children = {}

    def GetChild(self, index):
        if index in self.children:
            return self.children[index]

    def AddChild(self, item, index=-1):
        if index == -1:
            index = len(self.children)-1
        self.children[index] = item

class Tree(object):
    def __init__(self):
        self.root = None

    def AddNode(self, node, index=-1):
        if self.root is None:
            self.root = node
        else:
            position = self.FindPosition(self.root,node,0)
            if position is None:
                raise(CannotAddToTreeException("ERROR! could not find suitable position to put child in tree"))
            else:
                position.AddChild(node, index=index)

    def FindPosition(self, node, addition, index):
        if node is None:
            return None
        if type(addition) in node.rules:

            if len(node.children) < node.limit or node.limit == 0:
                return node
            else:
                return self.FindPosition(node.GetChild(index), addition, index+1)
        else:
            if len(node.children) == 0:
                return None
            else:
                if index < len(node.children):
                    return self.FindPosition(node.GetChild(index), addition, index+1)
                else:
                    return None

class EmptyNode(Node):
    def __init__(self, duration, **kwargs):
        limit = 0
        rules = []
        if "limit" in kwargs:
            limit = kwargs["limit"]
        if "rules" in kwargs:
            rules = kwargs["rules"]
        self.duration = duration
        Node.__init__(self, limit=limit, rules=rules)

