import xml.sax
from xml.sax import handler, make_parser
from MuseParse import helpers

from implementation.primaries.ExtractMetadata.classes.HashableDictionary import hashdict


class Extractor(xml.sax.ContentHandler):

    def __init__(self, parent):
        self.parent = parent

    def startElement(self, name, attrs):
        attribs = {}
        for attrname in attrs.getNames():
            attrvalue = attrs.get(attrname)
            attribs[attrname] = attrvalue
        self.parent.startTag(name, attribs)

    def characters(self, text):
        self.parent.newData(text)

    def endElement(self, name):
        self.parent.endTag(name)


class MetaParser(object):

    def __init__(self):
        self.tags = []
        self.attribs = {}
        self.chars = {}
        self.handlers = {
            "part-name": makeNewPart,
            "key": handleKey,
            "clef": handleClef,
            "transpose": handleTransposition,
            "time": handleMeter,
            "metronome": handleTempo,
            "movement-title": handleBibliography,
            "work-title": handleBibliography,
            "creator": handleBibliography,
            "credit-words": handleBibliography}
        self.close_tags = ["beat-unit-dot"]
        self.current_handler = None
        self.parts = {}
        self.data = {}

    def startTag(self, name, attrs):
        self.tags.append(name)
        self.attribs[name] = attrs
        if name in self.handlers:
            self.current_handler = self.handlers[name]

    def validateData(self, data):

        pass

    def newData(self, data):
        if len(self.tags) > 0:
            self.chars[self.tags[-1]] = data
            if self.current_handler is not None and self.tags[
                    -1] not in self.close_tags:
                self.current_handler(
                    self.tags,
                    self.attribs,
                    self.chars,
                    self.parts,
                    self.data)

    def endTag(self, name):
        if name in self.close_tags:
            if self.current_handler is not None:
                self.current_handler(
                    self.tags,
                    self.attribs,
                    self.chars,
                    self.parts,
                    self.data)
        self.tags.remove(name)

        if len(self.tags) > 0 and self.tags[-1] in self.handlers:
            self.current_handler = self.handlers[self.tags[-1]]

        if name in self.attribs:
            self.attribs.pop(name)
        if name in self.chars:
            self.chars.pop(name)

    def parse(self, file):
        parser = make_parser()

        parser.setContentHandler(Extractor(self))
        # OFFLINE MODE
        parser.setFeature(handler.feature_external_ges, False)
        fob = open(file, 'r')
        parser.decode(fob)
        self.collatePartsIntoData()
        fob.close()
        return self.data

    def collatePartsIntoData(self):
        instrument_list = []
        clef_list = {}
        key_list = {}
        for part in self.parts:

            data = {}
            if "name" in self.parts[part]:
                data["name"] = self.parts[part]["name"]
            else:
                self.parts[part]["name"] = "hello, world"
                data["name"] = "hello, world"

            if "transposition" in self.parts[part]:
                data["transposition"] = self.parts[part]["transposition"]
            if "key" in self.parts[part]:
                hashdict_list = [hashdict(item)
                                 for item in self.parts[part]["key"]]
                hashdict_set = set(hashdict_list)
                key_list[self.parts[part]["name"]] = hashdict_set
            if "clef" in self.parts[part]:
                hashdict_list = [hashdict(item)
                                 for item in self.parts[part]["clef"]]
                hashdict_set = set(hashdict_list)
                clef_list[self.parts[part]["name"]] = hashdict_set
            instrument_list.append(data)
        self.data["instruments"] = instrument_list
        if key_list != {}:
            self.data["key"] = key_list
        if clef_list != {}:
            self.data["clef"] = clef_list


# HANDLER METHODS


def makeNewPart(tags, attrs, chars, parts, data):
    """
    handler which works with anything inside the score-part tag, which creates a new part inside the data dict
    :param tags: current list of xml tags
    :param attrs: current dict of attribs
    :param chars: current dict of content of each tag
    :return: string of instrument name and a dict so the part dict can be updated
    """
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

        if tags[-1] == "fifths" or tags[-1] == "mode":
            thing = 0
            if "fifths" in chars:
                thing = int(chars["fifths"])
            if "mode" in chars:
                thing = chars["mode"]
            if len(parts[id]["key"]) == 0 or tags[-1] in parts[id]["key"][-1]:
                parts[id]["key"].append({tags[-1]: thing})
            elif tags[-1] not in parts[id]["key"][-1]:
                parts[id]["key"][-1][tags[-1]] = thing


