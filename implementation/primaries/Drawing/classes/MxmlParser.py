import xml.sax
from xml.sax import make_parser, handler
from implementation.primaries.Drawing.classes import Exceptions, Mark, Ornaments, Piece, Part, Harmony, Measure, Meta, Key, Meter, Note, Clef, Directions

note = None
degree = None
frame_note = None
cached_clef = None
measure_cached = None
stave = 1
last_note = 0
items = {}
notes = {}
expressions = {}
staff_id = 1


def GetID(attrs, tag, val):
    if tag in attrs:
        if val in attrs[tag]:
            return attrs[tag][val]
    return None

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
        self.structure = {"movement-title": SetupPiece, "credit-words": SetupPiece, "creator": SetupPiece, "defaults": SetupFormat, "part": UpdatePart,
             "score-part": UpdatePart, "measure": HandleMeasures, "note": CreateNote,
             "pitch":  HandlePitch, "unpitched": HandlePitch,"articulations":handleArticulation,
             "fermata": HandleFermata, "slur":handleOtherNotations, "lyric":handleLyrics,
             "technical": handleOtherNotations}
        # not sure this is needed anymore, but tags which we shouldn't clear the previous data for should be added here
        self.multiple_attribs = ["beats", "sign"]
        # any tags which close instantly in here
        self.closed_tags = ["technical","tie","dot","chord","note","measure","part",
                            "score-part","sound","print","rest","slur",
                            "accent","strong-accent","staccato",
                            "staccatissimo","up-bow","down-bow",
                            "cue","grace"]
        self.end_tag = ["tremolo"]
        self.piece = Piece.Piece()
        self.d = False

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
            self.d = CheckDynamics(name)
            if self.d and "dynamics" in self.tags:
                self.handler(self.tags, self.attribs, self.chars, self.piece)
            if name in self.closed_tags and self.handler is not None:
                self.handler(self.tags, self.attribs, self.chars, self.piece)
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




    def EndTag(self, name):
        global note, degree, frame_note, cached_clef, staff_id, last_note, notes, expressions, items
        if self.handler is not None and not self.d:
            self.handler(self.tags, self.attribs, self.chars, self.piece)
        if name in self.tags:
            if len(self.tags) > 1:
                key = len(self.tags) - 2
                self.handler = None
                while key >= 0:
                    if self.tags[key] in self.structure:
                        self.handler = self.structure[self.tags[key]]
                        break
                    key -= 1

            else:
                self.handler = None
        if name in self.tags:
            self.tags.remove(name)
        if name == "measure":
            part = self.piece.Parts[self.attribs["part"]["id"]]
            measure = part.measures[int(self.attribs["measure"]["number"])]
            #handle items
            measure.items.update(items)
            #handle expressions
            measure.expressions.update(expressions)
            #handle notes
            measure.notes.update(notes)
            #reset all the things
            staff_id = 1
            last_note = 0
            expressions = {}
            notes = {}
            items = {}

        if name == "measure" and self.attribs["measure"]["number"] != measure_cached:
            current_measure = self.piece.Parts[self.attribs["part"]["id"]].measures[int(self.attribs["measure"]["number"])]
            if not hasattr(current_measure, "clef"):
                current_measure.clef = cached_clef
                cached_clef = None
        if name in self.attribs:
            self.attribs.pop(name)
        if name in self.chars:
            self.chars.pop(name)

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
        parser.setContentHandler(Extractor(self))
        # OFFLINE MODE
        parser.setFeature(handler.feature_external_ges, False)
        fob = open(file, 'r')
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
    return_val = None
    if content is not [] and len(tag) > 0:
        title = None
        composer = None
        if tag[-1] == "movement-title":
            return_val = 1
            if "movement-title" in content:
                title = content["movement-title"]
        if tag[-1] == "creator":
            return_val = 1
            if "creator" in attrib:
                if "type" in attrib["creator"]:
                    if attrib["creator"]["type"] == "composer":
                        if "creator" in content:
                            composer = content["creator"]
        if tag[-1] == "movement-title" or "creator":
            if not hasattr(piece, "meta"):
                piece.meta = Meta.Meta(composer=composer, title=title)
            else:
                if not hasattr(piece.meta, "composer"):
                    piece.meta.composer = composer
                if not hasattr(piece.meta, "title"):
                    piece.meta.title = title
        if "credit" in tag:
            page = 0
            if "credit" in attrib:
                if "page" in attrib["credit"]:
                    page = int(attrib["credit"]["page"])
            if tag[-1] == "credit-words":
                x = None
                y = None
                size = None
                justify = None
                valign = None
                text = None
                if "credit-words" in attrib:
                    temp = attrib["credit-words"]

                    if "default-x" in temp:
                        x = float(temp["default-x"])
                    if "default-y" in temp:
                        y = float(temp["default-y"])
                    if "font-size" in temp:
                        size = float(temp["font-size"])
                    if "justify" in temp:
                        justify = temp["justify"]
                    if "valign" in temp:
                        valign = temp["valign"]
                if "credit-words" in content:
                    text = content["credit-words"]
                credit = Directions.CreditText(page=page, x=x,y=y,size=size,justify=justify,valign=valign,text=text)
                if not hasattr(piece, "meta"):
                    piece.meta = Meta.Meta()
                if not hasattr(piece.meta, "credits"):
                    piece.meta.credits = []
                piece.meta.credits.append(credit)
    return return_val


