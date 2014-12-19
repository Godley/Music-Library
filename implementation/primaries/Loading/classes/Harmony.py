from implementation.primaries.Loading.classes import Note, BaseClass

class Harmony(BaseClass.Base):
    def __init__(self, **kwargs):
        self.degrees = []
        if "root" in kwargs:
            if kwargs["root"] is not None:
                self.root = kwargs["root"]
        if "kind" in kwargs:
            if kwargs["kind"] is not None:
                self.kind = kwargs["kind"]
        if "bass" in kwargs:
            if kwargs["bass"] is not None:
                self.bass = kwargs["bass"]
        if "degrees" in kwargs:
            self.degrees = kwargs["degrees"]
        BaseClass.Base.__init__(self)

class Kind(BaseClass.Base):
    def __init__(self, **kwargs):
        if "value" in kwargs:
            if kwargs["value"] is not None:
                self.value = kwargs["value"]
        if "halign" in kwargs:
            if kwargs["halign"] is not None:
                self.halign = kwargs["halign"]
        if "text" in kwargs:
            if kwargs["text"] is not None:
                self.text = kwargs["text"]
        if "parenthesis" in kwargs:
            if kwargs["parenthesis"] is not None:
                self.parenthesis = kwargs["parenthesis"]
        BaseClass.Base.__init__(self)

class Degree(BaseClass.Base):
    def __init__(self, **kwargs):
        if "alter" in kwargs and kwargs["alter"] is not None:
            self.alter = kwargs["alter"]
        if "value" in kwargs and kwargs["alter"] is not None:
            self.value = kwargs["value"]
        if "type" in kwargs and kwargs["type"] is not None:
            self.type = kwargs["type"]

class harmonyPitch(Note.Pitch):
    def __str__(self):
        return "hello, world"