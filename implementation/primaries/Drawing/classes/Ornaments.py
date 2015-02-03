from implementation.primaries.Drawing.classes import BaseClass

# TODO: probably needs refactoring to 1 ornament class?
class InvertedMordent(BaseClass.Base):
    def toLily(self):
        return "\prall"

class Mordent(BaseClass.Base):

    def toLily(self):
        return "\mordent"

class Trill(BaseClass.Base):
    def toLily(self):
        return "\\trill"

class Turn(BaseClass.Base):
    def toLily(self):
        return "\\turn"

class InvertedTurn(BaseClass.Base):
    def toLily(self):
        return "\\reverseturn"

class Tremolo(BaseClass.Base):
    def __init__(self, **kwargs):
        self.preNote = True
        BaseClass.Base.__init__(self)
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]

        if "value" in kwargs:
            if kwargs["value"] is not None:
                self.value = kwargs["value"]
        else:
            self.value = 2

    def toLily(self):
        return_val = "\\repeat tremolo "
        num = ""
        if hasattr(self, "value"):
            num = str(8 * self.value)

        if hasattr(self, "type"):
            multipliers = {"single":16,"double":4,
                            "triple":8,"quadruple":16}
            if self.type in multipliers:
                num = str(multipliers[self.type])
        elif not hasattr(self, "value"):
            num = str(2)

        if num != "":
            return_val += num + " "
        return return_val

