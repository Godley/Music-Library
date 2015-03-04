
try:
    from implementation.primaries.Drawing.classes.tree_cls.BaseTree import Tree, Node, IndexedNode, Search, BackwardSearch, FindByIndex, FindPosition, toLily
    from implementation.primaries.Drawing.classes import Measure, Note, Part, Piece, Directions
    from implementation.primaries.Drawing.classes.Directions import OctaveShift
    from implementation.primaries.Drawing.classes.Note import GraceNote, Arpeggiate, NonArpeggiate
except:
    from classes.tree_cls.BaseTree import Tree, Node, IndexedNode, Search, BackwardSearch, FindByIndex, FindPosition, toLily
    from classes import Measure, Note, Part, Piece, Directions
    from classes.Directions import OctaveShift
    from classes.Note import GraceNote, Arpeggiate, NonArpeggiate
import copy

def SplitString(value):
    """simple method that puts in spaces every 10 characters"""
    string_length = len(value)
    chunks = int(string_length / 10)
    string_list = list(value)
    lstring = ""

    if chunks > 1:
        lstring = "\\markup { \n\r \column { "
        for i in range(int(chunks)):
            lstring += "\n\r\r \\line { \""
            index = i*10
            for i in range(index):
                lstring += string_list[i]
            lstring += "\" \r\r}"
        lstring += "\n\r } \n }"
    if lstring == "":
        indexes = [i for i in range(len(string_list)) if string_list[i] == "\r" or string_list[i] == "\n"]
        lstring = "\\markup { \n\r \column { "
        if len(indexes) == 0:
            lstring += "\n\r\r \\line { \"" + "".join(string_list) + "\" \n\r\r } \n\r } \n }"
        else:
            rows = []
            row_1 = string_list[:indexes[0]]
            rows.append(row_1)
            for i in range(len(indexes)):
                start = indexes[i]
                if i != len(indexes)-1:
                    end = indexes[i+1]
                else:
                    end = len(string_list)
                row = string_list[start:end]
                rows.append(row)

            for row in rows:
                lstring += "\n\r\r \\line { \""
                lstring += "".join(row)
                lstring += "\" \r\r}"
            lstring += "\n\r } \n }"
    return lstring

# \markup {
#     \column { "Clarinetti"
#       \line { "in B" \smaller \flat }
#     }
#   }