def UpdatePart(tag, attrib, content, piece):
    part_id = GetID(attrib, "part", "id")
    if part_id is None:
        part_id = GetID(attrib, "score-part", "id")
    return_val = None
    if len(tag) > 0:
        if "score-part" in tag:
            if part_id is None:
                raise(Exceptions.NoScorePartException("ERROR IN UPDATEPART: no score-part id found"))
            elif part_id not in piece.Parts:
                piece.Parts[part_id] = Part.Part()
                return_val = 1
            if "part-name" in tag:
                if "part-name" in content and part_id is not None:
                    piece.Parts[part_id].name = content["part-name"]
                    return_val = 1
    return return_val

def handleArticulation(tag, attrs, content, piece):
    global note
    if len(tag) > 0:
        if "articulations" in tag:
            if note is not None:
                accent = None
                if tag[-1] == "accent":
                    accent = Mark.Accent()
                if tag[-1] == "strong-accent":
                    type = ""
                    if "strong-accent" in attrs:
                        if "type" in attrs["strong-accent"]:
                            type = attrs["strong-accent"]["type"]
                    accent = Mark.StrongAccent(type=type)
                if tag[-1] == "staccato":
                    accent = Mark.Staccato()
                if tag[-1] == "staccatissimo":
                    accent = Mark.Staccatissimo()
                if tag[-1] == "detached-legato":
                    accent = Mark.DetachedLegato()
                if tag[-1] == "tenuto":
                    accent = Mark.Tenuto()
                if "placement" in attrs:
                    accent.placement = attrs["placement"]
                if accent is not None:
                    note.addNotation(accent)
                if tag[-1] == "breath-mark":
                    note.addNotation(Mark.BreathMark())
                if tag[-1] == "caesura":
                    note.addNotation(Mark.Caesura())
            return 1
    return None

def HandleFermata(tags, attrs, chars, piece):
    global note
    if "fermata" in tags:
        type = None
        symbol = None
        if "fermata" in attrs:
            if "type" in attrs["fermata"]:
                type = attrs["fermata"]["type"]
        if "fermata" in chars:
            symbol = chars["fermata"]
        fermata = Mark.Fermata(type=type, symbol=symbol)
        note.addNotation(fermata)
    return None

def handleOtherNotations(tag, attrs, content, piece):
    global note
    if len(tag) > 0:
        if "notations" in tag:
            if tag[-1] == "slur":
                if not hasattr(note, "slurs"):
                    note.slurs = {}

                notation = Directions.Slur()
                id = len(note.slurs)
                if "placement" in attrs:
                    notation.placement = attrs["placement"]
                if "number" in attrs:
                    id = int(attrs["number"])

                if "type" in attrs:
                    notation.type = attrs["type"]
                note.slurs[id] = notation
            if tag[-2] == "technical":
                text = None
                if tag[-1] in content:
                    text = content[tag[-1]]
                note.addNotation(Mark.Technique(type=tag[-1], symbol=text))

            return 1
    return None

