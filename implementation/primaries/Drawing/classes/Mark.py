class Notation(object):
    def __init__(self, **kwargs):
        if "placement" in kwargs:
            self.placement = kwargs["placement"]
        if "symbol" in kwargs:
            self.symbol = kwargs["symbol"]

    def __str__(self):
        return self.symbol + self.placement

    def toLily(self):
        return "\\"

class Accent(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]
        Notation.__init__(self, placement=placement, symbol="-")

    def toLily(self):
        val = Notation.toLily(self)
        val += "accent "
        return val
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
    def toLily(self):
        val = Notation.toLily(self)
        val += "marcato "
        return val

class Staccato(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "."
        Notation.__init__(self,placement=placement,symbol=symbol)

    def toLily(self):
        val = Notation.toLily(self)
        val += "staccato "
        return val
class Staccatissimo(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "triangle"
        Notation.__init__(self,placement=placement,symbol=symbol)

    def toLily(self):
        val = Notation.toLily(self)
        val += "staccatissimo "
        return val

class Tenuto(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "line"
        Notation.__init__(self,placement=placement,symbol=symbol)

    def toLily(self):
        val = Notation.toLily(self)
        val += "tenuto "
        return val

class DetachedLegato(Notation):
    def __init__(self, **kwargs):
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        symbol = "lineDot"
        Notation.__init__(self,placement=placement,symbol=symbol)

    def toLily(self):
        val = Notation.toLily(self)
        val+= "portato "
        return val

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

    def toLily(self):
        val = Notation.toLily(self)
        if hasattr(self, "symbol"):
            if self.symbol != "fermata":
                if self.symbol == "angled":
                    val += "short"
                if self.symbol == "square":
                    val += "long"
                if self.symbol == "squared":
                    val += "verylong"
        val += "fermata "
        return val
class BreathMark(Notation):
    def toLily(self):
        val = Notation.toLily(self)
        val += "breathe "
        return val

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

    def toLily(self):
        val = Notation.toLily(self)
        if hasattr(self, "type"):
            splitter = self.type.split("-")
            joined = "".join(splitter)
            val += joined+ " "
        return val