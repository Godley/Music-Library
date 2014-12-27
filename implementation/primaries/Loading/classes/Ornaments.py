from implementation.primaries.Loading.classes import BaseClass

# TODO: probably needs refactoring to 1 ornament class?
class InvertedMordent(BaseClass.Base):
    def __init__(self):
        BaseClass.Base.__init__(self)

class Mordent(BaseClass.Base):
    def __init__(self):
        BaseClass.Base.__init__(self)

class Trill(BaseClass.Base):
    def __init__(self):
        BaseClass.Base.__init__(self)

class Turn(BaseClass.Base):
    def __init__(self):
        BaseClass.Base.__init__(self)

class InvertedTurn(BaseClass.Base):
    def __init__(self):
        BaseClass.Base.__init__(self)

class Tremolo(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]

        if "value" in kwargs:
            if kwargs["value"] is not None:
                self.value = kwargs["value"]

