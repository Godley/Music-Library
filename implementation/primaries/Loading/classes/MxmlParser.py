import xml.sax
from xml.sax import make_parser
from implementation.primaries.Loading.classes import Piece, Part, Harmony, Measure, Meta, Key, Meter, Note, Clef, text

note = None
part_id = None
measure_id = None
degree = None
frame_note = None


class MxmlParser(object):
    """this needs a huge tidy, but this class:
        sets up a few things that define where the tags get handled
        runs sax, which calls the parent methods according to what's happened
        the parent methods call the handlers defined in structure, or else figure out what handler to use. If there absolutely isn't one, nothing gets called
        spits out a piece class holding all this info.
    """
    def __init__(self, excluded=[]):
        self.tags = []
        self.chars = {}
        self.attribs = {}
        self.handler = None
        self.excluded = excluded

        # add any handlers, along with the tagname associated with it, to this dictionary
        self.structure = {"movement-title": SetupPiece, "creator": SetupPiece, "defaults": SetupFormat, "part": UpdatePart,
             "score-part": UpdatePart, "measure": HandleMeasures, "note": CreateNote,
             "pitch": HandlePitch,"unpitched":HandlePitch,"direction":HandleDirections,"articulations":handleArticulation,"slur":handleOtherNotations,
             "technical":handleOtherNotations}
        # not sure this is needed anymore, but tags which we shouldn't clear the previous data for should be added here
        self.multiple_attribs = ["beats", "sign"]
        # any tags which close instantly in here
        self.closed_tags = ["technical","tie","dot","chord","note","measure","part",
                            "score-part","sound","print","rest","slur",
                            "accent","strong-accent","staccato",
                            "staccatissimo","up-bow","down-bow",
                            "cue","grace","wedge","octave-shift"]
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
            if d and "dynamics" in self.tags:
                self.handler(self.tags, attrs, None, self.piece)
            # handle tags which close immediately, or do not have any text content
            if name in self.closed_tags:
                self.handler(self.tags, attrs, None, self.piece)

    def validateData(self, text):
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

        if self.validateData(text):
            if len(self.tags) > 0:
                self.chars[self.tags[-1]] = text
            if self.handler is not None:
                self.handler(self.tags, self.attribs, self.chars, self.piece)



    def EndTag(self, name):
        global part_id, measure_id, note, degree, frame_note
        self.tags.remove(name)
        if name in self.attribs:
            self.attribs.pop(name)
        if name in self.chars:
            self.chars.pop(name)
        if len(self.tags) > 0:
            if self.tags[-1] in self.structure:
                self.handler = self.structure[self.tags[-1]]
            else:
                self.handler = None
        else:
            self.handler = None
        if name == "measure":
            measure_id = None
        if name == "part" or name == "score-part":
            part_id = None
        if name == "note":
            note = None
        if name == "degree":
            degree = None
        if name == "frame-note":
            frame_note = None

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
        fob = open(file, 'r')
        parser.setContentHandler(Extractor(self))
        parser.parse(fob)
        return self.piece

def YesNoToBool(entry):
    if entry == "yes":
        return True
    if entry == "no":
        return False

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
    if content is not [] and len(tag) > 0:
        if not hasattr(piece, "meta"):
            if tag[-1] == "creator" and attrib["creator"]["type"] == "composer":
                piece.meta = Meta.Meta(composer=content["creator"])
                return 1
            elif tag[-1] == "movement-title":
                piece.meta = Meta.Meta(title=content["movement-title"])
                return 1
        elif tag[-1] == "movement-title":
            piece.meta.title = content["movement-title"]
            return 1
        elif tag[-1] == "creator" and attrib["creator"]["type"] == "composer":
            piece.meta.composer = content["creator"]
            return 1
    return None


def UpdatePart(tag, attrib, content, piece):
    global measure_id, part_id
    return_val = None
    if len(tag) > 0:
        if "score-part" in tag:
            if part_id not in piece.Parts.keys():
                part_id = attrib["id"]
                piece.Parts[part_id] = Part.Part()
                return_val = 1
        if "part" in tag:
            if "id" in attrib:
                part_id = attrib["id"]
                if part_id not in piece.Parts:
                    print("whoops")
        if part_id is not None:
            part = piece.Parts[part_id]
        if "part-name" in tag:
            if "part-name" in content:
                part.name = content["part-name"]
                return_val = 1
    return return_val

