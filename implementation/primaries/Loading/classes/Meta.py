import BaseClass

class Meta(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "title" in kwargs.keys():
            self.title = kwargs["title"]
        if "composer" in kwargs.keys():
            self.composer = kwargs["composer"]

