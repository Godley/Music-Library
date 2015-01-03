class Notation(object):
    def __init__(self, **kwargs):
        if "placement" in kwargs:
            self.placement = kwargs["placement"]
        if "symbol" in kwargs:
            self.symbol = kwargs["symbol"]

    def __str__(self):
        return self.symbol + self.placement

class Accent(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]
        Notation.__init__(self, placement=placement, symbol="-")

class StrongAccent(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = ""
        if "type" in kwargs:
            self.type = kwargs["type"]
            if self.type == "up":
                symbol = "^"
            else:
                symbol = "V"
        Notation.__init__(self,placement=placement, symbol=symbol)

class Staccato(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "."
        Notation.__init__(self,placement=placement,symbol=symbol)

class Staccatissimo(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "triangle"
        Notation.__init__(self,placement=placement,symbol=symbol)

class Tenuto(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "line"
        Notation.__init__(self,placement=placement,symbol=symbol)

class DetachedLegato(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "lineDot"
        Notation.__init__(self,placement=placement,symbol=symbol)

class Fermata(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        if "type" in kwargs:
            self.type = kwargs["type"]

        symbol = "fermata"
        if "symbol" in kwargs:
            symbol = kwargs["symbol"]

        Notation.__init__(self,placement=placement,symbol=symbol)

class BreathMark(Notation):
    pass

class Caesura(BreathMark):
    pass

class Technique(Notation):
    def __init__(self, **kwargs):
        placement = None
        size = None
        font = None
        symbol = None
        if "type" in kwargs:
            self.type = kwargs["type"]
            symbol = self.type
        if "symbol" in kwargs:
            symbol = kwargs["symbol"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        Notation.__init__(self,placement=placement,
                            symbol=symbol)