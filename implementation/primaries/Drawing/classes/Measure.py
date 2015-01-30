from implementation.primaries.Drawing.classes import BaseClass, Note, Directions

class Measure(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "width" in kwargs:
            self.width = float(kwargs["width"])
        self.items = {1:[]}


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

    def toLily(self, measure_id):
        lilystring = ""
        end_list = []
        to_add = []
        previous = None
        for index in range(len(self.items[measure_id])):
            lilystring += " "
            if not isinstance(self.items[measure_id][index], Note.Note) and not isinstance(previous, Note.Note):
                obj = None
                if not isinstance(self.items[measure_id][index], Note.Note):
                    to_add.append(self.items[measure_id][index].toLily())
                    i = index
                    while not isinstance(obj, Note.Note):
                        obj = self.items[measure_id][i]
                        if not isinstance(obj, Note.Note):
                            to_add.append(obj.toLily())
                        i+=1
                        if i >= len(self.items[measure_id]):
                            break
                    lilystring += obj.toLily() + " "
                    lilystring += " ".join(to_add)
                    to_add = []
            else:
                return_val = self.items[measure_id][index].toLily()
                if type(return_val) == list:
                    if len(return_val) > 1:
                        lilystring+= return_val[0]
                        end_list.append(return_val[1])
                    else:
                        lilystring += return_val[0]
                else:
                    lilystring += return_val
            previous = self.items[measure_id][index]
        i = len(end_list)-1
        while i > -1:
            lilystring += end_list[i]
            i-=1
        return lilystring

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
