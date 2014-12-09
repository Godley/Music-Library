import xml.sax

from classes import Piece, Part, Measure, Meta, Key, Meter, Note, Clef


piece = Piece.Piece()
part_id = None
note_id = None
divisions = None
note = None


def ignore_exception(IgnoreException=Exception, DefaultVal=None):
    """ Decorator for ignoring exception from a function
    e.g.   @ignore_exception(DivideByZero)
    e.g.2. ignore_exception(DivideByZero)(Divide)(2/0)
    borrowed from: http://stackoverflow.com/questions/2262333/is-there-a-built-in-or-more-pythonic-way-to-try-to-parse-a-string-to-an-integer
    """

    def dec(function):
        def _dec(*args, **kwargs):
            try:
                return function(*args, **kwargs)
            except IgnoreException:
                return DefaultVal

        return _dec

    return dec


def SetupPiece(tag, attrib, content):
    if content is not []:
        if not hasattr(piece, "meta"):
            if tag[-1] == "creator" and attrib["creator"]["type"] == "composer":
                piece.meta = Meta.Meta(composer=content["creator"])
            elif tag[-1] == "movement-title":
                piece.meta = Meta.Meta(title=content["movement-title"])
        if tag[-1] == "movement-title":
            piece.meta.title = content["movement-title"]
        if tag[-1] == "creator" and attrib["creator"]["type"] == "composer":
            piece.meta.composer = content["creator"]


def UpdatePart(tag, attrib, content):
    global measure_id, part_id
    if "score-part" in tag:
        if part_id not in piece.Parts.keys():
                part_id = attrib["id"]
                piece.Parts[part_id] = Part.Part()
    if "part" in tag:
        if "id" in attrib:
            part_id = attrib["id"]
            if part_id not in piece.Parts:
                print "whoops"
    part = piece.Parts[part_id]
    if "part-name" in tag:
        if "part-name" in content:
            part.name = content["part-name"]

def HandleMeasures(tag, attrib, content):

    global measure_id, part_id
    if part_id not in piece.Parts.keys():
        if "part" in attrib.keys():
            part_id = attrib["part"]["id"]
            if part_id not in piece.Parts.keys():
                UpdatePart(tag, attrib, content)
    part = piece.Parts[part_id]
    if "measure" in tag:
        if measure_id not in part.measures:
            # attrib here only references the index it needs, as measure has no text content so calls its handler in the starttag method
            measure_id = int(attrib["number"])
            if "width" in attrib:
                part.measures[measure_id] = Measure.Measure(width=attrib["width"])
            else:
                part.measures[measure_id] = Measure.Measure()
    measure = part.measures[measure_id]
    if tag[-1] == "divisions":
        measure.divisions = int(content["divisions"])
    if tag[-1] == "mode":
        if hasattr(measure, "key"):
            measure.key.mode = content["mode"]
        else:
            measure.key = Key.Key(mode=content["mode"])
    if tag[-1] == "fifths":
        if hasattr(measure, "key"):
            measure.key.fifths = content["fifths"]
        else:
            measure.key = Key.Key(fifths=int(content["fifths"]))

    if tag[-1] == "beat-type":
        measure.meter = Meter.Meter(int(content["beats"]), int(content["beat-type"]))

    if tag[-1] == "line" and "clef" in tag:
        measure.clef = Clef.Clef(sign=content["sign"], line=content["line"])
    if "transpose" in tag:
        if "diatonic" in tag:
            if hasattr(measure, "transpose"):
                measure.transpose.diatonic = content["diatonic"]
            else:
                measure.transpose = Measure.Transposition(diatonic=content["diatonic"])
        if "chromatic" in tag:
            if hasattr(measure, "transpose"):
                measure.transpose.chromatic = content["chromatic"]
            else:
                measure.transpose = Measure.Transposition(chromatic=content["chromatic"])
        if "octave-change" in tag:
            if hasattr(measure, "transpose"):
                measure.transpose.octave = content["octave-change"]
            else:
                measure.transpose = Measure.Transposition(octave=content["octave-change"])


