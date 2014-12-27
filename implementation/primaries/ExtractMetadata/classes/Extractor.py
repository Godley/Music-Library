from xml.sax import ContentHandler
from implementation.primaries.Loading.classes import Key, Clef

class Extractor(ContentHandler):
    def __init__(self, parent, byTag = False):
        self.parent = parent
        self.byTag = byTag
        self.name = ""
        self.attrib = {}

    def startElement(self, name, attrs):
        if name in self.parent.tags:
            self.name = name
            for attrname in attrs.getNames():
                self.attrib[attrname] = attrs.get(attrname)

    def characters(self, chars):
        entry = chars
        tag = self.name
        if tag != "":
            if self.name == "key":
                self.key = Key.Key()
                return
            if self.name == "fifths":
                self.key.fifths = int(chars)
                return
            if self.name == "mode":
                self.key.mode = chars
                tag = "key"

            if hasattr(self, "key"):
                if hasattr(self.key, "fifths"):
                    if hasattr(self.key, "mode"):
                        entry = str(self.key)
                        self.key = None
            if self.name == "clef":
                self.clef = Clef.Clef()
                return
            if self.name == "sign":
                self.clef.sign = chars
                return
            if self.name == "line":
                self.clef.line = int(chars)
                tag = "clef"
            if self.name == "clef-octave-change":
                self.clef.octave_change = int(chars)
            if hasattr(self, "clef"):
                if hasattr(self.clef, "sign"):
                    if hasattr(self.clef, "line"):
                        entry = str(self.clef)
                        self.clef = None
            if self.byTag:
                if tag not in self.parent.tracked and tag not in ["mode","fifths","sign","line"]:
                    self.parent.tracked[tag] = {self.parent.file: {"value": entry, "attribs": {self.parent.file:self.attrib}}}
                if self.parent.file not in self.parent.tracked[tag]:
                    self.parent.tracked[tag][self.parent.file] = {"value": entry, "attribs": {self.parent.file:self.attrib}}
            else:
                if entry not in self.parent.tracked:
                    self.parent.tracked[entry] = {self.parent.file: {"tag": tag, "attribs": {self.parent.file:self.attrib}}}
                if self.parent.file not in self.parent.tracked[entry]:
                    self.parent.tracked[entry][self.parent.file] = {"tag":tag, "attribs":self.attrib}


    def endElement(self, name):
        self.name = ""
        self.attrib = {}