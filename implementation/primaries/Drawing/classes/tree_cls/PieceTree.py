
try:
    from implementation.primaries.Drawing.classes.tree_cls.BaseTree import Tree, Node, IndexedNode, Search, FindByIndex, FindPosition, toLily
    from implementation.primaries.Drawing.classes import Measure, Note, Part, Piece, Directions
except:
    from classes.tree_cls.BaseTree import Tree, Node, IndexedNode, Search, FindByIndex, FindPosition, toLily
    from classes import Measure, Note, Part, Piece, Directions
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
        lilystring = ""
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
        for staff in staves:
            child = self.getStaff(staff)
            child.CheckDivisions()

    def CheckTotals(self):
        """method to calculate the maximum total lilypond value for a measure without a time signature"""
        staves = self.GetChildrenIndexes()
        for staff in staves:
            child = self.getStaff(staff)
            child.CheckTotals()

    def CheckMeasureDivisions(self, measure):
        divisions = None
        staves = self.GetChildrenIndexes()
        for staff in staves:
            measure_obj = self.getMeasure(measure, staff)
            if hasattr(measure_obj.GetItem(), "divisions"):
                divisions = measure_obj.GetItem().divisions
            elif divisions is not None:
                measure_obj.GetItem().divisions = divisions

    def CheckMeasureMeter(self, measure):
        meter = None
        staves = self.GetChildrenIndexes()
        for staff in staves:
            measure_obj = self.getMeasure(measure, staff)
            item = measure_obj.GetItem()
            if hasattr(item, "meter"):
                meter = item.meter
            else:
                if meter is not None:
                    item.meter = meter

    def setDivisions(self, measure=1,divisions=1):
        staves = self.GetChildrenIndexes()
        for staff in staves:
            measure_obj = self.getMeasure(measure, staff)
            measure_obj.GetItem().divisions = divisions

    def getMeasure(self, measure=1, staff=1):
        staff_obj = self.GetChild(staff)
        measure_obj = None
        if staff_obj is not None:
            measure_obj = staff_obj.GetChild(measure)
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

    def CalculateVariable(self, name, staves):
        variables = []
        for staff in staves:
            variable = ""
            if len(name) > 0:
                lcase = name.lower()
                no_spaces = lcase.replace(' ', '')
                no_dots = no_spaces.replace('.', '')
                variable = ""
                for letter in no_dots:
                    if letter in [str(i) for i in range(10)]:
                        variable += Part.NumbersToWords(int(letter))
                    else:
                        variable += letter
            variable += "staff"+Part.NumbersToWords(staff)
            variables.append(variable)
        return variables

    def toLily(self):
        self.CheckDivisions()
        self.CheckTotals()
        staves = self.GetChildrenIndexes()
        name = ""
        if hasattr(self.item, "name"):
            name = self.item.name
        if hasattr(self.item, "shortname") and self.item.shortname is not None and (not hasattr(self.item, "name") or len(self.item.name) > 10):
            name = self.item.shortname
        variables = self.CalculateVariable(name, staves)
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

    def CheckTotals(self):
        measures = self.GetChildrenIndexes()
        total = "1"
        for m_id in measures:
            mNode = self.GetChild(m_id)
            mItem = mNode.GetItem()
            mItemTotal = mItem.GetTotalValue()
            if mItemTotal == "":
                mNode.value = total
            else:
                total = mItemTotal
                mNode.value = mItemTotal

    def toLily(self):
        lilystring = "\\autoBeamOff"
        children = self.GetChildrenIndexes()
        for child in range(len(children)):
            measureNode = self.GetChild(children[child])
            lilystring += " % measure "+str(children[child])+"\n"
            lilystring += measureNode.toLily()+"\n\n"
            measure = measureNode.GetItem()
            right_barline = measure.GetBarline("right")
            if right_barline is not None and hasattr(right_barline, "ending"):
                if len(children) == child+1:
                    lilystring += "}"
                else:
                    nxt_measure = self.GetChild(children[child+1]).GetItem()
                    left_bline = nxt_measure.GetBarline("left")
                    if not hasattr(left_bline, "ending"):
                        lilystring += "}"

        return lilystring

    def CheckDivisions(self):
        children = self.GetChildrenIndexes()
        divisions = 1
        for child in children:
            measure = self.GetChild(child)
            item = measure.GetItem()
            if hasattr(item, "divisions"):
                divisions = item.divisions
            else:
                item.divisions = divisions
            measure.CheckDivisions()

