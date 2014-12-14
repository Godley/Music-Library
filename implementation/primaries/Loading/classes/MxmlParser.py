import xml.sax

from implementation.primaries.Loading.classes import Piece, Part, Measure, Meta, Key, Meter, Note, Clef, text

note = None
part_id = None
measure_id = None

class MxmlParser:
    '''this needs a huge tidy, but this class:
        sets up a few things that define where the tags get handled
        runs sax, which calls the parent methods according to what's happened
        the parent methods call the handlers defined in structure, or else figure out what handler to use. If there absolutely isn't one, nothing gets called
        spits out a piece class holding all this info.
    '''
    def __init__(self, excluded=[]):
        self.tags = []
        self.chars = {}
        self.attribs = {}
        self.handler = None
        self.excluded = excluded

        # add any handlers, along with the tagname associated with it, to this dictionary
        self.structure = {"movement-title": SetupPiece, "creator": SetupPiece, "defaults": SetupFormat, "part": UpdatePart,
             "score-part": UpdatePart, "measure": HandleMeasures, "note": CreateNote,
             "pitch": HandlePitch,"direction":HandleDirections}
        # not sure this is needed anymore, but tags which we shouldn't clear the previous data for should be added here
        self.multiple_attribs = ["beats", "sign"]
        # any tags which close instantly in here
        self.closed_tags = ["tie","dot","chord","note","measure","part","score-part","sound","print","rest"]
        self.piece = Piece.Piece()

    def Flush(self):
        self.tags = []
        self.chars = []
        self.attribs = {}

    def StartTag(self, name, attrs):
        if name not in self.excluded:
            if name in self.structure.keys():
                self.handler = self.structure[name]

            self.tags.append(name)
            if attrs is not None:
                self.attribs[name] = attrs
            d = CheckDynamics(name)
            if d:
                self.handler(self.tags, attrs, None, self.piece)
            # handle tags which close immediately, or do not have any text content
            if name in self.closed_tags:
                self.handler(self.tags, attrs, None, self.piece)

    def ValidateData(self, text):
        if text == "\n":
            return False
        for c in text:
            try:
                if str(c) != " ":
                    return True
            except:
                return False
        return False


    def NewData(self, text):
        sint = ignore_exception(ValueError)(int)
        if len(self.tags) > 0:
            if self.tags[-1] == "beat-type" or self.tags[-1] == "beats":
                if sint(text) is int:
                    self.chars[self.tags[-1]] = text

        if self.ValidateData(text):
            if len(self.tags) > 0:
                self.chars[self.tags[-1]] = text
            if self.handler is not None:
                self.handler(self.tags, self.attribs, self.chars, self.piece)



    def EndTag(self, name):
        global part_id, measure_id, note
        if name == "note":
            self.handler = HandleMeasures
            note = None
        self.tags.remove(name)
        if name == "score-part" or name == "part":
            part_id = None
            self.handler = None
        if name == "measure":
            measure_id = None
            self.handler = None
        if name == "pitch":
            self.handler = CreateNote
        if name == "direction":
            self.handler = HandleMeasures
        if name == "movement-title":
            self.handler = None

        if name in self.chars.keys() and name not in self.multiple_attribs:
            self.chars.pop(name)
        if name in self.attribs.keys() and name not in self.multiple_attribs:
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
        return self.piece


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


def SetupPiece(tag, attrib, content, piece):
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


def UpdatePart(tag, attrib, content, piece):
    global measure_id, part_id
    if "score-part" in tag:
        if part_id not in piece.Parts.keys():
                part_id = attrib["id"]
                piece.Parts[part_id] = Part.Part()
    if "part" in tag:
        if "id" in attrib:
            part_id = attrib["id"]
            if part_id not in piece.Parts:
                print("whoops")
    part = piece.Parts[part_id]
    if "part-name" in tag:
        if "part-name" in content:
            part.name = content["part-name"]

