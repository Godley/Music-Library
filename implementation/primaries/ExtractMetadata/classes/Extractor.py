from xml.sax import ContentHandler
from implementation.primaries.Loading.classes import Key

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
        key = self.name
        if key != "":
            if self.name == "key":
                self.key = Key.Key()
            if self.name == "fifths":
                self.key.fifths = int(chars)
            if self.name == "mode":
                self.key.mode = chars
                key = "key"
            if hasattr(self, "key"):
                if hasattr(self.key, "fifths"):
                    if hasattr(self.key, "mode"):
                        entry = str(self.key)
            if self.byTag:
                pass
            else:
                if entry not in self.parent.tracked:
                    self.parent.tracked[entry] = {"files": [self.parent.file], "tags": [key], "attribs": {self.parent.file:self.attrib}}
                if self.parent.file not in self.parent.tracked[entry]["files"]:
                    self.parent.tracked[entry]["files"].append(self.parent.file)
                if key not in self.parent.tracked[entry]["tags"]:
                    self.parent.tracked[entry]["tags"].append(key)
                if self.parent.file not in self.parent.tracked[entry]["attribs"]:
                    self.parent.tracked[entry]["tags"]["attribs"] = self.attrib


    def endElement(self, name):
        self.name = ""
        self.attrib = {}