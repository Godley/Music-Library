from implementation.primaries.Loading.classes import BaseClass

class Tie(BaseClass.Base):
    def __init__(self, type):
        self.type = type



class Stem(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type

class Articulation(object):
    def __init__(self, **kwargs):
        if "placement" in kwargs:
            self.placement = kwargs["placement"]
        if "symbol" in kwargs:
            self.symbol = kwargs["symbol"]

    def __str__(self):
        return self.symbol + self.placement

class Accent(Articulation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]
        Articulation.__init__(self, placement=placement, symbol="-")

class StrongAccent(Articulation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = ""
        if "type" in kwargs:
            self.type = kwargs["type"]
            if self.type == "up":
                symbol = "^"
            else:
                symbol = "V"
        Articulation.__init__(self,placement=placement, symbol=symbol)

class Staccato(Articulation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "."
        Articulation.__init__(self,placement=placement,symbol=symbol)

class Staccatissimo(Articulation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "triangle"
        Articulation.__init__(self,placement=placement,symbol=symbol)



class Pitch(object):
    def __init__(self, **kwargs):
        if "alter" in kwargs:
            self.accidental = kwargs["accidental"]
        if "octave" in kwargs:
            self.octave = kwargs["octave"]
        if "step" in kwargs:
            self.step = kwargs["step"]

    def __str__(self):
        st = ""
        alter = {1:"sharp",-1:"flat",0:""}
        if hasattr(self, "step"):
            st += self.step
        if hasattr(self, "accidental"):
            st += alter[int(self.accidental)]
        if hasattr(self, "octave"):
            st += self.octave
        return st


class Note(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        self.ties = []
        if "rest" in kwargs:
            self.rest = True
        else:
            self.rest = False
        if "pitch" in kwargs:
            self.pitch = kwargs["pitch"]
        if "duration" in kwargs:
            self.duration = float(kwargs["duration"])
        if "divisions" in kwargs:
            self.divisions = float(kwargs["division"])
        else:
            self.divisions = 1

    def __str__(self):
        if hasattr(self, "divisions"):
            self.duration = self.duration / self.divisions
        st = BaseClass.Base.__str__(self)
        return st



class Stem(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type