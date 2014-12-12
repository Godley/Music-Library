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

class Stem(object):
    def __init__(self, type):
        self.type = type

    def __str__(self):
        return self.type