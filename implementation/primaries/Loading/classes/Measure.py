from implementation.primaries.Loading.classes import BaseClass, Note

class Measure(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "width" in kwargs:
            self.width = float(kwargs["width"])
        self.items = []


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

class Barline(BaseClass.Base):
    def __init__(self, **kwargs):
        if "style" in kwargs:
            if kwargs["style"] is not None:
                self.style = kwargs["style"]
        BaseClass.Base.__init__(self)

class BarMark(Barline):
    def __init__(self, **kwargs):
        style = None
        if "number" in kwargs:
            self.number = kwargs["number"]
        if "type" in kwargs:
            self.type = kwargs["type"]
        if "style" in kwargs:
            style = kwargs["style"]
        Barline.__init__(self, style=style)

class Transposition(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "diatonic" in kwargs:
            self.diatonic = kwargs["diatonic"]
        if "chromatic" in kwargs:
            self.chromatic = kwargs["chromatic"]
        if "octave" in kwargs:
            self.octave = kwargs["octave"]
