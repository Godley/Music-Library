import xml.sax
import copy
from xml.sax import handler, make_parser
from MuseParse import helpers

from implementation.primaries.ExtractMetadata.classes.hashdict import hashdict
from implementation.primaries.ExtractMetadata.classes.DataLayer.helpers import get_if_exists
from implementation.primaries.ExtractMetadata.classes.helpers import combine_dictionaries, init_kv


class Extractor(xml.sax.ContentHandler):

    def __init__(self, parent):
        self.parent = parent

    def startElement(self, name, attrs):
        attribs = {}
        for attrname in attrs.getNames():
            attrvalue = attrs.getValue(attrname)
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
            "part-name": make_new_part,
            "key": handle_clef_or_key,
            "clef": handle_clef_or_key,
            "transpose": handleTransposition,
            "time": handleMeter,
            "metronome": handle_tempo,
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
        self.pop_name(name)

        if len(self.tags) > 0 and self.tags[-1] in self.handlers:
            self.current_handler = self.handlers[self.tags[-1]]

    def pop_name(self, name):
        if name in self.tags:
            self.tags.remove(name)
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
        self.collate_parts()
        fob.close()
        return self.data

    def collate_parts(self):
        instrument_list = []
        keys = ["key", "clef"]
        for part in self.parts:
            data = {}
            data["name"] = get_if_exists(
                self.parts[part], "name", "hello, world")

            if "transposition" in self.parts[part]:
                data.update(self.parts[part]["transposition"])
                # data["transposition"] = self.parts[part]["transposition"]

            for key in keys:
                if key in self.parts[part]:
                    init_kv(self.data, "{}s".format(key), init_value={})
                    self.data["{}s".format(key)][
                        data["name"]] = remove_duplicates(
                        self.parts[part][key])

            instrument_list.append(data)
        self.data["instruments"] = instrument_list


# HANDLER METHODS


def make_new_part(tags, attrs, chars, parts, data):
    """
    handler which works with anything inside the score-part tag, which creates a new part inside the data dict
    :param tags: current list of xml tags
    :param attrs: current dict of attribs
    :param chars: current dict of content of each tag
    :return: string of instrument name and a dict so the part dict can be updated
    """
    id = helpers.GetID(attrs, "score-part", "id")
    if id is not None:
        init_kv(parts, id, init_value={})
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
    tag_dict = {"clef": ("line", "sign"), "key": ("fifths", "mode")}
    if id is not None:
        init_kv(parts, id, init_value={})
        if tags[-2] in tag_dict:
            init_kv(parts[id], tags[-2], init_value=[])
            elem_to_add = create_elem(
                chars, tag_dict[tags[-2]][0], tag_dict[tags[-2]][1])
            tag_type = tags[-2]
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
    data.setdefault("time_signatures", [])

    if tags[-1] != "time" and "time" in tags:
        elem = create_elem(chars, "beats", "beat-type", cast2=int)
        tag_type = ''
        if tags[-1] == "beats":
            tag_type = "beat"

        if tags[-1] == "beat-type":
            tag_type = "beat_type"

        update_or_append_entry(data["time_signatures"], tag_type, elem)
        # if len(data["time"]) == 0 or "type" in data["time"][-1]:
        #     data["time"].append({"type": int(b_type)})
        # else:
        #     data["time"][-1]["type"] = int(b_type)


def handle_tempo(tags, attrs, chars, parts, data):
    data.setdefault("tempos", [])

    if tags[-1] != "metronome":
        elem = create_elem(
            chars,
            "beat-unit",
            "per-minute",
            cast1=str,
            cast2=int)
        data["tempos"] = handle_beat_unit(elem, data["tempos"], tags[-1])
        data["tempos"] = handle_beat_unit_dot(data["tempos"], tags[-1])

        if tags[-1] == "per-minute":
            update_or_append_entry(data["tempos"], "minute", elem)


def handle_beat_unit_dot(list_of_dicts, tag):
    if tag == "beat-unit-dot":
        copy_of_dict = copy.deepcopy(list_of_dicts)
        if len(copy_of_dict) > 0:
            if "beat_2" in copy_of_dict[-1]:
                copy_of_dict[-1]["beat_2"] += "."
            elif "beat" in copy_of_dict[-1]:
                copy_of_dict[-1]["beat"] += "."
        return copy_of_dict
    return list_of_dicts


def handle_beat_unit(elem, list_of_dicts, tag):

    if tag == 'beat-unit':
        copy_of_dict = copy.deepcopy(list_of_dicts)

        if beat1_and_minute_or_beat2_exists(copy_of_dict):
            copy_of_dict.append({"beat": elem})

        # if not, we dump it as the first beat of the first tempo
        elif "beat" not in copy_of_dict[-1]:
            copy_of_dict[-1]["beat"] = elem

        # finally, if the first tempo doesn't have a second beat, or a minute,
        # we put it as the second beat of the tempo. MusicXML sucks.
        elif not minute_or_beat2_exists(copy_of_dict):
            copy_of_dict[-1]["beat_2"] = elem
        return copy_of_dict
    return list_of_dicts


def beat1_and_minute_or_beat2_exists(list_of_dicts):
    answer = False
    if len(list_of_dicts) == 0:
        answer = True
    elif "beat" in list_of_dicts[-1] and minute_or_beat2_exists(list_of_dicts):
        answer = True
    return answer


def minute_or_beat2_exists(list_of_dicts):
    answer = False
    if len(list_of_dicts) == 0:
        answer = True
    elif "minute" in list_of_dicts[-1] or "beat_2" in list_of_dicts[-1]:
        answer = True
    return answer


def handleBibliography(tags, attrs, chars, parts, data):
    if tags[-1] == "creator":
        creator_type = helpers.GetID(attrs, "creator", "type")
        if creator_type is not None:
            init_kv(data, creator_type, init_value="")
            if "creator" in chars:
                data[creator_type] += chars["creator"].lower()

    handle_title(tags[-1], chars, data)


def handle_title(tag, chars, data):
    if tag == "movement-title" or tag == "work-title":
        title = create_elem(
            chars,
            "movement-title",
            "work-title",
            cast1=str,
            cast2=str)
        init_kv(data, "title", init_value="")
        data["title"] += title.lower()


def remove_duplicates(list_of_dicts):
    hashdict_list = [hashdict(item) for item in list_of_dicts]
    hashdict_set = set(hashdict_list)
    hslist = [dict(item) for item in hashdict_set]
    return hslist
