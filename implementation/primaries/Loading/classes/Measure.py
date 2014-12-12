import BaseClass

class Measure(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "width" in kwargs:
            self.width = int(kwargs["width"])
        self.notes = []
        self.directions = []


    def CheckDivisions(self):
        if hasattr(self, "divisions"):
            for n in self.notes:
                n.divisions = float(self.divisions)

class Transposition(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "diatonic" in kwargs:
            self.diatonic = kwargs["diatonic"]
        if "chromatic" in kwargs:
            self.chromatic = kwargs["chromatic"]
        if "octave" in kwargs:
            self.octave = kwargs["octave"]
