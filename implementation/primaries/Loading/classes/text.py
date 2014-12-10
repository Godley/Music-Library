class Text(object):
    def __init__(self, **kwargs):
        if "font" in kwargs:
            self.font = kwargs["font"]
        if "size" in kwargs:
            self.size = kwargs["size"]
        if "text" in kwargs:
            self.text = kwargs["text"]
        else:
            self.text = ""

    def get(self):
        ret_list = []
        if hasattr(self, "font"):
            ret_list.append(self.font)
        if hasattr(self, "size"):
            ret_list.append(self.size)
        if hasattr(self, "text"):
            ret_list.append(self.text)
        return ret_list

    def __str__(self):
        st = ""
        if hasattr(self, "text"):
            st += self.text.encode('utf-8')
        if hasattr(self, "size"):
            st += " of size " + str(self.size)
        if hasattr(self, "font"):
            st += " and font " + self.font.encode('utf-8')
        return st



class Direction(Text):
    def __init__(self, **kwargs):
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                self.placement = kwargs["placement"]
        if "size" in kwargs:
            if "font" in kwargs:
                Text.__init__(self,font=kwargs["font"],size=kwargs["size"],text=kwargs["text"])
            else:
                Text.__init__(self,size=kwargs["size"],text=kwargs["text"])
        else:
            Text.__init__(self)


    def __str__(self):
        st = Text.__str__(self)
        if hasattr(self, "placement"):
            st += (" placement: "+self.placement).encode('utf-8')
        return st

class Metronome(Direction):
    def __init__(self, **kwargs):
        if "beat" in kwargs:
            self.beat = kwargs["beat"]
        if "min" in kwargs:
            self.min = kwargs["min"]
        if hasattr(self, "min"):
            if hasattr(self, "beat"):
                self.text = self.beat + " = " + self.min
            else:
                self.text = self.min
        if "font" in kwargs:
            if "size" in kwargs:
                Direction.__init__(self, font=kwargs["font"], size=kwargs["size"], placement=kwargs["placement"])
            else:
                Direction.__init__(self, font=kwargs["font"], placement=kwargs["placement"])
        else:
            Direction.__init__(self)
        if "parentheses" in kwargs:
            if kwargs["parentheses"] == "yes":
                self.parentheses = True
        else:
            self.parentheses = False

    def get_detail(self):
        ret_list = self.get()
        if hasattr(self, "beat"):
            ret_list.append(self.beat)
        if hasattr(self, "per-min"):
            ret_list.append(self.min)
        return ret_list

    def __str__(self):
        st = Text.__str__(self)
        if self.parentheses:
            st = ("(" + st + ")").encode('utf-8')
        return st

class Dynamic(Direction):
    def __init__(self, **kwargs):
        if "mark" in kwargs:
            self.mark = kwargs["mark"]
        if "volume" in kwargs:
            self.volume = kwargs["volume"]
        if "size" in kwargs:
            if "font" in kwargs:
                Direction.__init__(self,placement=kwargs["placement"],font=kwargs["font"],size=kwargs["size"],text=kwargs["mark"])
            else:
                Text.__init__(self,size=kwargs["size"],text=kwargs["mark"])
        else:
            Text.__init__(self,text=kwargs["mark"])

    def __str__(self):
        st = Text.__str__(self)
        if hasattr(self, "volume"):
            st += "\nvolume: " + self.volume
        return st