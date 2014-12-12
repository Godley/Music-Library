import BaseClass

class Tie(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type


class Stem(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type


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

class Stem(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type