def HandleMeasures(tag, attrib, content, piece):
    global cached_clef, measure_cached, items, notes, expressions, staff_id
    part_id = GetID(attrib, "part", "id")
    measure_id = GetID(attrib, "measure", "number")
    if measure_id is not None:
        measure_id = int(measure_id)
    part = None
    return_val = None
    global degree
    if len(tag) > 0 and "measure" in tag:
        if part_id is None:
            raise(Exceptions.NoScorePartException())
        if part_id is not None:
            if part_id in piece.Parts:
                part = piece.Parts[part_id]
            else:
                raise(Exceptions.NoPartCreatedException())
        if part is not None:
            if measure_id not in part.measures:
                if measure_id is None:
                    raise(Exceptions.NoMeasureIDException())
                else:
                    part.measures[measure_id] = Measure.Measure()
                if "width" in attrib:
                    part.measures[measure_id] = Measure.Measure(width=attrib["width"])
                else:
                    part.measures[measure_id] = Measure.Measure()
                    return_val = 1
        measure = None
        if part is not None:
            measure = part.measures[measure_id]

        if tag[-1] == "staves":
            staves = int(content["staves"])
            for i in range(staves):
                measure.items[i+1] = {}
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
        clef = None

        if "clef" in tag:

            # this section covers duplication: it's possible a measure
            # can have 2 clefs, the second of which should be in the next measure
            # so we cache this one and wait until the next measure is opened
            if len(items) > 0:
                if cached_clef is not None:
                    # if we've moved to a new measure...
                    if measure_cached != attrib["measure"]["number"]:
                        if not hasattr(measure, "clef"):
                            # and it doesn't have a clef, empty the cache into it
                            measure.clef = cached_clef
                            cached_clef = None
                            measure_cached = None
                        else:
                            # else, the clefs are the same, so reset the clef cache
                            cached_clef = Clef.Clef()
                            clef = cached_clef
                            measure_cached = attrib["measure"]["number"]
                    else:
                        # otherwise, still filling up the cache
                        clef = cached_clef
                if cached_clef is None:
                    cached_clef = Clef.Clef()
                    clef = cached_clef
                    measure_cached = attrib["measure"]["number"]
            else:
                # if we're at the beginning of the measure,
                # clef to fill up is the current measure's clef
                if hasattr(measure, "clef"):
                    clef = measure.clef
                else:
                    measure.clef = Clef.Clef()
                    clef = measure.clef



        if tag[-1] == "sign" and "clef" in tag:
            try:
                clef.sign = content["sign"]
            except Exception:
                print(attrib["measure"]["number"])
                print(measure_cached)
        if tag[-1] == "line" and "clef" in tag and "line" in content:
            clef.line = int(content["line"])
            return_val = 1
        if tag[-1] == "clef-octave-change" and "clef" in tag:
            clef.octave_change = int(content["clef-octave-change"])
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
            if "staff" in tag:
                staff_id = content["staff"]
            if staff_id not in items:
                items[staff_id] = {}
            if last_note not in items[staff_id]:
                items[staff_id][last_note] = []
            root = None
            kind = None
            bass = None
            if len(items[staff_id][last_note]) > 0:
                if items[staff_id][last_note][-1] is not Harmony.Harmony:
                    harmony = Harmony.Harmony(kind=kind)
                    items[staff_id][last_note].append(harmony)
                else:
                    harmony = items[staff_id][last_note][-1]
            else:
                harmony = Harmony.Harmony(kind=kind)
                items[staff_id][last_note].append(harmony)


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

                    if "string" in tag and "string" in content:
                        frame_note.string = content["string"]
                        harmony.frame.notes[int(content["string"])] = frame_note
                    if "fret" in tag and "fret" in content:
                        frame_note.fret = content["fret"]
                    if "barre" in tag and "barre" in attrib:
                        frame_note.barre = attrib["barre"]["type"]
                    if "fingering" in tag and "fingering" in content:
                        frame_note.fingering = content["fingering"]
    handleBarline(tag, attrib, content, piece)
    HandleDirections(tag, attrib, content, piece)
    handleArticulation(tag, attrib, content, piece)
    return return_val