def CheckID(tag, attrs, string, id_name):
    if string in tag:
        return attrs[string][id_name]


def CreateNote(tag, attrs, content):
    global note_id, note, part_id, measure_id
    if part_id is None:
        part_id = CheckID(tag, attrs, "part", "id")
        if part_id not in piece.Parts:
            UpdatePart(tag, attrs, content)
    if measure_id is None:
        measure_id = int(CheckID(tag, attrs, "measure", "number"))
        if measure_id not in piece.Parts[part_id].measures:
            HandleMeasures(tag, attrs, content)
    measure = piece.Parts[part_id].measures[measure_id]
    if "note" in tag and note is None:
        note = Note.Note()
        measure.notes.append(note)
        note_id = len(measure.notes) - 1

    if "rest" in tag:
        note.rest = True
    if tag[-1] == "duration" and "note" in tag:
        note.duration = float(content["duration"])
        if hasattr(measure, "divisions"):
            note.divisions = float(measure.divisions)

    if "dot" in tag:
        note.dotted = True
    if "tie" in tag:
        note.ties.append(Note.Tie(attrs["type"]))
    if "chord" in tag:
        note.chord = True
    if tag[-1] == "stem":
        note.stem = Note.Stem(content["stem"])


def SetupFormat(tags, attrs, text):
    return None


def HandlePitch(tags, attrs, text):
    if note is None:
        CreateNote(tags, attrs, text)
    if "pitch" in tags:
        if not hasattr(note, "pitch"):
            note.pitch = Note.Pitch()
    if tags[-1] == "step":
        note.pitch.step = text["step"]
    if tags[-1] == "alter":
        note.pitch.accidental = text["alter"]
    if tags[-1] == "octave":
        note.pitch.octave = text["octave"]


measure_id = None
structure = {"movement-title": SetupPiece, "creator": SetupPiece, "defaults": SetupFormat, "part": UpdatePart,
             "score-part": UpdatePart, "measure": HandleMeasures, "note": CreateNote,
             "pitch": HandlePitch}
multiple_attribs = ["beats", "sign"]
closed_tags = ["tie","dot","chord","note","measure","part","score-part"]

class MxmlParser:
    def __init__(self):
        self.tags = []
        self.chars = {}
        self.attribs = {}
        self.handler = None

    def Flush(self):
        self.tags = []
        self.chars = []
        self.attribs = {}

    def StartTag(self, name, attrs):
        if name in structure.keys():
            self.handler = structure[name]
        self.tags.append(name)

        # handle tags which close immediately, or do not have any text content
        if name in closed_tags:
            self.handler(self.tags, attrs, None)
        else:
            if attrs is not None:
                self.attribs[name] = attrs

    def ValidateData(self, text):
        if text == "\n":
            return False
        for c in text:
            if c != " ":
                return True
        return False


    def NewData(self, text):
        sint = ignore_exception(ValueError)(int)
        if self.tags[-1] == "beat-type" or self.tags[-1] == "beats":
            if sint(text) is int:
                self.chars[self.tags[-1]] = text

        if self.ValidateData(text):
            self.chars[self.tags[-1]] = text
            if self.handler is not None:
                self.handler(self.tags, self.attribs, self.chars)

    def EndTag(self, name):
        global part_id, measure_id, note_id, pitch, note
        if name == "rest":
            CreateNote(self.tags, self.attribs, self.chars)
        if name == "note":
            self.handler = HandleMeasures
            note = None
            note_id = None
        self.tags.remove(name)
        if name == "score-part" or name == "part":
            part_id = None
            self.handler = None
        if name == "measure":
            measure_id = None
            self.handler = None
        if name == "pitch":
            self.handler = CreateNote
        if name in self.chars.keys() and name not in multiple_attribs:
            self.chars.pop(name)
        if name in self.attribs.keys() and name not in multiple_attribs:
            self.attribs.pop(name)

    def parse(self, file):
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

        xml.sax.parse(file, Extractor(self))


indent = 3
p = MxmlParser()
p.parse("reading/ActorPreludeSample.xml")
print str(piece)