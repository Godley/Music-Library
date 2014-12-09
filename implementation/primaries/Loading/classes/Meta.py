class Meta(object):
    def __init__(self, **kwargs):
        if "title" in kwargs.keys():
            self.title = kwargs["title"]
        if "composer" in kwargs.keys():
            self.composer = kwargs["composer"]


    def __str__(self):
        st = ""
        if hasattr(self, "title"):
            st += self.title + " by "
        if hasattr(self, "composer"):
            st += self.composer
        return st
