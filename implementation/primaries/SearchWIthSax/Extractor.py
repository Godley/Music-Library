import xml.sax
class Extractor(xml.sax.ContentHandler):
    def __init__(self, parent, file, byTag=False):
        self.parent = parent
        self.file = file
        self.tracked = self.parent.tracked
        self.name = ""
        self.byTag = byTag

    def startElement(self, name, attrs):
        if name in self.parent.tags:
            attribs = {}
            for a in attrs.getNames():
                attribs[a] = attrs.get(a)
            self.attrs = attribs
            self.name = name

    def characters(self, chars):
        if self.name != "":
            if not self.byTag:
                if chars not in self.tracked.keys():
                    self.tracked[chars] = []
                self.tracked[chars].append([self.file, self.name, self.attrs])
            else:
                if self.name not in self.tracked.keys():
                    self.tracked[self.name] = []
                self.tracked[self.name].append([self.file, chars, self.attrs])


    def endElement(self, name):
        if name == self.name:
            self.name = ""