def handleArticulation(tag, attrs, content, piece):
    global note
    if len(tag) > 0:
        if "articulation" in tag:
            if note is not None:
                accent = None
                if not hasattr(note, "articulations"):
                    note.notations = []
                if tag[-1] == "accent":
                    accent = Note.Accent()
                if tag[-1] == "strong-accent":
                    type = ""
                    if "type" in attrs:
                        type = attrs["type"]
                    accent = Note.StrongAccent(type=type)
                if tag[-1] == "staccato":
                    accent = Note.Staccato()
                if tag[-1] == "staccatissimo":
                    accent = Note.Staccatissimo()
                if "placement" in attrs:
                    accent.placement = attrs["placement"]
                if accent is not None:
                    note.notations.append(accent)

            return 1

    return None

def handleOtherNotations(tag, attrs, content, piece):
    global note
    if len(tag) > 0:
        if "notations" in tag:
            if tag[-1] == "slur":
                if not hasattr(note, "slurs"):
                    note.slurs = {}

                notation = text.Slur()
                id = len(note.slurs)
                if "placement" in attrs:
                    notation.placement = attrs["placement"]
                if "number" in attrs:
                    id = int(attrs["number"])

                if "type" in attrs:
                    notation.type = attrs["type"]
                note.slurs[id] = notation
            if tag[-2] == "technical":
                if not hasattr(note, "techniques"):
                    note.techniques = []
                note.techniques.append(text.Technique(type=tag[-1]))
            return 1
    return None

def HandleMeasures(tag, attrib, content, piece):
    global measure_id, part_id
    part = None
    return_val = None
    global degree
    if len(tag) > 0 and "measure" in tag:
        if part_id is not None:
            part = piece.Parts[part_id]
        if part is not None:
            if measure_id not in part.measures:
                # attrib here only references the index it needs, as measure has no text content so calls its handler in the starttag method
                measure_id = int(attrib["number"])
                if "width" in attrib:
                    part.measures[measure_id] = Measure.Measure(width=attrib["width"])
                else:
                    part.measures[measure_id] = Measure.Measure()
                    return_val = 1
        measure = None
        if part is not None and "measure" in tag:
            measure = part.measures[measure_id]
        if tag[-1] == "divisions" and measure is not None:
            measure.divisions = int(content["divisions"])
            return_val = 1
        if tag[-1] == "mode" and "key" in tag and measure is not None:
            if hasattr(measure, "key"):
                measure.key.mode = content["mode"]

            else:
                measure.key = Key.Key(mode=content["mode"])
            return_val = 1
        if tag[-1] == "fifths" and "key" in tag:
            if hasattr(measure, "key"):
                measure.key.fifths = content["fifths"]
            else:
                measure.key = Key.Key(fifths=int(content["fifths"]))
            return_val = 1

        if tag[-1] == "beats" and "meter" in tag:
            if hasattr(measure, "meter"):
                measure.meter.beats = int(content["beats"])
            else:
                measure.meter = Meter.Meter(beats=int(content["beats"]))
            return_val = 1
        if tag[-1] == "beat-type" and "meter" in tag:
            if hasattr(measure, "meter"):
                measure.meter.type= int(content["beat-type"])
            else:
                measure.meter = Meter.Meter(type=int(content["beat-type"]))
            return_val = 1

        if tag[-1] == "sign" and "clef" in tag:
            if hasattr(measure, "clef"):
                measure.clef.sign = content["sign"]
            else:
                measure.clef = Clef.Clef(sign=content["sign"])
        if tag[-1] == "line" and "clef" in tag:
            if hasattr(measure, "clef"):
                measure.clef.line = content["line"]
            else:
                measure.clef = Clef.Clef(line=content["line"])
            return_val = 1

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
            return_val = 1
        if "print" in tag:
            if "print" in attrib:
                if "new-system" in attrib["print"]:
                    measure.newSystem = YesNoToBool(attrib["print"]["new-system"])
                if "new-page" in attrib["print"]:
                    measure.newPage = YesNoToBool(attrib["print"]["new-page"])
            return_val = 1

        if "harmony" in tag:
            root = None
            kind = None
            bass = None
            if len(measure.items) > 0:
                if measure.items[-1] is not Harmony.Harmony:
                    harmony = Harmony.Harmony(kind=kind)
                    measure.items.append(harmony)
                else:
                    harmony = measure.items[-1]
            else:
                harmony = Harmony.Harmony(kind=kind)
                measure.items.append(harmony)


            if "root" in tag:
                if not hasattr(harmony, "root"):
                    root = Harmony.harmonyPitch()
                    harmony.root = root
                else:
                    root = harmony.root
                if tag[-1] == "root-step":
                    if "root-step" in content:
                        root.step = content["root-step"]
                if tag[-1] == "root-alter":
                    if "root-alter" in content:
                        root.alter = content["root-alter"]

            if "kind" in tag:
                if not hasattr(harmony, "kind"):
                    kind = Harmony.Kind()
                    harmony.kind = kind
                else:
                    kind = harmony.kind
                if "kind" in content:
                    kind.value = content["kind"]
                if "kind" in attrib:
                    if "text" in attrib["kind"]:
                        kind.text = attrib["kind"]["text"]
                    if "halign" in attrib["kind"]:
                        kind.halign = attrib["kind"]["halign"]
                    if "parenthesis-degrees" in attrib["kind"]:
                        kind.parenthesis = attrib["kind"]["parenthesis-degrees"]


            if "bass" in tag:
                if not hasattr(harmony, "bass"):
                    harmony.bass = Harmony.harmonyPitch()
                if "bass-step" in tag and "bass-step" in content:
                    harmony.bass.step = content["bass-step"]
                if "bass-alter" in tag and "bass-alter" in content:
                    harmony.bass.alter = content["bass-alter"]
            frame = None

            if "degree" in tag:
                if degree is None:
                    degree = Harmony.Degree()
                    harmony.degrees.append(degree)

                if "degree-value" in tag:
                    if "degree-value" in content:
                        degree.value = content["degree-value"]
                if "degree-alter" in tag:
                    if "degree-alter" in content:
                        degree.alter = content["degree-alter"]
                if "degree-type" in tag:
                    if "degree-type" in content:
                        degree.type = content["degree-type"]
                    if "degree-type" in attrib:
                        if "text" in attrib["degree-type"]:
                            degree.display = attrib["degree-type"]["text"]

            if "frame" in tag:
                if not hasattr(harmony, "frame"):
                    harmony.frame = Harmony.Frame()
                if "first-fret" in tag:
                    harmony.frame.firstFret = True
                    if "first-fret" in content:
                        if "first-fret" not in attrib:
                            harmony.frame.firstFret = [content["first-fret"]]
                        else:
                            harmony.frame.firstFret = [content["first-fret"], attrib["first-fret"]["text"]]
                if "frame-strings" in tag and "frame-strings" in content:
                    harmony.frame.strings = content["frame-strings"]
                if "frame-frets" in tag and "frame-frets" in content:
                    harmony.frame.frets = content["frame-frets"]
                if "frame-note" in tag:
                    global frame_note
                    if frame_note is None:
                        frame_note = Harmony.FrameNote()
                        harmony.frame.notes.append(frame_note)
                    if "string" in tag and "string" in content:
                        frame_note.string = content["string"]
                    if "fret" in tag and "fret" in content:
                        frame_note.fret = content["fret"]
                    if "barre" in tag and "barre" in attrib:
                        frame_note.barre = attrib["barre"]["type"]
                    if "fingering" in tag and "fingering" in content:
                        frame_note.fingering = content["fingering"]
    return return_val

