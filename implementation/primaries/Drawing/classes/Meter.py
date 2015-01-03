class Meter(object):
    def __init__(self, **kwargs):
        if "beats" in kwargs:
            self.beats = kwargs["beats"]
        if "type" in kwargs:
            self.type = kwargs["type"]

    def __str__(self):
        return str(self.beats) + "/" + str(self.type)