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

    def toLily(self, staff_id):
        lilystring = ""

        #handle stuff attached to measures which aren't directions
        if hasattr(self, "clef") and self.clef is not None:
            lilystring += self.clef.toLily() + " "
        if hasattr(self, "key") and self.key is not None:
            lilystring += self.key.toLily() + " "

        if (staff_id in self.notes and len(self.notes[staff_id]) == 0) or staff_id not in self.notes:
            #if a measure has no notes, it's probably a rest measure.
            lilystring += "r"

        # handle measures containing notes
        if staff_id in self.notes and len(self.notes[staff_id]) > 0:
            for n_id in range(len(self.notes[staff_id])):
                lilystring += " "+self.notes[staff_id][n_id].toLily()

                #attach expressions to notes (these are classed as directions in mxml but in lilypond they have to be
                # attached to notes, e.g dynamics)
                if staff_id in self.expressions and n_id in self.expressions[staff_id]:
                    lilystring += "".join([expr.toLily() for expr in self.expressions[staff_id][n_id]])

                #add on direction strings, text, tempo markings etc
                if staff_id in self.items and n_id in self.items[staff_id]:
                    return_values = [dir.toLily() for dir in self.items[staff_id][n_id]]
                    lilystring += "".join([lilystr for lilystr in return_values if type(lilystr) != list])
                    lilystring = "".join([item[0] for item in return_values if type(item) == list]) + lilystring
                    lilystring += "".join([item[1] for item in return_values if type(item) == list])

        #could still have a measure without notes, so check those again
        elif staff_id in self.items and len(self.items[staff_id]) > 0:
            for n_id in range(len(self.items[staff_id])):
                lilystring += "".join([dir.toLily() for dir in self.items[staff_id][n_id] if dir is not list])
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