def CheckID(tag, attrs, string, id_name):
    if string in tag:
        return attrs[string][id_name]


def CreateNote(tag, attrs, content, piece):
    global note_id, note, part_id, measure_id
    ret_value = None
    if len(tag) > 0 and "note" in tag:
        if part_id is not None and measure_id is not None:
            measure = piece.Parts[part_id].measures[measure_id]
        if "note" in tag and note is None:
            note = Note.Note()
            measure.items.append(note)
            note_id = len(measure.items) - 1
            ret_value = 1

        if "rest" in tag:
            note.rest = True
        if "cue" in tag:
            note.cue = True

        if "grace" in tag:
            note.grace = True
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

        if "notehead" in tag:
            note.notehead = Note.Notehead()
            if "notehead" in attrs:
                if "filled" in attrs["notehead"]:
                    filled = YesNoToBool(attrs["notehead"]["filled"])
                    note.notehead.filled = filled
            if "notehead" in content:
                note.notehead.type = content["notehead"]
        if tag[-1] == "beam":
            type = ""
            if "beam" in content:
                type = content["beam"]
            if not hasattr(note, "beams"):
                note.beams = {}
            if "beam" in attrs:
                id = int(attrs["beam"]["number"])
            else:
                id = len(note.beams)
            note.beams[id] = Note.Beam(type=type)

    return ret_value

def SetupFormat(tags, attrs, text, piece):
    return None


