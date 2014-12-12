class Part(object):
    def __init__(self):
        self.measures = {}

    def __str__(self):
        self.CheckDivisions()
        st = ""
        if hasattr(self, "name"):
            st += "name:"+self.name
        for key, m in self.measures.iteritems():
            st += "\n"
            st += "Measure: "
            st += str(key)
            st += "\n\r Details: \r"
            st += str(m)
            st += "\n--------------------------------------------------------"
        return st

    def CheckDivisions(self):
        divisions = None
        for key, m in self.measures.iteritems():
            if hasattr(m, "divisions"):
                divisions = m.divisions
            else:
                m.divisions = divisions
                m.CheckDivisions()