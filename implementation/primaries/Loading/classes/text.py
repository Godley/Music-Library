from implementation.primaries.Loading.classes import BaseClass

class Text(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "font" in kwargs and kwargs["font"] is not None:
            self.font = kwargs["font"]
        if "size" in kwargs and kwargs["size"] is not None:
            self.size = kwargs["size"]
        if "text" in kwargs and kwargs["text"] is not None:
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



class Direction(Text):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                self.placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        Text.__init__(self,text=text,size=size,font=font)



class Metronome(Direction):
    def __init__(self, **kwargs):
        if "beat" in kwargs:
            self.beat = kwargs["beat"]
        if "min" in kwargs:
            self.min = kwargs["min"]
        if hasattr(self, "min"):
            if hasattr(self, "beat"):
                text = self.beat + " = " + self.min
            else:
                text = self.min
        if "size" in kwargs:
            size = kwargs["text"]
        if "font" in kwargs:
            font = kwargs["font"]
        Text.__init__(self,text=text,size=size,font=font)
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
