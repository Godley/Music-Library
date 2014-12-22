from implementation.primaries.Loading.classes import BaseClass

class Meta(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "title" in kwargs:
            if kwargs["title"] is not None:
                self.title = kwargs["title"]
        if "composer" in kwargs:
            if kwargs["composer"] is not None:
                self.composer = kwargs["composer"]

