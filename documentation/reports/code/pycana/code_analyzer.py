from inspect import *
from pygraphviz import AGraph
from collections import defaultdict
from itertools import chain

from relations import *

def is_container(var):
    return isinstance(var, list) or isinstance(var, dict) or isinstance(var, set)

def itercontainer(c):
    assert is_container(c)
    if isinstance(c, list):
        return ([e] for e in c)
    elif isinstance(c, dict):
        return c.iteritems()
    elif isinstance(c, set):
        return ([e] for e in c)

class CodeAnalyzer(object):
    def __init__(self, *base_modules):
        self.base_modules= base_modules
        self.already_checked= set()

    def analyze(self, exceptions=None):
        variables= currentframe(1).f_locals
        module_vars= []
        for varname, var in variables.iteritems():
            if self._belongs_to_module(var):
                module_vars.append(var)

        aggregation_relations= defaultdict(set)
        for var in module_vars:
            self._get_aggregation_relations(var, module_vars, aggregation_relations)

        if exceptions is not None:
            for klass in exceptions:
                if klass in aggregation_relations: aggregation_relations.pop(klass)

                for other_klass, related in aggregation_relations.iteritems():
                    aggregation_relations[other_klass]= set(r for r in related if not r.object2 == klass)
        

        all_classes= set(aggregation_relations.keys())
        for related in aggregation_relations.itervalues():
            all_classes.update(i.object2 for i in related)


        # prune aggregation relations
        inheritance_relations= self._build_inheritance_relations(all_classes)
        for n1, parents in inheritance_relations.iteritems():
            to_remove= set()
            for pr in parents:
                for agr2 in aggregation_relations.get(pr.object2, []):
                    if agr2 in to_remove: continue
                    for agr1 in aggregation_relations.get(n1, []):
                        if agr1 in to_remove: continue
                        if agr1.object2 == agr2.object2 and agr1.attrname == agr2.attrname:
                            to_remove.add(agr1)
            
            for agr in to_remove:
                if agr not in aggregation_relations[n1]: import ipdb;ipdb.set_trace()
                aggregation_relations[n1].remove(agr)


        relations= aggregation_relations
        for klass, related in inheritance_relations.iteritems():
            relations[klass].update(related)

        return relations

    def _build_inheritance_relations(self, all_classes):
        inheritance_relations= defaultdict(list)
 
        new_classes= set()
        for n1 in all_classes:
            for i, super_n1 in enumerate(n1.mro()[1:-1]):
                if any(issubclass(super_n1, klass) for klass in n1.mro()[1:1+i]): 
                    continue
                if super_n1 not in all_classes: 
                    new_classes.add(super_n1)
                relation= InheritanceRelation(n1, super_n1)
                inheritance_relations[n1].append(relation)

        all_classes.update(new_classes) 

        for n1 in all_classes:
            for n2 in all_classes:
                if n1 == n2: continue
                if issubclass(n1, n2):
                    for relation in inheritance_relations[n1]:
                        if issubclass(n2, relation.object2): break
                    else:
                        inheritance_relations[n1].append(InheritanceRelation(n1, n2))
        
        for n1 in all_classes:
            to_remove= []
            for r1 in inheritance_relations.get(n1, []):
                n2= r1.object2
                for r2 in inheritance_relations.get(n2, []):
                    n3= r2.object2
                    for r in inheritance_relations[n1]:
                        if r.object2 == n3: to_remove.append(r)

            for r in to_remove:
                inheritance_relations[n1].remove(r)

                
        return inheritance_relations

    def _belongs_to_module(self, var):
        try: 
            var_module= getmodule(var.__class__)
            return any(var_module.__name__.startswith(base_module.__name__) for base_module in self.base_modules)
        except AttributeError: 
            return False
        except Exception, e:
            import ipdb;ipdb.set_trace()
            return False
        
    def _get_aggregation_relations(self, module_var, module_vars, aggregation_relations):
        assert module_var in module_vars
        if id(module_var) in self.already_checked: return

        aggregation_relations[module_var.__class__]

        for attrname, attrvalue in getmembers(module_var):
            if not self._is_member_interesting(attrname): continue
            if self._belongs_to_module(attrvalue):
                if attrvalue not in module_vars:
                    module_vars.append(attrvalue)
                    self._get_aggregation_relations(attrvalue, module_vars, aggregation_relations)

                relation= AggregationRelation(module_var.__class__, attrvalue.__class__, attrname, is_multiple=False)
                aggregation_relations[module_var.__class__].add(relation)

            if is_container(attrvalue):
                container_module_vars= self._container_relations(attrvalue, module_vars, aggregation_relations)
                for container_module_var in container_module_vars:
                    relation= AggregationRelation(module_var.__class__, container_module_var.__class__, attrname, is_multiple=True)
                    aggregation_relations[module_var.__class__].add(relation)


        self.already_checked.add(id(module_var))


    def _container_relations(self, container, module_vars, aggregation_relations):
        container_module_vars= []
        for iterable in itercontainer(container):
            for e in iterable:
                if self._belongs_to_module(e):
                    container_module_vars.append(e)
                    if not e in module_vars: module_vars.append(e)
                    self._get_aggregation_relations(e, module_vars, aggregation_relations)
                elif is_container(e):
                    container_module_vars.extend(self._container_relations(e, module_vars, aggregation_relations))
        return container_module_vars                    

    def draw_relations(self, relations, fname, draw_packages=False, package_function=None):
        def get_node_name(n):
            return getmodule(n).__name__ + ':' + n.__name__

        g= AGraph(directed=True)
        for relation in chain(*relations.itervalues()):
            g.add_node(get_node_name(relation.object1))
            g.add_node(get_node_name(relation.object2))

        if draw_packages:
            assert package_function is not None
            subgraphs= defaultdict(list)
            for n in g.nodes():
                package= package_function(n)
                if package:
                    subgraphs[package].append(n)
            
            for i, (package, nodes) in enumerate(subgraphs.iteritems()):
                subgraph= g.subgraph(nbunch=nodes, name='cluster%s' % i, color='black', label=package)

        for relation in chain(*relations.itervalues()):
            n1_name= get_node_name(relation.object1)
            n2_name= get_node_name(relation.object2)
            g.add_edge(n1_name, n2_name)

            e= g.get_edge(n1_name, n2_name)
            relation.set_edge_attributes(e)

        for n in g.nodes():
            n.attr['shape']= 'box'




        g.draw(fname, prog='dot', args='-Grankdir=TB')
        
    def _is_member_interesting(self, attrname):
        return not attrname in ['__setattr__',
                                '__reduce_ex__',
                                '__new__',
                                '__reduce__',
                                '__str__',
                                '__getattribute__',
                                '__class__',
                                '__delattr__',
                                '__repr__',
                                '__hash__',
                                '__doc__',
                                '__init__',
                                '__dict__',
                                '__module__',
                                '__weakref__']

                                            
    
