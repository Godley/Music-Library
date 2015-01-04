class Base(object):
    def __init__(self):
        self.indent = 1
    def toLily(self):
        pass
    def __str__(self):
        st = str(type(self))
        values = vars(self)
        for key in values.keys():
            if key == "indent":
                continue
            st += "\n"
            for i in range(self.indent):
                st += "\t"
            if type(values[key]) is not dict and type(values[key]) is not list:
                try:
                    values[key].indent = self.indent + 1
                except:
                    pass
                st += key + " : "
                if type(values[key]) is not None:
                    st += str(values[key])
                else:
                    st += key + ":None"

            if type(values[key]) is list:
                if len(values[key]) > 0:
                    st += key + " : "
                    for item in values[key]:
                        if type(item) is not str and type(item) is not int and type(item) is not float:
                            item.indent = self.indent +1
                        st +=  str(item) + "\n"
            if type(values[key]) is dict:
                if len(values[key]) > 0:
                    st += key + " : "
                    for k in values[key].keys():
                        if type(values[key][k]) is not str and type(values[key][k]) is not int and type(values[key][k]) is not float:
                            values[key][k].indent = self.indent + 1
                        st += key + " : " + str(values[key][k])
        return st