class PieceTree(Tree):
    def __init__(self):
        Tree.__init__(self)
        self.root = IndexedNode(rules=[PartNode])
        self.item = Piece.Piece()
        self.groups = {}
        self.current = []

    def SetValue(self, item):
        self.root.SetItem(item)

    def getLastPart(self):
        indexes = self.root.GetChildrenIndexes()
        if len(indexes) > 0:
            return self.getPart(indexes[-1])

    def addPart(self, item, index=-1):
        node = PartNode(index=index)
        node.SetItem(item)
        self.AddNode(node, index=index)
        if len(self.current) > 0:
            for item in self.current:
                self.AddToGroup(item, index)

    def startGroup(self, index):
        if index not in self.groups:
            self.groups[index] = []
        if index not in self.current:
            self.current.append(index)

    def stopGroup(self, index):
        if index in self.current:
            self.current.remove(index)

    def AddToGroup(self, name, index):
        if name not in self.groups:
            self.groups[name] = []
        if type(index) == str and index not in self.groups[name]:
            self.groups[name].append(index)
        elif type(index) == list:
            self.groups[name].append(index)

    def getGroup(self, name):
        if name in self.groups:
            return self.groups[name]

    def getPart(self, key):
        return self.FindNodeByIndex(key)

    def GetItem(self):
        return self.item

    def SetItem(self, i):
        self.item = i

    def handleGroups(self):
        lilystring = ""
        ids_loaded = []
        groupings = []
        group_ids = sorted(self.groups, key=lambda k: len(self.groups[k]), reverse=True)
        for i in range(len(group_ids)):
            merger = []
            for j in range(i+1, len(group_ids)):
                for k in self.groups[group_ids[j]]:
                    if k in self.groups[group_ids[i]]:
                        merger.append(k)
            if len(merger) > 0:
                for group in group_ids:
                    [self.groups[group].remove(a) for a in self.groups[group] if a in merger]
                self.AddToGroup(group_ids[i], merger)
        for group in group_ids:
            groupstr = "\\new StaffGroup <<"
            not_nested = [g for g in self.groups[group] if type(g) != list]
            not_nested.sort()
            not_nested.extend([g for g in self.groups[group] if type(g) == list])
            for element in not_nested:
                if type(element) is not list and element not in ids_loaded:
                    part = self.getPart(element)
                    pstring = part.toLily()
                    lilystring += pstring[0]
                    groupstr += pstring[1]
                    ids_loaded.append(element)
                elif type(element) is list:
                    groupstr += "\\new StaffGroup <<"
                    for nested_part in element:
                        part = self.getPart(nested_part)
                        pstring = part.toLily()
                        lilystring += pstring[0]
                        groupstr += pstring[1]
                        ids_loaded.append(nested_part)
                    groupstr += ">>"
            groupstr += ">>"
            groupings.append(groupstr)
        return lilystring, groupings, ids_loaded

    def toLily(self):
        lilystring = "\\version \"2.18.2\" \n"

        partstrings = []
        ids_loaded = []
        groupings = []
        if len(self.groups) > 0:
            # here we need to do some set union theory
            lstring, groupings, ids_loaded = self.handleGroups()
            lilystring += lstring
        children = [child for child in self.root.GetChildrenIndexes() if child not in ids_loaded]
        children.sort()
        for child in children:
            part = self.getPart(child)
            partstring = part.toLily()
            lilystring += partstring[0]
            partstrings.append(partstring[1])
        lilystring += self.item.toLily()
        lilystring += "<<"
        lilystring += "".join([gstring for gstring in groupings])
        lilystring += "".join([partstring for partstring in partstrings])
        lilystring += ">>"
        return lilystring