def HandlePitch(tags, attrs, text, piece):
    return_val = None
    if len(tags) > 0:
        if "pitch" or "unpitched" in tags:
            if not hasattr(note, "pitch"):
                note.pitch = Note.Pitch()
            if "unpitched" in tags:
                note.pitch.unpitched = True
            if "step" in tags[-1]:
                if "step" not in text:
                    note.pitch.step = text["display-step"]
                else:
                    note.pitch.step = text["step"]
                return_val = 1
            if tags[-1] == "alter":
                note.pitch.accidental = text["alter"]
                return_val = 1
            if "octave" in tags[-1]:
                if "octave" not in text:
                    note.pitch.octave = text["display-octave"]
                else:
                    note.pitch.octave = text["octave"]
                return_val = 1
    return return_val

def HandleDirections(tags, attrs, chars, piece):
    measure = piece.Parts[part_id].measures[measure_id]
    placement = None
    return_val = None
    if len(tags) == 0:
        return None
    if "direction" in tags:
        if "direction" in attrs:
            if "placement" in attrs["direction"]:
                placement = attrs["direction"]["placement"]
        if tags[-1] == "words":
            return_val = 1

            size = None
            font = None
            chars = chars["words"]

            if "words" in attrs:
                if "font-size" in attrs["words"]:
                    size = attrs["words"]["font-size"]
                if "font-family" in attrs["words"]:
                    font = attrs["words"]["font-family"]
            direction = text.Direction(font=font,text=chars,size=size,placement=placement)
            measure.items.append(direction)
        if "metronome" in tags:
            if tags[-1] == "beat-unit":
                return_val = 1
                unit = chars["beat-unit"]
                metronome = text.Metronome(placement=placement,beat=unit)

                metronome.text = str(metronome.beat)
                if "metronome" in attrs:
                    if "font-family" in attrs["metronome"]:
                        metronome.font = attrs["metronome"]["font-family"]
                    if "font-size" in attrs["metronome"]:
                        metronome.size = attrs["metronome"]["font-size"]
                    if "parentheses" in attrs["metronome"]:
                        metronome.parentheses = YesNoToBool(attrs["metronome"]["parentheses"])

                measure.items.append(metronome)
            if tags[-1] == "per-minute":
                return_val = 1
                pm = chars["per-minute"]
                if len(measure.items) > 0:
                    if type(measure.items[-1]) is text.Metronome:
                        metronome = measure.items[-1]
                    else:
                        metronome = text.Metronome(min=pm)
                        measure.items.append(metronome)
                else:
                    metronome = text.Metronome(min=pm)
                    measure.items.append(metronome)
                metronome.min = pm
                metronome.text += " = " + metronome.min
                if "metronome" in attrs:
                    if "font-family" in attrs["metronome"]:
                        metronome.font = attrs["metronome"]["font-family"]
                    if "font-size" in attrs["metronome"]:
                        metronome.size = float(attrs["metronome"]["font-size"])
                    if "parentheses" in attrs["metronome"]:
                        metronome.parentheses = YesNoToBool(attrs["metronome"]["parentheses"])
        if tags[-1] == "wedge":
            type = None
            if "wedge" in attrs:
                if "type" in attrs["wedge"]:
                    type = attrs["wedge"]["type"]
            dynamic = text.Wedge(placement = placement,type=type)
            measure.items.append(dynamic)
        if len(tags) > 1:
            if tags[-2] == "dynamics":
                dynamic = text.Dynamic(placement=placement, mark=tags[-1])
                measure.items.append(dynamic)
        if "sound" in tags:
            return_val = 1
            if "dynamics" in attrs:
                measure.volume = attrs["dynamics"]
            if "tempo" in attrs:
                measure.tempo = attrs["tempo"]
        if tags[-1] == "offset" and len(measure.items) > 0:
            measure.items[-1].offset = chars["offset"]

        if "octave-shift" in tags:
            type = None
            size = None
            font = None
            if "octave-shift" in attrs:
                if "type" in attrs["octave-shift"]:
                    type = attrs["octave-shift"]["type"]
                if "size" in attrs["octave-shift"]:
                    size = attrs["octave-shift"]["size"]
                if "font" in attrs["octave-shift"]:
                    font = attrs["octave-shift"]["font"]

            measure.items.append(text.OctaveShift(type=type, size=size, font=font))

    return return_val

def CheckDynamics(tag):
    return_val = False
    dmark = ["p","f"]
    if len(tag) == 1 and tag in dmark:
        return_val = True
    elif len(tag) == 2:
        if tag[-1] in dmark:
            if tag[0] == tag[-1] or tag[0] == "m":
                return_val = True
    if len(tag) > 2:
        val = tag[0]
        if val in dmark:
            for char in tag:
                if char == val:
                    return_val = True
                else:
                    return_val = False
    return return_val



