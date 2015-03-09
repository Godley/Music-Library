from inspect import isclass

class Relation(object):
    def __init__(self, object1, object2):
        self.object1= object1
        self.object2= object2

    def set_edge_attributes(self, edge):
        pass

class ClassRelation(Relation):
    def __init__(self, object1, object2):
        assert isclass(object1) and isclass(object2)
        super(ClassRelation, self).__init__(object1, object2)

class AggregationRelation(ClassRelation):
    def __init__(self, object1, object2, attrname, is_multiple):
        super(AggregationRelation, self).__init__(object1, object2)
        self.is_multiple= is_multiple
        self.attrname= attrname

    def set_edge_attributes(self, edge):
        if self.is_multiple:
            edge.attr['arrowhead']= 'crowodiamond'
        else:
            edge.attr['arrowhead']= 'odiamond'

        edge.attr['label']= self.attrname
            

class InheritanceRelation(ClassRelation):
    def set_edge_attributes(self, edge):
        edge.attr['arrowhead']= 'empty'
        
