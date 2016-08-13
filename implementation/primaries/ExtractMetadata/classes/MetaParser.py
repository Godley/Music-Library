import xml.sax
from xml.sax import handler, make_parser
from MuseParse import helpers

from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict
from implementation.primaries.ExtractMetadata.classes.helpers import combine_dictionaries

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
            "key": handle_clef_or_key,
            "clef": handle_clef_or_key,
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
        parser.parse(fob)
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


def handle_clef_or_key(tags, attrs, chars, parts, data):
    """
    Since clefs and keys are very similar, handle them in the same method
    """
    id = helpers.GetID(attrs, "part", "id")
    if id is not None:
        init_kv(parts, id, init_value={})

        if "clef" in tags:
            init_kv(parts[id], "clef", init_value=[])
            elem_to_add = create_elem(chars, "line", "sign")
            tag_type = "clef"
            if tags[-1] != "clef":
                update_or_append_entry(parts[id][tag_type], tags[-1], elem_to_add)


        elif "key" in tags:
            init_kv(parts[id], "key", init_value=[])
            elem_to_add = create_elem(chars, "fifths", "mode")
            tag_type = "key"
            if tags[-1] != "key":
                update_or_append_entry(parts[id][tag_type], tags[-1], elem_to_add)


def update_or_append_entry(dictionary, tag, entry):
    """
    Method to check if a dictionary is empty, or if it's last entry contains the tag
    being added. If yes, create a new entry. If it doesn't contain the tag,
    add it. Used by clef and key creation queries, might be used by other handlers in future
    """
    if len(dictionary) == 0 or tag in dictionary[-1]:
        dictionary.append({tag: entry})
    elif tag not in dictionary[-1]:
        dictionary[-1][tag] = entry

def init_kv(elem, key, init_value=list()):
    """
    Initialise a key in a dictionary with a default value if it doesn't exist already
    """
    if key not in elem:
        elem[key] = init_value

def create_elem(chars, key1, key2, cast1=int, cast2=str):
    """
    select a return value from chars dictionary. Priority given to key 2 over key 1,
    both are cast to whatever value we need. Used by clef and key handlers as both
    need the first element, then the second, and both happen to be format int then str.
    Made generic as poss incase this is useful elsewhere.
    """
    return_value = 0
    if key1 in chars:
        return_value = cast1(chars[key1])
    if key2 in chars:
        return_value = cast2(chars[key2])
    return return_value


def handleTransposition(tags, attrs, chars, parts, data):
    id = helpers.GetID(attrs, "part", "id")
    if id is not None:
        init_kv(parts, id, init_value={})
        init_kv(parts[id], "transposition", init_value={})

        if tags[-1] == "diatonic" or tags[-1] == "chromatic":
            content = 0
            if tags[-1] in chars:
                content = int(chars[tags[-1]])
            parts[id]["transposition"][tags[-1]] = content


def handleMeter(tags, attrs, chars, parts, data):
    init_kv(data, "time", init_value=[])

    if tags[-1] != "time" and "time" in tags:
        elem = create_elem(chars, "beats", "beat-type", cast2=int)
        tag_type = ''
        if tags[-1] == "beats":
            tag_type = "beat"

        if tags[-1] == "beat-type":
            tag_type = "type"

        update_or_append_entry(data["time"], tag_type, elem)
            # if len(data["time"]) == 0 or "type" in data["time"][-1]:
            #     data["time"].append({"type": int(b_type)})
            # else:
            #     data["time"][-1]["type"] = int(b_type)


def handleTempo(tags, attrs, chars, parts, data):
    init_kv(data, "tempo", [])

    if tags[-1] != "metronome":

        if tags[-1] == "beat-unit-dot":
            if len(data["tempo"]) > 0:
                if "beat_2" in data["tempo"][-1]:
                    data["tempo"][-1]["beat_2"] += "."
                elif "beat" in data["tempo"][-1]:
                    data["tempo"][-1]["beat"] += "."

        elem = create_elem(chars, "beat-unit", "per-minute", cast1=str, cast2=int)
        if tags[-1] == "beat-unit":

            # beat could either be a first beat of a tempo,
            # or a second beat of a tempo. Each tempo can only have either
            # a minute or a second beat, so we check first if there are no tempos,
            # then if the first tempo has a beat, then if the first tempo has a second beat
            # if all above is true, then we append it.
            if tags[-1] == "beat-unit":
                if len(data["tempo"]) == 0 or \
                    ("beat" in data["tempo"][-1] and
                         ("minute" in data["tempo"][-1] or "beat_2" in data["tempo"][-1])
                     ):
                    data["tempo"].append({"beat": elem})

            # if not, we dump it as the first beat of the first tempo
                elif "beat" not in data["tempo"][-1]:
                    data["tempo"][-1]["beat"] = elem

                # finally, if the first tempo doesn't have a second beat, or a minute,
                # we put it as the second beat of the tempo. MusicXML sucks.
                elif "minute" not in data["tempo"][-1] and "beat_2" not in data["tempo"][-1]:
                    data["tempo"][-1]["beat_2"] = elem

        elif tags[-1] == "per-minute":
            update_or_append_entry(data["tempo"], "minute", elem)


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
