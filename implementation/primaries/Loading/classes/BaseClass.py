class Base(object):
    def __init__(self):
        self.indent = 1
    def __str__(self):
        st = ""
        delim = "********************"
        for key, v in vars(self).iteritems():
            if type(v) is object:
                v.indent = self.indent + 1
            st += "\n"
            for i in range(self.indent):
                st += "\t"
            if type(v) is not dict and type(v) is not list:
                st += key + " : " + str(v)

            if type(v) is list:
                if len(v) > 0:
                    st += key + " : "
                    for item in v:
                        if type(item) is object:
                            item.indent = self.indent +1
                        st += str(item)
            if type(v) is dict:
                if len(v) > 0:
                    st += key + " : "
                    for key, item in v.iteritems():
                        st += key + " : " + str(item)
        return st
