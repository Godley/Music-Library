__author__ = 'charlotte'
clef_type = {"G2": "treble", "G1": "French violin", "F4": "bass", "F3": "baritone", "F": "sub-bass", "C3": "alto",
             "C4": "tenor", "C5": "Baritone on C", "C2": "mezzo-soprano", "C1": "soprano"}


class Clef(object):
    def __init__(self, **kwargs):
        if "sign" in kwargs:
            self.sign = kwargs["sign"]
        if "line" in kwargs:
            self.line = kwargs["line"]
        if "octave_change" in kwargs:
            self.octave_change = kwargs["octave_change"]

    def __str__(self):
        name = ""
        index = self.sign + str(self.line)
        if index in clef_type:
            name = clef_type[index]
        else:
            name += index
        if hasattr(self, "octave_change"):
            name += "shifted " + str(self.octave_change) + " octave(s)"
        return name
