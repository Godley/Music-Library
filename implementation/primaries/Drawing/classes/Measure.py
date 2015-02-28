try:
    from classes import BaseClass, Note, Directions
except:
    from implementation.primaries.Drawing.classes import BaseClass, Note, Directions

class Measure(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "width" in kwargs:
            self.width = float(kwargs["width"])
        self.items = []


    def GetBarline(self, side):
        if hasattr(self, "barlines"):
            if side in self.barlines:
                return self.barlines[side]

    def AddBarline(self, item, location="left"):
        if not hasattr(self, "barlines"):
            self.barlines = {}
        self.barlines[location] = item

    def SetDivisions(self, divisions):
        if divisions is not None:
            if not hasattr(self, "divisions") or self.divisions is None:
                self.divisions = divisions

    def FindIndex(self, duration=8):
        # simple method which finds the position before a note of x duration.
        note_index = len(self.notes)-1
        total = 0
        while note_index > -1 and total < (duration/self.divisions):
            total += self.notes[note_index].duration
            note_index -= 1
            if total >= duration/self.divisions:
                break
        return note_index

    def CheckDivisions(self):
        if hasattr(self, "divisions"):
            for n in self.notes:
                if self.divisions is not None:
                    n.CheckDivisions(self.divisions)


    def __str__(self):
        self.CheckDivisions()
        ret_str = BaseClass.Base.__str__(self)
        return ret_str

    def addWrapper(self, item):
        # method to add any notation that needs to wrap the whole bar
        self.items.append(item)

    def CalculateTransposition(self):
        scale = ['a','bes','b','c','cis','d','dis','e','f','fis','g','gis']
        base = 3
        result = base
        if hasattr(self.transpose, "chromatic"):
            chromatic = int(self.transpose.chromatic)
            result = base + chromatic

        elif hasattr(self.transpose, "diatonic"):
            diatonic = int(self.transpose.diatonic)
            result = base + (diatonic*2)
        if result < 0:
                result = (len(scale)-1)-result
        if result >= len(scale):
            result = result-(len(scale)-1)
        lettername = scale[result]
        octave_shifters = "'"
        if hasattr(self.transpose, "octave"):
            octave = self.transpose.octave

            if octave > 0:
                octave_shifters += "".join(["'" for i in range(octave)])
            if octave < 0:
                octave_shifters += "".join(["," for i in range(abs(octave))])
        return "\\transpose "+lettername+octave_shifters+" c' {"
        pass

    def HandleAttributes(self):
        lilystring = ""
        if hasattr(self, "transpose"):
            lilystring += self.CalculateTransposition()
        if hasattr(self, "clef") and self.clef is not None:
            lilystring += self.clef.toLily() + " "
        if hasattr(self, "key") and self.key is not None:
            lilystring += self.key.toLily() + " "
        if hasattr(self, "meter"):
            lilystring += self.meter.toLily() + " "
        if hasattr(self, "barlines"):
            if "left" in self.barlines:
                lilystring += self.GetBarline("left").toLily()

        lilystring += "".join([item.toLily()[0] for item in self.items])
        return lilystring

    def HandleClosingAttributes(self):
        lstring = ""
        lstring += "".join([item.toLily()[0] for item in self.items])
        if self.GetBarline("right") is not None:
            bline = self.GetBarline("right").toLily()
            lstring += bline
        else:
            lstring += " | "
        if hasattr(self, "transpose") and hasattr(self.transpose, "type") and self.transpose.type == "stop":
            lstring += " }"

        return lstring

    def toLily(self):
        start = self.HandleAttributes()
        end = self.HandleClosingAttributes()
        return [start, end]

    def getWrapper(self, index):
        if index < len(self.items):
            return self.items[index]

    def GetTotalValue(self):
        """Gets the total value of the bar according to it's time signature"""
        value = ""
        if hasattr(self, "meter"):
            top_value = self.meter.beats
            bottom = self.meter.type
            fraction = top_value/bottom
            if fraction == 1:
                value = "1"
            else:
                if fraction > 1:
                    value = "1."
                if fraction < 1:
                    if fraction >= 0.5:
                        fraction -= 0.5
                        value = "2"
                        if fraction == 0.25:
                            value += "."
        return value


class Barline(BaseClass.Base):
    def __init__(self, **kwargs):
        if "style" in kwargs:
            if kwargs["style"] is not None:
                self.style = kwargs["style"]
        if "repeat" in kwargs:
            if kwargs["repeat"] is not None:
                self.repeat = kwargs["repeat"]
        if "ending" in kwargs:
            if kwargs["ending"] is not None:
                self.ending = kwargs["ending"]
        if "repeat-num" in kwargs:
            if kwargs["repeat-num"] is not None:
                self.repeatNum = kwargs["repeat-num"]
            else:
                self.repeatNum = 2
        else:
            self.repeatNum = 2
        BaseClass.Base.__init__(self)

    def toLily(self):
        lilystring = ""
        if not hasattr(self, "ending") and not hasattr(self, "repeat"):
            lilystring += " \\bar \""
            if hasattr(self, "style"):
                options = {"light-light":"||","heavy-light":".|","light-heavy":"|.",
                           "heavy-heavy":"..","dotted":";","dashed":"!","none":"","tick":"'"}
                if self.style in options:
                    lilystring += options[self.style]
                else:
                    lilystring += "|"
                lilystring+= "\""
            else:
                lilystring += "\""
        else:



            if hasattr(self, "repeat"):
                if self.repeat == "forward":
                    lilystring = " \\repeat volta "+str(self.repeatNum)+" {"
                if self.repeat == "backward" and not hasattr(self, "ending"):
                    lilystring += "}"
                if self.repeat == "forward-barline":
                    lilystring = " \\bar \".|:\""
                if self.repeat == "backward-barline":
                    lilystring = " \\bar \":|.\""
                if self.repeat == "backward-barline-double":
                    lilystring = " \\bar \":|.|:\""

            if hasattr(self, "ending"):
                lilystring += self.ending.toLily()
        return lilystring

class EndingMark(BaseClass.Base):
    def __init__(self, **kwargs):
        if "number" in kwargs:
            self.number = kwargs["number"]
        if "type" in kwargs:
            self.type = kwargs["type"]
        BaseClass.Base.__init__(self)

    def toLily(self):
        lilystring = ""
        if hasattr(self, "number"):
            if self.number == 1:
                lilystring += "}\n\\alternative {\n"
            lilystring += "{"
        else:
            lilystring = "}\n\\alternative {\n{"
        if hasattr(self, "type"):
            if self.type == "stop":
                lilystring = "}\n"
        return lilystring

class Transposition(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "diatonic" in kwargs:
            self.diatonic = kwargs["diatonic"]
        if "chromatic" in kwargs:
            self.chromatic = kwargs["chromatic"]
        if "octave" in kwargs:
            self.octave = kwargs["octave"]