def handleBarline(tag, attrib, content, piece):
    part_id = GetID(attrib, "part", "id")
    measure_id = GetID(attrib, "measure", "number")
    measure = None
    if measure_id is not None:
        measure_id = int(measure_id)
    if part_id is not None and measure_id is not None:
        measure = piece.Parts[part_id].measures[measure_id]
    if "barline" in tag and measure is not None:
        if not hasattr(measure, "barlines"):
            measure.barlines = {}
        barline = None
        style = None
        repeat = None
        ending = None
        if tag[-1] == "ending":
            btype = None
            number = None
            if "ending" in attrib:
                if "number" in attrib["ending"]:
                    if attrib["barline"]["location"] not in measure.barlines or not hasattr(measure.barlines[attrib["barline"]["location"]], "ending"):
                        number = int(attrib["ending"]["number"])
                    else:
                        measure.barlines[attrib["barline"]["location"]].ending.number = int(attrib["ending"]["number"])
                if "type" in attrib["ending"]:
                    if attrib["barline"]["location"] not in measure.barlines or not hasattr(measure.barlines[attrib["barline"]["location"]], "ending"):
                        btype = attrib["ending"]["type"]
                    else:
                        measure.barlines[attrib["barline"]["location"]].ending.type = attrib["ending"]["type"]

            ending = Measure.EndingMark(type=btype, number=number)

            if attrib["barline"]["location"] in measure.barlines:
                measure.barlines[attrib["barline"]["location"]].ending = ending

        if tag[-1] == "bar-style":
                if attrib["barline"]["location"] not in measure.barlines:
                    style = content["bar-style"]
                else:
                    measure.barlines[attrib["barline"]["location"]].style = style
        if tag[-1] == "repeat":
            if "repeat" in attrib:
                if "direction" in attrib["repeat"]:
                    if attrib["barline"]["location"] not in measure.barlines:
                        repeat = attrib["repeat"]["direction"]
                    else:
                        measure.barlines[attrib["barline"]["location"]].repeat = attrib["repeat"]["direction"]
        if attrib["barline"]["location"] not in measure.barlines:
            if barline is None:
                barline = Measure.Barline(style=style, repeat=repeat, ending=ending)
            measure.barlines[attrib["barline"]["location"]] = barline
def CheckID(tag, attrs, string, id_name):
    if string in tag:
        return attrs[string][id_name]


def CreateNote(tag, attrs, content, piece):
    global note, item_list, staff_id, notes, last_note
    part_id = None
    measure_id = None
    ret_value = None
    measure = None

    if len(tag) > 0 and "note" in tag:
        if tag[-1] == "staff":
            staff_id = int(content["staff"])
        if "part" in attrs:
            if "id" in attrs["part"]:
                part_id = attrs["part"]["id"]
        if "measure" in attrs:
            if "number" in attrs["measure"]:
                measure_id = int(attrs["measure"]["number"])
        if part_id is not None and measure_id is not None:
            measure = piece.Parts[part_id].measures[measure_id]
        if "note" in tag and note is None:
            if staff_id not in notes:
                notes[staff_id] = []
            note = Note.Note()
            notes[staff_id].append(note)
            last_note = len(notes[staff_id])-1
            ret_value = 1

        if "rest" in tag:
            note.rest = True
        if "cue" in tag:
            note.cue = True

        if "grace" in tag:
            slash = False
            if "grace" in attrs:
                if "slash" in attrs["grace"]:
                    slash = YesNoToBool(attrs["grace"]["slash"])
            note.grace = Note.GraceNote(slash=slash)
        if tag[-1] == "duration" and "note" in tag:
            note.duration = float(content["duration"])
            if hasattr(measure, "divisions"):
                if measure.divisions is not None:
                    note.divisions = float(measure.divisions)

        if "dot" in tag:
            note.dotted = True
        if "tie" in tag:
            note.ties.append(Note.Tie(attrs["tie"]["type"]))
        if "chord" in tag:
            note.chord = True
        if tag[-1] == "stem":
            note.stem = Note.Stem(content["stem"])


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


        if tag[-1] == "accidental":
            if not hasattr(note, "pitch"):
                note.pitch = Note.Pitch()
                if "accidental" in content:
                    note.pitch.accidental = content["accidental"]

            else:
                if "accidental" in content:
                    note.pitch.accidental = content["accidental"]
    HandleNoteheads(tag, attrs, content, piece)
    HandleArpeggiates(tag, attrs, content, piece)
    HandleSlidesAndGliss(tag, attrs, content, piece)
    handleLyrics(tag, attrs, content, piece)
    handleOrnaments(tag, attrs, content, piece)
    handleOtherNotations(tag, attrs, content, piece)
    handleTimeMod(tag, attrs, content, piece)
    return ret_value

