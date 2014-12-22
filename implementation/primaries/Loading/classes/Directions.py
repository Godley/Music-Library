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

class Lyric(Text):
    def __init__(self, **kwargs):
        font = None
        text = None
        size = None
        if "font" in kwargs:
            font = kwargs["font"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "syllabic" in kwargs:
            self.syllabic = kwargs["syllabic"]
        Text.__init__(self, text=text, font=font, size=size)



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

class RepeatSign(Direction):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        placement = None
        if "type" in kwargs:
            self.type = kwargs["type"]
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        Direction.__init__(self, placement=placement, text=text,size=size,font=font)

class OctaveShift(Direction):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
        Direction.__init__(self, text=text, size=size, font=font, placement=placement)

class Metronome(Direction):
    def __init__(self, **kwargs):
        size = None
        font = None
        text = None
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
        placement = None
        size = None
        font = None
        if "mark" in kwargs:
            self.mark = kwargs["mark"]
        if "text" in kwargs:
            text = kwargs["text"]
        else:
            text = self.mark

        if "size" in kwargs:
            size = kwargs["size"]

        if "font" in kwargs:
            font = kwargs["font"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        Direction.__init__(self,placement=placement,
                           font=font,
                           size=size,
                           text=text)

class Wedge(Dynamic):
    def __init__(self, **kwargs):
        placement = None
        self.type = None
        if "placement" in kwargs:
            placement = kwargs["placement"]
        if "type" in kwargs:
            self.type = kwargs["type"]

        Dynamic.__init__(self,placement=placement,text=self.type)



class Slur(Direction):
    def __init__(self, **kwargs):
        placement = None
        size = None
        font = None
        if "size" in kwargs:
            size = kwargs["size"]

        if "font" in kwargs:
            font = kwargs["font"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        Direction.__init__(self,placement=placement,
                           font=font,
                           size=size)

class Technique(Direction):
    def __init__(self, **kwargs):
        placement = None
        size = None
        font = None
        text = None
        if "type" in kwargs:
            self.type = kwargs["type"]
            text = self.type
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]

        if "font" in kwargs:
            font = kwargs["font"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        Direction.__init__(self,placement=placement,
                           font=font,
                           size=size,
                           text=text)