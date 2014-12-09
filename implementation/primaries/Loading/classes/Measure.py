class Measure:
    def __init__(self, **kwargs):
        if "width" in kwargs:
            self.width = int(kwargs["width"])
        self.notes = []

    def __str__(self):
        st = ""
        if hasattr(self, "width"):
            st += "Width: " + str(self.width) + "\n"
        if hasattr(self, "meter"):
            st += "Time Signature:\n\r" + str(self.meter)
        if hasattr(self, "key"):
            st += "\n\rkey: "
            st += str(self.key)
        if hasattr(self, "clef"):
            st += "\n\rclef: "
            st += str(self.clef)
        if hasattr(self, "divisions"):
            st += "\n\rdivisions: " + str(self.divisions)
        st += "\nnote sequence: \n"
        for note in self.notes:
            st += "\t" + str(note) + "\n"
        if hasattr(self, "transpose"):
            st += "\ntransposed by:\n"+str(self.transpose)
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
        if hasattr(self, "diatonic"):
            st += "diatonic: "+self.diatonic
        if hasattr(self, "chromatic"):
            st += "\nchromatic: "+self.chromatic
        if hasattr(self,"octave"):
            st += "\noctaves: "+self.octave
        return st