def handleClef(tags, attrs, chars, parts, data):
    id = helpers.GetID(attrs, "part", "id")
    if id is not None:
        if id not in parts:
            parts[id] = {}

        if "clef" not in parts[id]:
            parts[id]["clef"] = []

        if tags[-1] == "line" or tags[-1] == "sign":
            thing = 0
            if "line" in chars:
                thing = int(chars["line"])
            if "sign" in chars:
                thing = chars["sign"]
            if len(parts[id]["clef"]) == 0 or tags[-
                                                   1] in parts[id]["clef"][-
                                                                           1]:
                parts[id]["clef"].append({tags[-1]: thing})
            elif tags[-1] not in parts[id]["clef"][-1]:
                parts[id]["clef"][-1][tags[-1]] = thing


def handleTransposition(tags, attrs, chars, parts, data):
    id = helpers.GetID(attrs, "part", "id")
    if id is not None:
        if id not in parts:
            parts[id] = {}

        if "transposition" not in parts[id]:
            parts[id]["transposition"] = {}

        if tags[-1] == "diatonic" or tags[-1] == "chromatic":
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
                try:
                    data["time"].append({"beat": int(beat)})
                except:
                    data["time"].append({"beat": beat})
            else:
                data["time"][-1]["beat"] = int(beat)

        if tags[-1] == "beat-type":
            if "beat-type" in chars:
                b_type = chars["beat-type"]

            if len(data["time"]) == 0 or "type" in data["time"][-1]:
                data["time"].append({"type": int(b_type)})
            else:
                data["time"][-1]["type"] = int(b_type)


def handleTempo(tags, attrs, chars, parts, data):
    if "tempo" not in data:
        data["tempo"] = []

    if tags[-1] != "metronome":
        beat = 0
        minute = 0

        if tags[-1] == "beat-unit-dot":
            if len(data["tempo"]) > 0:
                if "beat_2" in data["tempo"][-1]:
                    data["tempo"][-1]["beat_2"] += "."
                elif "beat" in data["tempo"][-1]:
                    data["tempo"][-1]["beat"] += "."

        if tags[-1] == "beat-unit":
            if "beat-unit" in chars:
                beat = chars["beat-unit"]

            if len(data["tempo"]) == 0 or ("beat" in data["tempo"][-
                                                                   1] and ("minute" in data["tempo"][-
                                                                                                     1] or "beat_2" in data["tempo"][-
                                                                                                                                     1])):
                data["tempo"].append({"beat": beat})
            elif "beat" not in data["tempo"][-1]:
                data["tempo"][-1]["beat"] = beat
            elif "minute" not in data["tempo"][-1] and "beat_2" not in data["tempo"][-1]:
                data["tempo"][-1]["beat_2"] = beat

        if tags[-1] == "per-minute":
            if "per-minute" in chars:
                minute = chars["per-minute"]

            if len(data["tempo"]) == 0 or "minute" in data["tempo"][-1]:
                data["tempo"].append({"minute": int(minute)})
            else:
                data["tempo"][-1]["minute"] = int(minute)


def handleBibliography(tags, attrs, chars, parts, data):
    if tags[-1] == "creator":
        creator_type = helpers.GetID(attrs, "creator", "type")
        if creator_type is not None:
            if creator_type not in data:
                data[creator_type] = ""
            if "creator" in chars:
                data[creator_type] += chars["creator"].lower()

    if tags[-1] == "movement-title" or tags[-1] == "work-title":
        title = ""
        if "movement-title" in chars:
            title = chars["movement-title"]
        if "work-title" in chars:
            title = chars["work-title"]
        if "title" not in data:
            data["title"] = ""
        data["title"] += title.lower()
