class CannotAddToTreeException(BaseException):
    '''error in tree addition!'''

class CannotFindInTreeException(BaseException):
    '''error! can't find element'''

class Node(object):
    """This class is very generic, and has 3 attributes:
        - children: as with any tree it needs to have children
        - limit: the maximum amount of children before castcading to the next level
        - rules: the class instances allowed to be children of this object """
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
        """adds the child to the list - index is included as an optional param but doesn't do anything because
        this allows us to ducktype between this and IndexedNode """
        self.children.append(item)

    def AddRule(self, rule):
        self.rules.append(rule)

class EmptyNode(Node):
    """This is a class used to represent gaps in note representation - i.e where we want to jump forward in the measure and then come back
    and fill the gap in later on. Used mostly in voices where we maybe want to fill in an extra voice at a specific moment"""
    def __init__(self, duration, **kwargs):
        limit = 0
        rules = []
        if "limit" in kwargs:
            limit = kwargs["limit"]
        if "rules" in kwargs:
            rules = kwargs["rules"]
        self.duration = duration
        Node.__init__(self, limit=limit, rules=rules)


class IndexedNode(Node):
    """same as node, except the children section have their own indexes. to be used in nodes like Piece and Part, as both have
    children which have indexes applied to them in xml"""
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
    """Your basic generic tree structure, but with a few improvements to handle automatic ruling."""
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
                if len(node.children) == 0:
                    return None
                result = self.FindPosition(node.GetChild(index), addition, index)
                if result is None:
                    index += 1
                child = index
                while result is None and child < len(node.children):
                    result = self.FindPosition(node.GetChild(child), addition, index)
                    child += 1
                return result
        else:
            if len(node.children) == 0:
                return None
            result = self.FindPosition(node.GetChild(index), addition, index)
            if result is None:
                index += 1
            child = index
            while result is None and child < len(node.children):
                result = self.FindPosition(node.GetChild(child), addition, index)
                child += 1
            return result

    def FindNode(self, cls_type, index):
        result = self.Search(cls_type, self.root, 0, count=index+1)
        if result is None:
            raise(CannotFindInTreeException("ERROR! could not find "+str(cls_type)+" index "+str(index)))
        return result

    def Search(self, cls_type, node, index, depth=0, count=1):
        counter = depth + 1
        if node is None:
            return None
        if type(node) == cls_type and counter == count:
            return node
        else:
            if type(node) != cls_type:
                counter -= 1
            if len(node.children) == 0:
                return None
            result = self.Search(cls_type, node.GetChild(index), index, depth=counter, count=count)
            if result is None:
                index += 1
            child = 0
            while result is None and child < len(node.children):
                result = self.Search(cls_type, node.GetChild(child), index, depth=counter, count=count)
                child += 1
            return result



