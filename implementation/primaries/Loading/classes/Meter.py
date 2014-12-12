class Meter(object):
    def __init__(self, beats, type):
        self.beats = beats
        self.type = type

    def __str__(self):
        return str(self.beats) + "/" + str(self.type)