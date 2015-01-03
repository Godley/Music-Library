from implementation.primaries.Drawing.classes import BaseClass

class Tie(BaseClass.Base):
    def __init__(self, type):
        self.type = type

class Notehead(BaseClass.Base):
    def __init__(self, filled=False, type=""):
        self.filled = filled
        self.type = type




class Stem(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type


class Pitch(object):
    def __init__(self, **kwargs):
        if "alter" in kwargs:
            self.alter = kwargs["alter"]
        if "octave" in kwargs:
            self.octave = kwargs["octave"]
        if "step" in kwargs:
            self.step = kwargs["step"]
        if "accidental" in kwargs:
            self.accidental = kwargs["accidental"]
        if "unpitched" in kwargs:
            self.unpitched = True

    def __str__(self):
        st = ""
        alter = {1:"sharp",-1:"flat",0:""}
        if hasattr(self,"unpitched"):
            st += "unpitched"
        if hasattr(self, "step"):
            st += self.step

        if hasattr(self, "alter"):
            st += alter[int(self.alter)]
        if hasattr(self, "accidental"):
            st += "("+self.accidental+")"
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
        if hasattr(self, "divisions") and hasattr(self, "duration"):
            self.duration = self.duration / self.divisions
        st = BaseClass.Base.__str__(self)
        return st

class Tuplet(BaseClass.Base):
    def __init__(self, **kwargs):
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
        if "bracket" in kwargs:
            if kwargs["bracket"] is not None:
                self.bracket = kwargs["bracket"]
        BaseClass.Base.__init__(self)

class GraceNote(BaseClass.Base):
    def __init__(self, **kwargs):
        if "slash" in kwargs:
            self.slash = kwargs["slash"]
        BaseClass.Base.__init__(self)
class TimeModifier(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "normal" in kwargs:
            self.normal = kwargs["normal"]
        if "actual" in kwargs:
            self.actual = kwargs["actual"]

class Arpeggiate(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "direction" in kwargs:
            self.direction = kwargs["direction"]

class Slide(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
        if "lineType" in kwargs:
            if kwargs["lineType"] is not None:
                self.lineType = kwargs["lineType"]
        if "number" in kwargs:
            if kwargs["number"] is not None:
                self.number = kwargs["number"]

class Glissando(Slide):
    def hello(self):
        amethod = "h"


class NonArpeggiate(Arpeggiate):
    def __init__(self, **kwargs):
        Arpeggiate.__init__(self)
        if "type" in kwargs:
            self.type = kwargs["type"]

class Stem(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type

class Beam(Stem):
    def __init__(self, **kwargs):
        if "type" in kwargs:
            Stem.__init__(self,kwargs["type"])