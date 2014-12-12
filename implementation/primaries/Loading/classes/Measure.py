class Measure:
    def __init__(self, **kwargs):
        if "width" in kwargs:
            self.width = int(kwargs["width"])
        self.notes = []
        self.directions = []

    def __str__(self):
        st = ""
        for key, v in vars(self).iteritems():
            st += key + " : "
            if type(v) is list:
                for val in v:
                    st += "\n" + str(val)
            else:
                st += str(v) + "\n"

        return st

    def CheckDivisions(self):
        if hasattr(self, "divisions"):
            for n in self.notes:
                n.divisions = float(self.divisions)

class Transposition(object):
    def __init__(self, **kwargs):
        if "diatonic" in kwargs:
            self.diatonic = kwargs["diatonic"]
        if "chromatic" in kwargs:
            self.chromatic = kwargs["chromatic"]
        if "octave" in kwargs:
            self.octave = kwargs["octave"]

    def __str__(self):
        st = ""
        for key, v in vars(self).iteritems():
            st += key + " : "
            if type(v) is list:
                for val in v:
                    st += "\n" + str(val)
            if type(v) is dict:
                for k, val in v.iteritems():
                    st += "\n" + str(val)
            elif type(v) is not dict and type(v) is not list:
                st += str(v) + "\n"

        return st