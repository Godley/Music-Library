class Meter(object):
    def __init__(self, **kwargs):
        if "beats" in kwargs:
            self.beats = kwargs["beats"]
        if "type" in kwargs:
            self.type = kwargs["type"]

    def __str__(self):
        return str(self.beats) + "/" + str(self.type)

    def toLily(self):
        val = "\\time"
        if hasattr(self, "beats"):
            val += " " + str(self.beats)
            if hasattr(self, "type"):
                val += "/" + str(self.type)
            else:
                if self.beats <= 4:
                    val += "/4"
                elif 4 < self.beats <= 8:
                    val += "/8"
        elif not hasattr(self, "type"):
            val += " 4/4"
        else:
            val += " " + str(self.type) + "/" + str(self.type)

        return val