def HandleNoteheads(tags, attrs, content, piece):
    if "note" in tags:
        if tags[-1] == "notehead":
            note.notehead = Note.Notehead()
            if "notehead" in attrs:
                if "filled" in attrs["notehead"]:
                    filled = YesNoToBool(attrs["notehead"]["filled"])
                    note.notehead.filled = filled
            if "notehead" in content:
                note.notehead.type = content["notehead"]
def HandleArpeggiates(tags, attrs, content, piece):
    if len(tags) > 0:
        if tags[-1] == "arpeggiate":
            direction = None
            if "arpeggiate" in attrs:
                if "direction" in attrs["arpeggiate"]:
                    direction = attrs["arpeggiate"]["direction"]
            arpegg = Note.Arpeggiate(direction=direction)
            note.addNotation(arpegg)
        if tags[-1] == "non-arpeggiate":
            type = None
            if "non-arpeggiate" in attrs:
                if "type" in attrs["non-arpeggiate"]:
                    type = attrs["non-arpeggiate"]["type"]
            narpegg = Note.NonArpeggiate(type=type)
            note.addNotation(narpegg)

def HandleSlidesAndGliss(tags, attrs, content, piece):
    type = None
    number = None
    lineType = None
    if "slide" in tags or "glissando" in tags:
        if tags[-1] in attrs:
            if "type" in attrs[tags[-1]]:
                type = attrs[tags[-1]]["type"]
            if "line-type" in attrs[tags[-1]]:
                lineType = attrs[tags[-1]]["line-type"]
            if "number" in attrs[tags[-1]]:
                number = int(attrs[tags[-1]]["number"])
    if "slide" in tags:
        slide = Note.Slide(type=type, lineType=lineType, number=number)
        note.addNotation(slide)
    if "glissando" in tags:
        gliss = Note.Glissando(type=type, lineType=lineType, number=number)
        note.addNotation(gliss)

def handleOrnaments(tags, attrs, content, piece):
    global note
    if "ornaments" in tags:
        if tags[-1] == "inverted-mordent":
            note.addNotation(Ornaments.InvertedMordent())
        if tags[-1] == "mordent":
            note.addNotation(Ornaments.Mordent())
        if tags[-1] == "trill-mark":
            note.addNotation(Ornaments.Trill())
        if tags[-1] == "turn":
            note.addNotation(Ornaments.Turn())
        if tags[-1] == "inverted-turn":
            note.addNotation(Ornaments.InvertedTurn())
        if tags[-1] == "tremolo":
            type = None
            value = None
            if "tremolo" in attrs:
                if "type" in attrs["tremolo"]:
                    type = attrs["tremolo"]["type"]
            if "tremolo" in content:
                value = int(content["tremolo"])
            note.addNotation(Ornaments.Tremolo(type=type, value=value))

def SetupFormat(tags, attrs, text, piece):
    return None


def HandlePitch(tags, attrs, text, piece):
    return_val = None
    if len(tags) > 0:
        if "pitch" or "unpitched" in tags:
            if not hasattr(note, "pitch") and note is not None:
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
                note.pitch.alter = text["alter"]
                return_val = 1
            if "octave" in tags[-1]:
                if "octave" not in text:
                    note.pitch.octave = text["display-octave"]
                else:
                    note.pitch.octave = text["octave"]
                return_val = 1
    return return_val

