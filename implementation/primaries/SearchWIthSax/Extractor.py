import xml.sax
class Extractor(xml.sax.ContentHandler):
    def __init__(self, parent, file):
        self.parent = parent
        self.file = file
        self.tracked = self.parent.tracked
        self.name = ""

    def startElement(self, name, attrs):
        attribs = {}
        for a in attrs.getNames():
            attribs[a] = attrs.get(a)
        self.attrs = attribs
        if name in self.parent.tags:
            self.name = name

    def characters(self, chars):
        if self.name != "":
            self.tracked[chars] = [self.file, self.name, self.attrs]

    def endElement(self, name):
        self.name = ""


