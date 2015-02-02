from implementation.primaries.Drawing.classes import BaseClass, Note, Directions

class Measure(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "width" in kwargs:
            self.width = float(kwargs["width"])
        self.items = {1:{}}
        self.expressions = {1:{}}
        self.notes = {1:[]}


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

    # TODO: REFACTOR. Dynamics and some other stuff need to come straight after a note so a generic "item" list won't work.
    def toLily(self, staff_id):
        lilystring = ""
        if (staff_id in self.notes and len(self.notes[staff_id]) == 0) or staff_id not in self.notes:
            lilystring += "r"
        if staff_id in self.notes and len(self.notes[staff_id]) > 0:
            for n_id in range(len(self.notes[staff_id])):
                lilystring += " "+self.notes[staff_id][n_id].toLily()
                if staff_id in self.expressions and n_id in self.expressions[staff_id]:
                    lilystring += "".join([expr.toLily() for expr in self.expressions[staff_id][n_id]])
                if staff_id in self.items and n_id in self.items[staff_id]:
                    lilystring+= "".join([dir.toLily() for dir in self.items[staff_id][n_id]])
        elif staff_id in self.items and len(self.items[staff_id]) > 0:
            for n_id in range(len(self.items[staff_id])):
                lilystring += "".join([dir.toLily() for dir in self.items[staff_id][n_id]])
                if staff_id in self.expressions and n_id in self.expressions[staff_id]:
                    lilystring += "".join([expr.toLily() for expr in self.expressions[staff_id][n_id]])
        return lilystring

    def addDirection(self, item, note, staff):
        if staff not in self.items:
            self.items[staff] = {}
        if note not in self.items[staff]:
            self.items[staff][note] = []
        self.items[staff][note].append(item)

    def addExpression(self, item, note, staff):
        if staff not in self.expressions:
            self.expressions[staff] = {}
        if note not in self.expressions[staff]:
            self.expressions[staff][note] = []
        self.expressions[staff][note].append(item)

    def addNote(self, item, staff):
        if staff not in self.notes:
            self.notes[staff] = []
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

class EndingMark(BaseClass.Base):
    def __init__(self, **kwargs):
        if "number" in kwargs:
            self.number = kwargs["number"]
        if "type" in kwargs:
            self.type = kwargs["type"]
        BaseClass.Base.__init__(self)

class Transposition(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "diatonic" in kwargs:
            self.diatonic = kwargs["diatonic"]
        if "chromatic" in kwargs:
            self.chromatic = kwargs["chromatic"]
        if "octave" in kwargs:
            self.octave = kwargs["octave"]
