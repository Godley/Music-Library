class Piece(object):
    def __init__(self):
        self.Parts = {}

    def __str__(self):
        st = ""
        if hasattr(self, "meta"):
            st += str(self.meta)
        for key in sorted(self.Parts.keys()):
            st += "\n"
            st += "Part: "
            st += key
            st += "\n Details: "
            st += str(self.Parts[key])
        return st

    def toLily(self):
        lilystring = ""
        partStrings = []
        for part in self.Parts.keys():
            variables, pstring = self.Parts[part].toLily()
            lilystring += "\n".join(variables)
            partStrings.append(pstring)
        if hasattr(self, "meta"):
            lilystring += "\n"+self.meta.toLily()

        lilystring += "<<"
        lilystring += "".join([pstring for pstring in partStrings])
        lilystring += ">>"
        return lilystring

    def addPart(self, id="gubbins", part=None):
        if id not in self.Parts:
            self.Parts[id] = part

    def getPart(self, id="gubbins"):
        if id in self.Parts:
            return self.Parts[id]