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
        acc = ""
        if hasattr(self, "accidental"):
            if int(self.accidental) == 1:
                acc = "sharp"
            elif int(self.accidental) == -1:
                acc = "flat"

        if hasattr(self, "step"):
            st += str(self.step)

        st += acc
        if hasattr(self, "octave"):
            st += str(self.octave)
        return st


class Note(object):
    def __init__(self, **kwargs):
        self.ties = []
        if "rest" in kwargs:
            self.rest = True
        else:
            self.rest = False
        if "pitch" in kwargs:
            self.pitch = kwargs["pitch"]
        if "duration" in kwargs:
            self.duration = float(kwargs["duration"])
        if "accidental" in kwargs:
            self.accidental = kwargs["accidental"]
        if "divisions" in kwargs:
            self.divisions = float(kwargs["division"])
        else:
            self.divisions = 1

    def __str__(self):
        st = ""
        if hasattr(self, "chord"):
            st += "chord with previous note: \t"
        if self.rest:
            st += "rest "
        if hasattr(self, "pitch"):
            st += "note of pitch " + str(self.pitch)

        if hasattr(self, "duration"):
            length = float(self.duration / self.divisions)
            st += " and duration %.2f " % length
            if hasattr(self, "dotted"):
                st += "(dotted)"
        if len(self.ties) > 0:
            st += "\n ties: "
        for t in self.ties:
            st += str(t)
        if hasattr(self, "stem"):
            st += "\nstem direction "+str(self.stem)
        return st

class Stem(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type