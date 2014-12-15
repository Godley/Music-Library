__author__ = 'charlotte'
clef_type = {"G2": "treble", "G1": "French violin", "F4": "bass", "F3": "baritone", "F": "sub-bass", "C3": "alto",
             "C4": "tenor", "C5": "Baritone on C", "C2": "mezzo-soprano", "C1": "soprano"}


class Clef(object):
    def __init__(self, **kwargs):
        if "sign" in kwargs:
            self.sign = kwargs["sign"]
        if "line" in kwargs:
            self.line = kwargs["line"]

    def __str__(self):
        if hasattr(self, "sign"):
            if hasattr(self, "line"):
                if (self.sign + self.line) in clef_type:
                    return clef_type[(self.sign + self.line)]
                else:
                    return (self.sign + self.line)
            else:
                return(self.sign)
        return ""