class MeasureNode(IndexedNode):
    def __init__(self):
        IndexedNode.__init__(self, rules=[VoiceNode])
        self.index = 0
        if self.item is None:
            self.item = Measure.Measure()

    def CheckDivisions(self):
        children = self.GetChildrenIndexes()
        divisions = self.item.divisions
        for child in children:
            voice = self.GetChild(child)
            indexes = voice.GetChildrenIndexes()
            for i in indexes:
                note = voice.GetChild(i)
                item = note.GetItem()
                if item is not None:
                    item.divisions = divisions

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
        if key not in self.children:
            self.AddChild(VoiceNode(), key)
        return self.GetChild(key)

    def PositionChild(self, item, key, voice=1):
        voice_obj = self.getVoice(voice)
        children = voice_obj.GetChildrenIndexes()
        if key in children:
            start_index = key
            end_index = len(children)
            popped = []
            for index in range(start_index, end_index):
                child = voice_obj.PopChild(index)
                if child is not None:
                    popped.append(child)
            voice_obj.AddChild(item)
            [voice_obj.AddChild(p) for p in popped]

    def addNote(self, item, voice=1, increment=1, chord=False):
        # get the appropriate voice
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.getVoice(voice)

        # set up a basic duration: this val will only be used for a placeholder
        duration = 0
        if type(item) is not NoteNode and type(item) is not Placeholder:
            # wrap the item in a node if it isn't wrapped already
            if hasattr(item, "duration"):
                duration = item.duration
            node = NoteNode(duration=duration)
            node.SetItem(item)
        else:
            node = item
        if not chord:
            #get whatever is at the current index
            placeholder = voice_obj.GetChild(self.index)
            if type(placeholder) is Placeholder and type(node) is not Placeholder:
                # if it's an empty placeholder, replace it with a note
                if placeholder.duration == 0:
                    voice_obj.ReplaceChild(self.index, node)
                    if type(node) is not Placeholder:
                        self.index += 1

            # nothing there? add our note
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

        else:
            #get whatever is at the current index
            placeholder = voice_obj.GetChild(self.index-1)
            if placeholder is not None:
                placeholder.AttachNote(node)


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
        wrappers = [Directions.Bracket]
        if type(item) in wrappers:
            self.item.addWrapper(item)
            return
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
        if self.index == 0:
            finder = 0
        else:
            finder = self.index-1
        note_obj = voice_obj.GetChild(finder)
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
        value = 1
        if hasattr(self, "rest"):
            if not hasattr(self, "value"):
                self.value = self.GetItem().GetTotalValue()
        for voice in voices:
            v_obj = self.getVoice(voice)
            if hasattr(self, "rest"):
                v_obj.total = self.value
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
            item = note.GetItem()
            if item is not None:
                if len(children) == child+1:
                    result = item.Search(Note.GraceNote)
                    if result is not None:
                        if not hasattr(result, "last") or not result.last:
                            result.last = True
                else:
                    next = self.GetChild(children[child+1])
                    next_item = next.GetItem()
                    if next_item is not None:
                        result = item.Search(Note.GraceNote)
                        next_result = next_item.Search(Note.GraceNote)
                        if result is not None:
                            if next_result is None:
                                if not hasattr(result, "last") or not result.last:
                                    result.last = True
                            else:
                                result.last = False
                                next_result.first = False
            if hasattr(self, "rest") and hasattr(self, "total"):
                lilystring += "R"+self.total
            else:
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
        Node.__init__(self, rules=[DirectionNode,ExpressionNode,NoteNode],limit=3)
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
        if len(self.children) > 0:
            if type(self.GetChild(0)) is DirectionNode:
                self.PositionChild(0, new_node)
            if type(self.GetChild(0)) is NoteNode:
                second = self.GetChild(1)
                if second is None:
                    self.AddChild(new_node)
                elif type(second) is ExpressionNode:
                    node = FindPosition(second, new_node)
                    node.AddChild(new_node)
                else:
                    self.PositionChild(1, new_node)
        else:
            self.AddChild(new_node)



    def AttachNote(self, new_note):
        if len(self.children) > 0:
            firstchild = self.GetChild(0)
            if type(firstchild) is NoteNode:
                firstchild.AttachNote(new_note)
            else:
                self.PositionChild(0, new_note)
        else:
            self.AddChild(new_note)

    def toLily(self):
        lilystring = ""
        if self.item is not None:
            if type(self.GetChild(0)) is not NoteNode:
                if hasattr(self.item, "chord") and self.item.chord:
                    self.item.chord = "stop"
            if type(self.GetChild(0)) is NoteNode:
                if not hasattr(self.item, "chord") or not self.item.chord:
                    self.item.chord = "start"
            lilystring += self.item.toLily()
        children = self.GetChildrenIndexes()
        for child in children:
            if self.GetChild(child) is not None:
                if type(self.GetChild(child)) is NoteNode:
                    lilystring += " "
                lilystring += self.GetChild(child).toLily()
            else:
                wat=True
        return lilystring

    def PositionChild(self, key, node):
        children = self.GetChildrenIndexes()
        if key in children:
            start = key
            popped = self.children[start:]
            self.children = self.children[:start]
            self.AddChild(node)
            [self.AddChild(pop) for pop in popped]


class Placeholder(NoteNode):
    def __init__(self, **kwargs):
        NoteNode.__init__(self, **kwargs)
        self.item = None

class SelfNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[type(self)],limit=1)

    def toLily(self):
        lilystring = ""
        if self.item is not None:
            if type(self.item.toLily()) is list:
                print(self.item)
            lilystring += self.item.toLily()
        child = self.GetChild(0)
        if child is not None:
            lilystring += child.toLily()
        return lilystring

class DirectionNode(SelfNode):
    pass

class ExpressionNode(SelfNode):
    pass