def HandleDirections(tags, attrs, chars, piece):
    global expressions, items, staff_id
    return_val = None
    direction = None
    dynamic = None
    if len(tags) == 0:
        return None

    if "direction" in tags:
        measure_id = GetID(attrs, "measure", "number")
        if measure_id is not None:
            measure_id = int(measure_id)
        part_id = GetID(attrs, "part", "id")
        measure = None
        if measure_id is not None and part_id is not None:
            measure = piece.Parts[part_id].measures[measure_id]
        placement = None
        if measure is None:
            return None
        if tags[-1] == "staff":
            staff_id = int(chars["staff"])
            if staff_id not in items:
                items[staff_id] = {}
            if staff_id not in expressions:
                expressions[staff_id] = {}
        if "direction" in attrs:
            if "placement" in attrs["direction"]:
                placement = attrs["direction"]["placement"]

        if tags[-1] == "words":
            return_val = 1

            size = None
            font = None
            text = None
            if "words" in chars:
                text = chars["words"]

            if "words" in attrs:
                if "font-size" in attrs["words"]:
                    size = attrs["words"]["font-size"]
                if "font-family" in attrs["words"]:
                    font = attrs["words"]["font-family"]
            direction = Directions.Direction(font=font,text=text,size=size,placement=placement)

        if tags[-1] == "rehearsal":
            return_val = 1

            size = None
            font = None
            text = chars["rehearsal"]

            if "words" in attrs:
                if "font-size" in attrs["words"]:
                    size = attrs["words"]["font-size"]
                if "font-family" in attrs["words"]:
                    font = attrs["words"]["font-family"]
            direction = Directions.RehearsalMark(font=font,text=text,size=size,placement=placement)
        if "metronome" in tags:
            if tags[-1] == "beat-unit":
                return_val = 1
                unit = chars["beat-unit"]
                direction = Directions.Metronome(placement=placement,beat=unit)

                direction.text = str(direction.beat)
                if "metronome" in attrs:
                    if "font-family" in attrs["metronome"]:
                        direction.font = attrs["metronome"]["font-family"]
                    if "font-size" in attrs["metronome"]:
                        direction.size = attrs["metronome"]["font-size"]
                    if "parentheses" in attrs["metronome"]:
                        direction.parentheses = YesNoToBool(attrs["metronome"]["parentheses"])
            if tags[-1] == "per-minute":
                return_val = 1
                pm = chars["per-minute"]
                if len(items) > 0:
                    if type(items[staff_id][last_note][-1]) is Directions.Metronome:
                        direction = items[staff_id][last_note][-1]
                    else:
                        direction = Directions.Metronome(min=pm)

                else:
                    direction = Directions.Metronome(min=pm)
                direction.min = pm
                direction.text += " = " + direction.min
                if "metronome" in attrs:
                    if "font-family" in attrs["metronome"]:
                        direction.font = attrs["metronome"]["font-family"]
                    if "font-size" in attrs["metronome"]:
                        direction.size = float(attrs["metronome"]["font-size"])
                    if "parentheses" in attrs["metronome"]:
                        direction.parentheses = YesNoToBool(attrs["metronome"]["parentheses"])
        if tags[-1] == "wedge":
            w_type = None
            if "wedge" in attrs:
                if "type" in attrs["wedge"]:
                    w_type = attrs["wedge"]["type"]
            dynamic = Directions.Wedge(placement = placement,type=w_type)

        if len(tags) > 1:
            if tags[-2] == "dynamics":
                dynamic = Directions.Dynamic(placement=placement, mark=tags[-1])
        if "sound" in tags:
            return_val = 1
            if "sound" in attrs:
                if "dynamics" in attrs["sound"]:
                    measure.volume = attrs["sound"]["dynamics"]
                if "tempo" in attrs["sound"]:
                    measure.tempo = attrs["sound"]["tempo"]
        l_type = None
        if tags[-1] in ["wavy-line","octave-shift","pedal","bracket"]:
            if tags[-1] in attrs:
                if "type" in attrs[tags[-1]]:
                    l_type = attrs[tags[-1]]["type"]
        if "octave-shift" in tags:
            amount = None
            font = None
            if "octave-shift" in attrs:
                if "size" in attrs["octave-shift"]:
                    amount = int(attrs["octave-shift"]["size"])
                if "font" in attrs["octave-shift"]:
                    font = attrs["octave-shift"]["font"]
            direction = Directions.OctaveShift(type=l_type, amount=amount, font=font)


        if tags[-1] == "wavy-line":
            direction = Directions.WavyLine(type=l_type)
        if tags[-1] == "pedal":
            line = None
            if "pedal" in attrs:
                if "line" in attrs["pedal"]:
                    line = YesNoToBool(attrs["pedal"]["line"])
            direction = Directions.Pedal(line=line, type=l_type)
        if tags[-1] == "bracket":
            num = None
            ltype = None
            elength=None
            lineend=None
            if "bracket" in attrs:
                if "number" in attrs["bracket"]:
                    num = int(attrs["bracket"]["number"])
                if "line-type" in attrs["bracket"]:
                    ltype = attrs["bracket"]["line-type"]
                if "end-length" in attrs["bracket"]:
                    elength = int(attrs["bracket"]["end-length"])
                if "line-end" in attrs["bracket"]:
                    lineend = attrs["bracket"]["line-end"]
            direction = Directions.Bracket(lineEnd=lineend, elength=elength, type=l_type, ltype=ltype, number=num)

    if direction is not None:
        if staff_id not in items:
            items[staff_id] = {}
        if last_note not in items[staff_id]:
            items[staff_id][last_note] = []
        items[staff_id][last_note].append(direction)
    if dynamic is not None:
        if staff_id not in expressions:
            expressions[staff_id] = {}

        if last_note not in expressions[staff_id]:
            expressions[staff_id][last_note] = []
        expressions[staff_id][last_note].append(dynamic)
    HandleRepeatMarking(tags, attrs, chars, piece)

    return return_val

