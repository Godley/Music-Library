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