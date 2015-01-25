class Part(object):
    def __init__(self):
        self.measures = {}

    def __str__(self):
        self.CheckDivisions()
        st = ""
        if hasattr(self, "name"):
            st += "name:"+self.name
        for key in self.measures.keys():
            st += "\n"
            st += "Measure: "
            st += str(key)
            st += "\n\r Details: \r"
            st += str(self.measures[key])
            st += "\n--------------------------------------------------------"
        return st

    def CheckDivisions(self):
        divisions = None
        for key in self.measures.keys():
            if hasattr(self.measures[key], "divisions"):
                divisions = self.measures[key].divisions
            else:
                self.measures[key].divisions = divisions
                self.measures[key].CheckDivisions()

    def toLily(self):
        lilystring = "<<"
        if len(self.measures.keys()) > 0:
            staff_nums = self.measures[list(self.measures.keys())[0]].items.keys()
            for id in staff_nums:

                lilystring += "\\new Staff"
                if hasattr(self, "name"):
                    lilystring += " \with { \ninstrumentName = #\""+ self.name +" \"\n}"
                lilystring += "{"
                for key in self.measures.keys():
                    if id in self.measures[key].items:
                        lilystring += self.measures[key].toLily(id)
                lilystring += "}"
        lilystring += ">>"
        return lilystring