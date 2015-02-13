try:
    from classes import BaseClass, Note, Directions
except:
    from implementation.primaries.Drawing.classes import BaseClass, Note, Directions

class Measure(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "width" in kwargs:
            self.width = float(kwargs["width"])
        self.items = {}
        self.preitems = {}
        self.expressions = {}
        self.notes = []
        self.forwards = {}
        self.octaveShift = {}


    def GetBarline(self, side):
        if hasattr(self, "barlines"):
            if side in self.barlines:
                return self.barlines[side]

    def AddBarline(self, side, item):
        if not hasattr(self, "barlines"):
            self.barlines = {}
        self.barlines[side] = item

    def CheckDivisions(self):
        if hasattr(self, "divisions"):
            for n in self.notes:
                if self.divisions is not None:
                    n.CheckDivisions(self.divisions)


    def __str__(self):
        self.CheckDivisions()
        ret_str = BaseClass.Base.__str__(self)
        return ret_str

    def HandleAttributes(self):
        lilystring = ""
        if hasattr(self, "clef") and self.clef is not None:
            lilystring += self.clef.toLily() + " "
        if hasattr(self, "key") and self.key is not None:
            lilystring += self.key.toLily() + " "
        if hasattr(self, "barlines"):
            if "left" in self.barlines:
                lilystring += self.barlines["left"].toLily()
            if "right" in self.barlines and hasattr(self.barlines["right"], "repeat") and self.barlines["right"] == "backward":
                lilystring += self.barlines["right"].toLily()
        return lilystring

    def toLily(self, start=0,end=-1):
        lilystring = ""
        values = []

        #handle stuff attached to measures which aren't directions
        lilystring = self.HandleAttributes()

        if len(self.notes) < 1 and len(self.forwards) == 0:
            #if a measure has no notes, it's probably a rest measure.
            lilystring += " r"

        # handle measures containing notes
        if len(self.notes) > 0:
            if end==-1:
                end = len(self.notes)
            duration_total = 0
            fwd_repeat = -1
            for n_id in range(start,end):
                if n_id in self.forwards:
                    if n_id == 0:
                        values.extend(self.forwards[n_id].toLily())
                        values.append(lilystring)
                    else:
                        value = self.forwards[n_id].toLily()
                        fwd_repeat = value[1]
                        lilystring += "\\repeat percent 2 {"
                if n_id in self.preitems:
                    lilystring += "".join([preitem.toLily() for preitem in self.preitems[n_id]])
                if hasattr(self.notes[n_id], "chord"):
                    if len(self.notes) > n_id+1:
                        if not hasattr(self.notes[n_id+1], "chord"):
                            self.notes[n_id].chord = "stop"
                    else:
                        self.notes[n_id].chord = "stop"
                if type(self.notes[n_id]) != str:
                    lilystring += " "+self.notes[n_id].toLily()
                if len(self.notes)-1 > n_id:
                    if hasattr(self.notes[n_id], "grace") and not hasattr(self.notes[n_id+1], "grace"):
                        lilystring += "}"
                elif hasattr(self.notes[n_id],"grace"):
                    lilystring += "}"
                #attach expressions to notes (these are classed as directions in mxml but in lilypond they have to be
                # attached to notes, e.g dynamics)
                if n_id in self.expressions:
                    lilystring += "".join([expr.toLily() for expr in self.expressions[n_id]])

                #add on direction strings, text, tempo markings etc
                if n_id in self.items:
                    # pull out all the toLily return values
                    return_values = [dir.toLily() for dir in self.items[n_id]]

                    # add the strings that aren't lists
                    lilystring += "".join([lilystr for lilystr in return_values if type(lilystr) != list])

                    # any that are lists are intended to be index 0 comes before the current lilystring,
                    # index 1 comes after, so wrap the current lilystring in them
                    lilystring = "".join([item[0] for item in return_values if type(item) == list]) + lilystring
                    lilystring += "".join([item[1] for item in return_values if type(item) == list])

                if fwd_repeat != -1:
                    if hasattr(self.notes[n_id], "duration"):
                        duration_total += self.notes[n_id].duration
                    if duration_total >= fwd_repeat:
                        lilystring += "}"
                        fwd_repeat = -1

        #could still have a measure without notes, so check those again
        elif len(self.items) > 0:
            if end == -1:
                end = len(self.items)
            for n_id in range(start, end):
                if n_id in self.forwards:
                    if n_id == 0:
                        values.extend(self.forwards[n_id].toLily())
                        values.append(lilystring)
                # pull out all the toLily return values
                if n_id in self.items:
                    return_values = [dir.toLily() for dir in self.items[n_id]]

                    # add the strings that aren't lists
                    lilystring += "".join([lilystr for lilystr in return_values if type(lilystr) != list])

                    # any that are lists are intended to be index 0 comes before the current lilystring,
                    # index 1 comes after, so wrap the current lilystring in them
                    lilystring = "".join([item[0] for item in return_values if type(item) == list]) + lilystring
                    lilystring += "".join([item[1] for item in return_values if type(item) == list])
                    if n_id in self.expressions:
                        lilystring += "".join([expr.toLily() for expr in self.expressions[n_id]])



        elif len(self.forwards) > 0:
            for item in self.forwards:
                values.extend(self.forwards[item].toLily())
        if hasattr(self, "barlines") and "right" in self.barlines:
            lilystring += self.barlines["right"].toLily()
        if len(values) > 0:
            return values
        return lilystring

    def addDirection(self, item, note):
        if (type(item) is not Directions.OctaveShift and type(item) is not Directions.Pedal) or item.type == "stop":
            if note not in self.items:
                self.items[note] = []
            self.items[note].append(item)
            if type(item) is Directions.OctaveShift:
                if note+1 not in self.octaveShift:
                    self.octaveShift[note+1] = 0
        else:
            if type(item) is Directions.OctaveShift:
                if note not in self.octaveShift:
                    multiplier = 1
                    if item.type == "up":
                        multiplier = 1
                    if item.type == "down":
                        multiplier = -1
                    octaves = 0
                    if item.amount == 8:
                        octaves = 2
                    if item.amount == 15:
                        octaves = 4
                    self.octaveShift[note] = octaves*multiplier
            if note not in self.preitems:
                self.preitems[note] = []
            self.preitems[note].append(item)

    def addExpression(self, item, note):
        if note not in self.expressions:
            self.expressions[note] = []
        self.expressions[note].append(item)

    def addNote(self, item):
        range = [self.octaveShift[number] for number in self.octaveShift if number <= len(self.notes)]
        if len(range) > 0:
            item.pitch.octave = str(int(item.pitch.octave) - range[-1])
        self.notes.append(item)



class Barline(BaseClass.Base):
    def __init__(self, **kwargs):
        if "style" in kwargs:
            if kwargs["style"] is not None:
                self.style = kwargs["style"]
        if "repeat" in kwargs:
            if kwargs["repeat"] is not None:
                self.repeat = kwargs["repeat"]
        if "ending" in kwargs:
            if kwargs["ending"] is not None:
                self.ending = kwargs["ending"]
        if "repeat-num" in kwargs:
            if kwargs["repeat-num"] is not None:
                self.repeatNum = kwargs["repeat-num"]
            else:
                self.repeatNum = 2
        else:
            self.repeatNum = 2
        BaseClass.Base.__init__(self)

    def toLily(self):
        lilystring = ""
        if not hasattr(self, "ending") and not hasattr(self, "repeat"):
            lilystring += " \\bar \""
            if hasattr(self, "style"):
                options = {"light-light":"||","heavy-light":".|","light-heavy":"|.",
                           "heavy-heavy":"..","dotted":";","dashed":"!"}
                if self.style in options:
                    lilystring += options[self.style] + "\""
            else:
                lilystring += "|\""
        else:



            if hasattr(self, "repeat"):
                if self.repeat == "forward":
                    lilystring = " \\repeat volta "+str(self.repeatNum)+" {"
                if self.repeat == "backward" and not hasattr(self, "ending"):
                    lilystring += "}"
                if self.repeat == "forward-barline":
                    lilystring = " \\bar \".|:\""
                if self.repeat == "backward-barline":
                    lilystring = " \\bar \":|.\""
                if self.repeat == "backward-barline-double":
                    lilystring = " \\bar \":|.|:\""

            if hasattr(self, "ending"):
                lilystring += self.ending.toLily()
        return lilystring

class EndingMark(BaseClass.Base):
    def __init__(self, **kwargs):
        if "number" in kwargs:
            self.number = kwargs["number"]
        if "type" in kwargs:
            self.type = kwargs["type"]
        BaseClass.Base.__init__(self)

    def toLily(self):
        lilystring = ""
        if hasattr(self, "number"):
            if self.number == 1:
                lilystring += "}\n\\alternative {\n"
            lilystring += "{"
        else:
            lilystring = "}\n\\alternative {\n{"
        if hasattr(self, "type"):
            if self.type == "stop":
                lilystring = "}\n"
        return lilystring

class Transposition(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "diatonic" in kwargs:
            self.diatonic = kwargs["diatonic"]
        if "chromatic" in kwargs:
            self.chromatic = kwargs["chromatic"]
        if "octave" in kwargs:
            self.octave = kwargs["octave"]
