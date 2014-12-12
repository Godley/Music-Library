class Base(object):
    def __init__(self):
        self.indent = 1
    def __str__(self):
        st = ""
        for key, v in vars(self).iteritems():
            if key == "indent":
                continue
            st += "\n"
            for i in range(self.indent):
                st += "\t"
            if type(v) is not dict and type(v) is not list:
                try:
                    v.indent = self.indent + 1
                except:
                    pass
                st += key + " : " + str(v)

            if type(v) is list:
                if len(v) > 0:
                    st += key + " : "
                    for item in v:
                        if type(item) is not str and type(item) is not int and type(item) is not float:
                            item.indent = self.indent +1
                        st +=  str(item) + "\n"
            if type(v) is dict:
                if len(v) > 0:
                    st += key + " : "
                    for key, item in v.iteritems():
                        if type(item) is not str and type(item) is not int and type(item) is not float:
                            item.indent = self.indent + 1
                        st += key + " : " + str(item)
        return st