def HandleMeasures(tag, attrib, content, piece):
    global measure_id, part_id
    part = None
    if part_id is not None:
        part = piece.Parts[part_id]
    if "measure" in tag and part is not None:
        if measure_id not in part.measures:
            # attrib here only references the index it needs, as measure has no text content so calls its handler in the starttag method
            measure_id = int(attrib["number"])
            if "width" in attrib:
                part.measures[measure_id] = Measure.Measure(width=attrib["width"])
            else:
                part.measures[measure_id] = Measure.Measure()
    if part is not None:
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
    # TODO: refactor so that this is handled in the same way as keys (i.e separate the tags)
    if tag[-1] == "beat-type":
        measure.meter = Meter.Meter(int(content["beats"]), int(content["beat-type"]))
    # TODO: see above
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
    if "print" in tag:
        flags = {"yes":True,"no":False}
        if "print" in attrib:
            if "new-system" in attrib["print"]:
                measure.newSystem = flags[attrib["print"]["new-system"]]
            if "new-page" in attrib["print"]:
                measure.newPage = flags[attrib["print"]["new-page"]]


def CheckID(tag, attrs, string, id_name):
    if string in tag:
        return attrs[string][id_name]


def CreateNote(tag, attrs, content, piece):
    global note_id, note, part_id, measure_id
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


def SetupFormat(tags, attrs, text, piece):
    return None


def HandlePitch(tags, attrs, text, piece):
    if "pitch" in tags:
        if not hasattr(note, "pitch"):
            note.pitch = Note.Pitch()
    if tags[-1] == "step":
        note.pitch.step = text["step"]
    if tags[-1] == "alter":
        note.pitch.accidental = text["alter"]
    if tags[-1] == "octave":
        note.pitch.octave = text["octave"]

def HandleDirections(tags, attrs, chars, piece):
    measure = piece.Parts[part_id].measures[measure_id]
    placement = None
    if "direction" in tags:
        if "direction" in attrs:
            attribs = attrs["direction"]
            if "placement" in attribs:
                placement = attribs["placement"]
    if tags[-1] == "words":
        attribs = attrs["words"]
        if "font-size" in attribs:
            if "font-family" in attribs:
                direction = text.Direction(placement=placement,size=attribs["font-size"],text=chars["words"],font=attribs["font-family"])
                measure.directions.append(direction)
            else:
                direction = text.Direction(placement=placement,size=attribs["font-size"],text=chars["words"])
                measure.directions.append(direction)
        else:
            direction = text.Direction(placement=placement,text=chars["words"])
            measure.directions.append(direction)
    if "metronome" in tags:
        attribs = attrs["metronome"]
        if tags[-1] == "beat-unit":
            unit = chars["beat-unit"]
            metronome = text.Metronome(placement=placement,beat=unit)

            metronome.text = str(metronome.beat)
            if "font-family" in attribs:
                metronome.font = attribs["font-family"]
            if "font-size" in attribs:
                metronome.size = attribs["font-size"]
            if "parentheses" in attribs:
                metronome.parentheses = attribs["parentheses"]

            measure.directions.append(metronome)
        if tags[-1] == "per-minute":
            pm = chars["per-minute"]
            metronome = measure.directions[-1]
            metronome.min = pm
            metronome.text += " = " + metronome.min
            if "font-family" in attribs:
                metronome.font = attribs["font-family"]
            if "font-size" in attribs:
                metronome.size = 6.1
            if "parentheses" in attribs:
                metronome.parentheses = attribs["parentheses"]

    if tags[-2] == "dynamics":
        dynamic = text.Dynamic(placement=placement, mark=tags[-1])
        measure.directions.append(dynamic)
    if "sound" in tags:
        if "dynamics" in attrs:
            measure.volume = attrs["dynamics"]
        if "tempo" in attrs:
            measure.tempo = attrs["tempo"]

def CheckDynamics(tag):
    # TODO: modify so that "fm/pm" is an invalid dynamic mark
    dmark = ["p","f","m"]
    for char in tag:
        if char not in dmark:
            return False
    return True


