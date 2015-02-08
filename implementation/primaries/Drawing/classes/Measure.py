try:
    from classes import BaseClass, Note, Directions
except:
    from implementation.primaries.Drawing.classes import BaseClass, Note, Directions

class Measure(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "width" in kwargs:
            self.width = float(kwargs["width"])
        self.items = {1:{}}
        self.preitems = {1:{}}
        self.expressions = {1:{}}
        self.notes = {1:[]}
        self.forwards = {}
        self.octaveShift = {}


    def CheckDivisions(self):
        if hasattr(self, "divisions"):
            for n in self.items:
                if n is Note.Note:
                    if self.divisions is not None:
                        n.divisions = float(self.divisions)

    def __str__(self):
        self.CheckDivisions()
        st = BaseClass.Base.__str__(self)
        return st

    def toLily(self, staff_id, start=0,end=-1):
        lilystring = ""
        values = []

        #handle stuff attached to measures which aren't directions
        if hasattr(self, "clef") and self.clef is not None:
            lilystring += self.clef.toLily() + " "
        if hasattr(self, "key") and self.key is not None:
            lilystring += self.key.toLily() + " "

        if ((staff_id in self.notes and len(self.notes[staff_id]) == 0) or staff_id not in self.notes) and len(self.forwards) == 0:
            #if a measure has no notes, it's probably a rest measure.
            lilystring += " r"

        # handle measures containing notes
        if staff_id in self.notes and len(self.notes[staff_id]) > 0:
            if end==-1:
                end = len(self.notes[staff_id])
            duration_total = 0
            fwd_repeat = -1
            for n_id in range(start,end):
                if staff_id in self.forwards and n_id in self.forwards[staff_id]:
                    if n_id == 0:
                        values.extend(self.forwards[staff_id][n_id].toLily())
                        values.append(lilystring)
                    else:
                        value = self.forwards[staff_id][n_id].toLily()
                        fwd_repeat = value[1]
                        lilystring += "\\repeat percent 2 {"
                if staff_id in self.preitems and n_id in self.preitems[staff_id]:
                    lilystring += "".join([preitem.toLily() for preitem in self.preitems[staff_id][n_id]])
                lilystring += " "+self.notes[staff_id][n_id].toLily()

                #attach expressions to notes (these are classed as directions in mxml but in lilypond they have to be
                # attached to notes, e.g dynamics)
                if staff_id in self.expressions and n_id in self.expressions[staff_id]:
                    lilystring += "".join([expr.toLily() for expr in self.expressions[staff_id][n_id]])

                #add on direction strings, text, tempo markings etc
                if staff_id in self.items and n_id in self.items[staff_id]:
                    # pull out all the toLily return values
                    return_values = [dir.toLily() for dir in self.items[staff_id][n_id]]

                    # add the strings that aren't lists
                    lilystring += "".join([lilystr for lilystr in return_values if type(lilystr) != list])

                    # any that are lists are intended to be index 0 comes before the current lilystring,
                    # index 1 comes after, so wrap the current lilystring in them
                    lilystring = "".join([item[0] for item in return_values if type(item) == list]) + lilystring
                    lilystring += "".join([item[1] for item in return_values if type(item) == list])

                if fwd_repeat != -1:
                    if hasattr(self.notes[staff_id][n_id], "duration"):
                        duration_total += self.notes[staff_id][n_id].duration
                    if duration_total >= fwd_repeat:
                        lilystring += "}"
                        fwd_repeat = -1

        #could still have a measure without notes, so check those again
        elif staff_id in self.items and len(self.items[staff_id]) > 0:
            if end == -1:
                end = len(self.items[staff_id])
            for n_id in range(start, end):
                if staff_id in self.forwards and n_id in self.forwards[staff_id]:
                    if n_id == 0:
                        values.extend(self.forwards[staff_id][n_id].toLily())
                        values.append(lilystring)
                # pull out all the toLily return values
                return_values = [dir.toLily() for dir in self.items[staff_id][n_id]]

                # add the strings that aren't lists
                lilystring += "".join([lilystr for lilystr in return_values if type(lilystr) != list])

                # any that are lists are intended to be index 0 comes before the current lilystring,
                # index 1 comes after, so wrap the current lilystring in them
                lilystring = "".join([item[0] for item in return_values if type(item) == list]) + lilystring
                lilystring += "".join([item[1] for item in return_values if type(item) == list])
                if staff_id in self.expressions and n_id in self.expressions[staff_id]:
                    lilystring += "".join([expr.toLily() for expr in self.expressions[staff_id][n_id]])



        elif staff_id in self.forwards:
            for item in self.forwards[staff_id]:
                values.extend(self.forwards[staff_id][item].toLily())

        if len(values) > 0:
            return values
        return lilystring

    def addDirection(self, item, note, staff):
        if (type(item) is not Directions.OctaveShift and type(item) is not Directions.Pedal) or item.type == "stop":
            if staff not in self.items:
                self.items[staff] = {}
            if note not in self.items[staff]:
                self.items[staff][note] = []
            self.items[staff][note].append(item)
            if type(item) is Directions.OctaveShift:
                if note not in self.octaveShift[staff]:
                    self.octaveShift[staff][note+1] = 0
        else:
            if type(item) is Directions.OctaveShift:
                if staff not in self.octaveShift:
                    self.octaveShift[staff] = {}
                if note not in self.octaveShift[staff]:
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
                    self.octaveShift[staff][note] = octaves*multiplier
            if staff not in self.preitems:
                self.preitems[staff] = {}
            if note not in self.preitems[staff]:
                self.preitems[staff][note] = []
            self.preitems[staff][note].append(item)

    def addExpression(self, item, note, staff):
        if staff not in self.expressions:
            self.expressions[staff] = {}
        if note not in self.expressions[staff]:
            self.expressions[staff][note] = []
        self.expressions[staff][note].append(item)

    def addNote(self, item, staff):
        if staff not in self.notes:
            self.notes[staff] = []
        if staff in self.octaveShift:
            range = [self.octaveShift[staff][number] for number in self.octaveShift[staff] if number <= len(self.notes[staff])]
            print(range)
            if len(range) > 0:
                item.pitch.octave = str(int(item.pitch.octave) - range[-1])
        self.notes[staff].append(item)



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

            if hasattr(self, "ending"):
                if not hasattr(self.ending, "number") or (hasattr(self.ending, "number") and self.ending.number == 1):
                    lilystring = "\\alternative {"
                if not hasattr(self.ending, "type") or (hasattr(self.ending, "type") and self.ending.type != "stop"):
                    lilystring += "{ "
                elif hasattr(self.ending, "type") and self.type == "stop":
                    lilystring = " }"

            if hasattr(self, "repeat"):
                if self.repeat == "forward":
                    lilystring = "\\repeat volta 2 { "
                if self.repeat == "backward":
                    lilystring = " }"

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
                lilystring += "\\alternative {"
            lilystring += "{"
        else:
            lilystring = "\\alternative {{"
        if hasattr(self, "type"):
            if self.type == "stop":
                lilystring = "}"
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
