import xml.sax
from xml.sax import handler, make_parser
from implementation.primaries.Drawing.classes import helpers

class MetaParser(object):
    def __init__(self):
        self.tags = []
        self.attribs = {}
        self.chars = {}
        self.handlers = {"part-name":makeNewPart}
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
                data = self.current_handler(self.tags, self.attribs, self.chars)
                if self.tags[-1] == "part-name":
                    self.parts.update(data[1])
                    if "instruments" not in self.data:
                        self.data["instruments"] = []
                    self.data["instruments"].append(data[0])

    def EndTag(self, name):
        if name in self.close_tags:
            if self.current_handler is not None:
                data = self.current_handler(self.tags,self.attribs,self.chars)
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
def makeNewPart(tags, attrs, chars):
    '''
    handler which works with anything inside the score-part tag, which creates a new part inside the data dict
    :param tags: current list of xml tags
    :param attrs: current dict of attribs
    :param chars: current dict of content of each tag
    :return: not sure yet lol
    '''
    data = {}
    id = helpers.GetID(attrs, "score-part", "id")
    if id is not None:
        data = {id:{}}
    if tags[-1] == "part-name":
        if "part-name" in chars:
            name = chars["part-name"]
            data[id]["name"] = name
            return name, data
    return data