def HandleRepeatMarking(tags, attrs, chars, piece):
    global staff_id, last_note, items
    direction = None
    if "direction" in tags or "forward" in tags:
        measure = None
        part_id = GetID(attrs, "part", "id")
        measure_id = GetID(attrs, "measure", "number")
        if measure_id is not None:
            measure_id = int(measure_id)
        if part_id is not None:
            if measure_id is not None:
                measure = piece.Parts[part_id].measures[measure_id]

        if measure is not None:
            d_type = None
            if "forward" in tags:
                duration = None
                if tags[-1] == "duration":
                    duration = int(chars["duration"])
                measure.forwards[last_note] = Directions.Forward(duration=duration)
            if tags[-1] == "segno" or tags[-1] == "coda":
                d_type = tags[-1]
                direction = Directions.RepeatSign(type=d_type)

            if tags[-1] == "sound":
                if "sound" in attrs:
                    if "coda" in attrs["sound"]:
                        measure.coda = attrs["sound"]["coda"]
                    if "dacapo" in attrs["sound"]:
                        measure.dacapo = YesNoToBool(attrs["sound"]["dacapo"])
                    if "dalsegno" in attrs["sound"]:
                        measure.dalsegno = attrs["sound"]["dalsegno"]
                    if "fine" in attrs["sound"]:
                        measure.fine = YesNoToBool(attrs["sound"]["fine"])
                    if "segno" in attrs["sound"]:
                        measure.segno = attrs["sound"]["segno"]
                    if "tocoda" in attrs["sound"]:
                        measure.tocoda = attrs["sound"]["tocoda"]
    if direction is not None:
        if staff_id not in items:
            items[staff_id] = {}
        if last_note not in items[staff_id]:
            items[staff_id][last_note] = []
        items[staff_id][last_note].append(direction)



def handleLyrics(tags, attrs, chars, piece):
    global note
    if "lyric" in tags:
        if not hasattr(note, "lyrics"):
            note.lyrics = {}
        number = len(note.lyrics)
        if "lyric" in attrs:
            if "number" in attrs["lyric"]:
                number = int(attrs["lyric"]["number"])
        if number not in note.lyrics:
            note.lyrics[number] = Directions.Lyric()
        if tags[-1] == "text":
            note.lyrics[number].text = chars["text"]
        if tags[-1] == "syllabic":
            note.lyrics[number].syllabic = chars["syllabic"]

def handleTimeMod(tags, attrs, chars, piece):
    if "notations" in tags:
        if tags[-1] == "tuplet":
            type = None
            bracket = None

            if "tuplet" in attrs:
                if "type" in attrs["tuplet"]:
                    type = attrs["tuplet"]["type"]
                if "bracket" in attrs["tuplet"]:
                    bracket = YesNoToBool(attrs["tuplet"]["bracket"])
            tuplet = Note.Tuplet(bracket=bracket, type=type)
            note.addNotation(tuplet)
    if "time-modification" in tags:
        if not hasattr(note, "timeMod"):
            note.timeMod = Note.TimeModifier()
        if tags[-1] == "actual-notes":
            note.timeMod.actual = int(chars["actual-notes"])
        if tags[-1] == "normal-notes":
            note.timeMod.normal = int(chars["normal-notes"])
    return None

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



