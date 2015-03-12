import xml.sax
from xml.sax import handler, make_parser
from implementation.primaries.Drawing.classes import helpers

class MetaParser(object):
    def __init__(self):
        self.tags = []
        self.attribs = {}
        self.chars = {}
        self.handlers = {"part-name":makeNewPart,"key":handleKey,"clef":handleClef,"transpose":handleTransposition,
                         "time":handleMeter}
        self.close_tags = []
        self.current_handler = None
        self.parts = {}
        self.data = {}

    def StartTag(self, name, attrs):
        self.tags.append(name)
        self.attribs[name] = attrs
        if name in self.handlers:
            self.current_handler = self.handlers[name]

    def NewData(self, data):
        if len(self.tags) > 0:
            self.chars[self.tags[-1]] = data
            if self.current_handler is not None and self.tags[-1] not in self.close_tags:
                self.current_handler(self.tags, self.attribs, self.chars, self.parts, self.data)

    def EndTag(self, name):
        if name in self.close_tags:
            if self.current_handler is not None:
                self.current_handler(self.tags,self.attribs,self.chars, self.parts, self.data)
        self.tags.remove(name)

        if len(self.tags) > 0 and self.tags[-1] in self.handlers:
            self.current_handler = self.handlers[self.tags[-1]]

        self.attribs.pop(name)
        if name in self.chars:
            self.chars.pop(name)

    def parse(self, file):
        parser = make_parser()
        class Extractor(xml.sax.ContentHandler):
            def __init__(self, parent):
                self.parent = parent

            def startElement(self, name, attrs):
                attribs = {}
                for attrname in attrs.getNames():
                    attrvalue = attrs.get(attrname)
                    attribs[attrname] = attrvalue
                self.parent.StartTag(name, attribs)

            def characters(self, text):
                self.parent.NewData(text)

            def endElement(self, name):
                self.parent.EndTag(name)
        parser.setContentHandler(Extractor(self))
        # OFFLINE MODE
        parser.setFeature(handler.feature_external_ges, False)
        fob = open(file, 'r')
        parser.parse(fob)
        return self.piece

# HANDLER METHODS
def makeNewPart(tags, attrs, chars, parts, data):
    '''
    handler which works with anything inside the score-part tag, which creates a new part inside the data dict
    :param tags: current list of xml tags
    :param attrs: current dict of attribs
    :param chars: current dict of content of each tag
    :return: string of instrument name and a dict so the part dict can be updated
    '''
    id = helpers.GetID(attrs, "score-part", "id")
    if id is not None:
        if id not in parts:
            parts[id] = {}
    if tags[-1] == "part-name":
        if "part-name" in chars:
            name = chars["part-name"]
            parts[id]["name"] = name
            if "instruments" not in data:
                data["instruments"] = []
            data["instruments"].append(name)

def handleKey(tags, attrs, chars, parts, data):
    id = helpers.GetID(attrs, "part", "id")
    if id is not None:
        if id not in parts:
            parts[id] = {}

        if "key" not in parts[id]:
            parts[id]["key"] = []

        if tags[-1] != "key":
            thing = 0
            if "fifths" in chars:
                thing = int(chars["fifths"])
            if "mode" in chars:
                thing = chars["mode"]
            if len(parts[id]["key"]) == 0 or tags[-1] in parts[id]["key"][-1]:
                parts[id]["key"].append({tags[-1]:thing})
            elif tags[-1] not in parts[id]["key"][-1]:
                parts[id]["key"][-1][tags[-1]] = thing

def handleClef(tags, attrs, chars, parts, data):
    id = helpers.GetID(attrs, "part", "id")
    if id is not None:
        if id not in parts:
            parts[id] = {}

        if "clef" not in parts[id]:
            parts[id]["clef"] = []

        if tags[-1] != "clef":
            thing = 0
            if "line" in chars:
                thing = int(chars["line"])
            if "sign" in chars:
                thing = chars["sign"]
            if len(parts[id]["clef"]) == 0 or tags[-1] in parts[id]["clef"][-1]:
                parts[id]["clef"].append({tags[-1]:thing})
            elif tags[-1] not in parts[id]["clef"][-1]:
                parts[id]["clef"][-1][tags[-1]] = thing

def handleTransposition(tags, attrs, chars, parts, data):
    id = helpers.GetID(attrs, "part", "id")
    if id is not None:
        if id not in parts:
            parts[id] = {}

        if "transposition" not in parts[id]:
            parts[id]["transposition"] = {}

        if tags[-1] != "transposition":
            content = 0
            if tags[-1] in chars:
                content = int(chars[tags[-1]])
            parts[id]["transposition"][tags[-1]] = content

def handleMeter(tags, attrs, chars, parts, data):
    if "time" not in data:
        data["time"] = []

    if tags[-1] != "time":
        beat = 0
        b_type = 0
        if tags[-1] == "beats":
            if "beats" in chars:
                beat = chars["beats"]

            if len(data["time"]) == 0 or "beat" in data["time"][-1]:
                data["time"].append({"beat":int(beat)})
            else:
                data["time"][-1]["beat"] = int(beat)

        if tags[-1] == "beat-type":
            if "beat-type" in chars:
                b_type = chars["beat-type"]

            if len(data["time"]) == 0 or "type" in data["time"][-1]:
                data["time"].append({"type":int(b_type)})
            else:
                data["time"][-1]["type"] = int(b_type)

def handleMetronome(tags, attrs, chars, parts, data):
    pass