class PartNode(IndexedNode):
    def __init__(self, index=0):
        IndexedNode.__init__(self, rules=[StaffNode])
        self.index = index
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
            if measure_obj is not None:
                if hasattr(measure_obj.GetItem(), "divisions"):
                    divisions = measure_obj.GetItem().divisions
                elif divisions is not None:
                    measure_obj.GetItem().divisions = divisions

    def CheckMeasureMeter(self, measure):
        meter = None
        staves = self.GetChildrenIndexes()
        for staff in staves:
            measure_obj = self.getMeasure(measure, staff)
            if measure_obj is not None:
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

    def CheckIfTabStaff(self, measure):
        staves = self.GetChildrenIndexes()
        for staff in staves:
            stave = self.getStaff(staff)
            measureNode = self.getMeasure(measure, staff)
            if measureNode is not None:
                item = measureNode.GetItem()
                if hasattr(item, "clef"):
                    clef = item.clef
                    if clef.sign == "percussion" and not hasattr(stave, "drum"):
                        stave.drum = True
                    else:
                        stave.drum = False
                        break

                    if clef.sign == "TAB" and not hasattr(stave, "tab"):
                        stave.tab = True

                    else:
                        stave.tab = False
                        break

            if hasattr(stave, "tab") and stave.tab:
                return "ERROR: THIS APPLICATION DOES NOT HANDLE TAB NOTATION"
            if hasattr(stave, "drum") and stave.drum:
                return "ERROR: THIS APPLICATION DOES NOT HANDLE DRUM NOTATION"

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
        shortname = ""
        if hasattr(self.item, "name"):
            name = self.item.name
            name = SplitString(name)
        if hasattr(self.item, "shortname"):
            shortname = SplitString(self.item.shortname)
        variables = self.CalculateVariable(str(self.index), staves)
        first_part = ""
        for staff, variable in zip(staves, variables):
            staffstring = variable
            if hasattr(self.GetChild(staff), "tab") and self.GetChild(staff).tab:
                staffstring += " = \\new TabStaff"
            elif hasattr(self.GetChild(staff), "drum") and self.GetChild(staff).drum:
                staffstring += " = \\drums"
            else:
                staffstring += " = \\new Staff"
            if len(staves) == 1:
                if name != "":
                    staffstring += " \with {\n"
                    staffstring += "instrumentName = "+ name +" \n"
                    if shortname != "":
                        staffstring += "shortInstrumentName = "+ shortname +" \n"
                    staffstring += " }"
            staffstring += "{"+self.GetChild(staff).toLily() + " }\n\n"
            first_part += staffstring

        second_part = ""
        if len(variables) > 1:
            second_part += "\\new StaffGroup "
            if name != "":
                second_part += "\with {\n"
                second_part += "instrumentName = "+ name +" \n"
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
        if not hasattr(self, "transpose"):
            self.transpose = None
        for child in range(len(children)):
            measureNode = self.GetChild(children[child])
            measure = measureNode.GetItem()
            # if hasattr(measure, "transpose"):
            #     if self.transpose is None:
            #         self.transpose = True
            #     else:
            #         lilystring += "}"
            lilystring += " % measure "+str(children[child])+"\n"
            lilystring += measureNode.toLily()+"\n\n"

            right_barline = measure.GetBarline("right")
            if right_barline is not None and hasattr(right_barline, "ending"):
                if len(children) == child+1:
                    lilystring += "}"
                else:
                    nxt_measure = self.GetChild(children[child+1]).GetItem()
                    left_bline = nxt_measure.GetBarline("left")
                    if not hasattr(left_bline, "ending"):
                        lilystring += "}"
        # if self.transpose:
        #     lilystring += "}"
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
        if self.item is None or not hasattr(self, "item"):
            self.item = Measure.Measure()

    def GetLastKey(self, voice=1):
        """key as in musical key, not index"""
        voice_obj = self.GetChild(voice)
        if voice_obj is not None:
            key = BackwardSearch(KeyNode, voice_obj, 1)
            if key is not None:
                return key
            else:
                if hasattr(self.item, "key"):
                    return self.item.key

    def addKey(self, item, voice=1):
        if not hasattr(self.item, "key"):
            self.item.key = item
        else:
            if self.GetChild(voice) is None:
                self.addVoice(VoiceNode(), voice)
            voice_obj = self.GetChild(voice)
            node = KeyNode()
            node.SetItem(item)
            if voice_obj is not None:
                voice_obj.AddChild(node)
                self.index += 1

    def GetLastClef(self, voice=1):
        if self.GetChild(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.GetChild(voice)
        if voice_obj is not None:
            key = BackwardSearch(ClefNode, voice_obj, 1)
            if key is not None:
                return key
            else:
                if hasattr(self.item, "clef"):
                    return self.item.clef

    def addClef(self, item, voice=1):
        if not hasattr(self.item, "clef"):
            self.item.clef = item
        else:
            voice_obj = self.GetChild(voice)
            node = ClefNode()
            node.SetItem(item)
            if voice_obj is not None:
                voice_obj.AddChild(node)
                self.index += 1

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
                if hasattr(note, "duration"):
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
        shift = 0
        # get the appropriate voice
        if self.getVoice(voice) is None:
            self.addVoice(VoiceNode(), voice)
        voice_obj = self.getVoice(voice)

        # get last note and check it's shifter
        last = voice_obj.GetChild(self.index-1)
        if last is not None:
            if hasattr(last, "shift"):
                shift = last.shift
                if hasattr(item, "GetItem"):
                    item.GetItem().pitch.octave += last.shift
                elif item.__class__.__name__ == Note.Note.__name__:
                    value = int(item.pitch.octave) + last.shift
                    item.pitch.octave = str(value)

        # set up a basic duration: this val will only be used for a placeholder
        duration = 0
        if type(item) is not NoteNode and type(item) is not Placeholder:
            # wrap the item in a node if it isn't wrapped already
            if hasattr(item, "duration"):
                duration = item.duration
            node = NoteNode(duration=duration)
            node.SetItem(item)
            if shift != 0:
                node.shift = shift
        else:
            node = item
            if shift != 0:
                node.shift = shift
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
            if placeholder.GetItem() is not None:
                if hasattr(placeholder.GetItem(), "beams"):
                    node.GetItem().beams = placeholder.GetItem().beams
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
        if self.index == 0:
            finder = 0
        else:
            finder = self.index-1
        note_obj = voice_obj.GetChild(finder)
        if type(note_obj) is NoteNode or type(note_obj) is Placeholder:
            note_obj.AttachDirection(direction_obj)
        else:
            self.addPlaceholder()
            note_obj = voice_obj.GetChild(self.index)
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
        if len(voices) > 1:
            lilystring += "<<"
        for voice in voices:
            v_obj = self.getVoice(voice)
            if hasattr(self, "rest"):
                v_obj.total = self.value
            if len(voices) > 1:
                lilystring += " % voice "+str(voice)+"\n"
                lilystring += "\\new Voice = \""+Part.NumbersToWords(voice)+"\"\n"
                lilystring += "{\\voice"+Part.NumbersToWords(voice).capitalize() + " "
            lilystring += v_obj.toLily()
            if len(voices) > 1:
                lilystring += "}"
        if len(voices) > 1:
            lilystring += ">>"
        lilystring += wrap[1]

        return lilystring

class VoiceNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[NoteNode, Placeholder])

    def toLily(self):
        lilystring = ""
        children = self.GetChildrenIndexes()
        close = False
        previous = None
        for child in range(len(children)):
            note = self.GetChild(children[child])
            item = note.GetItem()
            if item is not None and type(note) == NoteNode:
                arpeg = item.Search(Arpeggiate)
                narpeg = item.Search(NonArpeggiate)
                if arpeg is not None or narpeg is not None:
                    note.UpdateArpeggiates()
                if len(children) == child+1:
                    result = item.Search(GraceNote)
                    if result is not None:
                        note.CheckForGraceNotes()

                    if hasattr(item, "timeMod"):

                        close = True
                        if previous is not None:
                            if hasattr(previous.GetItem(), "timeMod"):
                                item.timeMod.first = False
                            else:
                                item.timeMod.first = True
                        else:
                            item.timeMod.first = True
                    else:
                        close = False
                else:
                    next = self.GetChild(children[child+1])
                    next_item = next.GetItem()
                    if next_item is not None and type(next) is NoteNode:
                        result = item.Search(GraceNote)
                        next_result = next_item.Search(GraceNote)
                        if result is not None:
                            if next_result is None:
                                note.CheckForGraceNotes()
                            else:
                                result.last = False
                                next_result.first = False
                        if hasattr(item, "timeMod"):
                            res = item.Search(Note.Tuplet)

                            if not hasattr(next_item, "timeMod") and res is None:
                                close = True
                            else:
                                close = False
                            if previous is not None and type(previous) is NoteNode:
                                if hasattr(previous.GetItem(), "timeMod"):
                                    item.timeMod.first = False
                                else:
                                    item.timeMod.first = True
                            else:
                                item.timeMod.first = True
                        else:
                            close = False
            if hasattr(self, "rest") and hasattr(self, "total"):
                lilystring += "R"+self.total
            else:
                lilystring += note.toLily() + " "
            if close:
                lilystring += "} "
            previous = note
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

    def SetGrace(self):
        if self.item.Search(GraceNote) is None:
            self.item.addNotation(GraceNote())

    def SetLast(self):
        result = self.item.Search(GraceNote)
        if result is not None:
            result.last = True

    def UpdateArpeggiates(self, type="start"):
        result = self.item.Search(Arpeggiate)
        if result is not None:
            if type=="start":
                result.type = type
            child = self.GetChild(0)
            if child is not None:
                if child.item.Search(Arpeggiate) is None:
                    new_obj = copy.deepcopy(result)
                    new_obj.type = "none"
                    child.GetItem().addNotation(new_obj)
                if child is not None and hasattr(child, "UpdateArpeggiates"):
                    child.UpdateArpeggiates(type="stop")
            else:
                result.type = type
        else:
            result = self.item.Search(NonArpeggiate)
            if result is not None:
                if type=="start":
                    result.type = type
                child = self.GetChild(0)
                if child is not None:
                    search = child.item.Search(NonArpeggiate)
                    if search is None:
                        cpy = copy.deepcopy(result)
                        cpy.type = "none"
                        child.item.addNotation(cpy)
                    if hasattr(child, "UpdateArpeggiates"):
                        child.UpdateArpeggiates(type="stop")
                else:
                    result.type = type


    def CheckForGraceNotes(self):
        result = self.item.Search(GraceNote)
        if result is not None:
            first_child = self.GetChild(0)
            if type(self.GetChild(0)) is NoteNode:
                first_child.SetGrace()
                first_child.CheckForGraceNotes()
            else:
                self.SetLast()

    def AttachDirection(self, item):
        if item.GetItem().__class__.__name__ == OctaveShift.__name__:
            amount = item.GetItem().amount
            direction = item.GetItem().type
            converter = {8:1,15:2,0:0}
            if direction == "up":
                self.shift = converter[amount]*2
            if direction == "down":
                self.shift = (converter[amount] * -1)*2
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
                if type(new_note.GetItem()) != int and type(new_note.GetItem()) != str:
                    post, pre, wrap = new_note.GetItem().GetAllNotation()
                    [self.GetItem().addNotation(n) for n in post if self.GetItem().Search(type(n)) is None]
                    [self.GetItem().addNotation(p) for p in pre if self.GetItem().Search(type(p)) is None]
                    [self.GetItem().addNotation(w) for w in wrap if self.GetItem().Search(type(w)) is None]
                    new_note.GetItem().FlushNotation()
                self.PositionChild(0, new_note)
        else:
            if type(new_note.GetItem()) != int and type(new_note.GetItem()) != str:
                post, pre, wrap = new_note.GetItem().GetAllNotation()
                [self.GetItem().addNotation(n) for n in post if self.GetItem().Search(type(n)) is None]
                [self.GetItem().addNotation(p) for p in pre if self.GetItem().Search(type(p)) is None]
                [self.GetItem().addNotation(w) for w in wrap if self.GetItem().Search(type(w)) is None]
                new_note.GetItem().FlushNotation()
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
                return_val = self.GetChild(child).toLily()
                if type(return_val) == str:
                    lilystring += return_val
                else:
                    lilystring = return_val[0] + lilystring + return_val[1]
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

    def toLily(self):
        return ""

class SelfNode(Node):
    def __init__(self):
        Node.__init__(self, rules=[type(self)],limit=1)

    def toLily(self):
        lilystring = ""
        if self.item is not None:
            lstring = self.item.toLily()
            if type(lstring) == str:
                lilystring += lstring
            else:
                lilystring = lstring
        child = self.GetChild(0)
        if child is not None:
            if type(lilystring) == str:
                lilystring += child.toLily()
            else:
                lilystring.append(child.toLily())
        return lilystring

class DirectionNode(SelfNode):
    pass

class ExpressionNode(SelfNode):
    pass

class KeyNode(Node):
    def __init__(self):
        Node.__init__(self,limit=-1)

    def toLily(self):
        lstring = ""
        if self.item is not None:
            lstring += self.item.toLily()
        return lstring

class ClefNode(KeyNode):
    pass