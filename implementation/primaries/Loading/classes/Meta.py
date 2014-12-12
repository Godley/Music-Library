class Meta(object):
    def __init__(self, **kwargs):
        if "title" in kwargs.keys():
            self.title = kwargs["title"]
        if "composer" in kwargs.keys():
            self.composer = kwargs["composer"]


    def __str__(self):
        st = ""
        for key, v in vars(self).iteritems():
            st += key + " : "
            if type(v) is list:
                for val in v:
                    st += "\n" + str(val)
            if type(v) is dict:
                for k, val in v.iteritems():
                    st += "\n" + str(val)
            elif type(v) is not dict and type(v) is not list:
                st += str(v) + "\n"

        return st
