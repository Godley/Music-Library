try:
    from classes import BaseClass
except:
    from implementation.primaries.Drawing.classes import BaseClass
import string, random
class Text(BaseClass.Base):
    def __init__(self, **kwargs):
        BaseClass.Base.__init__(self)
        if "font" in kwargs and kwargs["font"] is not None:
            self.font = kwargs["font"]
        if "size" in kwargs and kwargs["size"] is not None:
            self.size = kwargs["size"]
        if "text" in kwargs and kwargs["text"] is not None:
            self.text = kwargs["text"]
        else:
            self.text = ""

    def get(self):
        ret_list = []
        if hasattr(self, "font"):
            ret_list.append(self.font)
        if hasattr(self, "size"):
            ret_list.append(self.size)
        if hasattr(self, "text"):
            ret_list.append(self.text)
        return ret_list

    def toLily(self):
        # \abs-fontsize #20
        lilystring = ""
        if hasattr(self, "size"):
            lilystring += "\\abs-fontsize #" + str(self.size) + " "
        if hasattr(self, "font"):
            fonts_available = ["sans","typewriter","roman"]
            if self.font in fonts_available:
                lilystring += "\\"+self.font + " "
            else:
                rand = random.Random()
                selected = rand.choice(fonts_available)
                lilystring += "\\"+selected + " "
        valid = False
        for char in self.text:
            if char in string.ascii_letters or char in ["0","1","2","3","4","5","6","7","8","9"]:
                lilystring += "\""+ self.text + "\" "
                valid = True
                break
            else:
                valid = False
        if not valid:
            lilystring = ""
        return lilystring

class CreditText(Text):
    def __init__(self, **kwargs):
        font = None
        size = None
        text = None
        if "font" in kwargs:
            font = kwargs["font"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "x" in kwargs:
            if kwargs["x"] is not None:
                self.x = kwargs["x"]
        if "y" in kwargs:
            if kwargs["y"] is not None:
                self.y = kwargs["y"]
        if "size" in kwargs:
            if kwargs["size"] is not None:
                self.size = kwargs["size"]
        if "justify" in kwargs:
            if kwargs["justify"] is not None:
                self.justify = kwargs["justify"]
        if "valign" in kwargs:
            if kwargs["valign"] is not None:
                self.valign = kwargs["valign"]
        if "page" in kwargs:
            if kwargs["page"] is not None:
                self.page = kwargs["page"]
        Text.__init__(self, font=font, size=size, text=text)

class Lyric(Text):
    def __init__(self, **kwargs):
        font = None
        text = None
        size = None
        if "font" in kwargs:
            font = kwargs["font"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "syllabic" in kwargs:
            self.syllabic = kwargs["syllabic"]
        Text.__init__(self, text=text, font=font, size=size)

class Direction(Text):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                self.placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        Text.__init__(self,text=text,size=size,font=font)

    def toLily(self):
        default = 10

        textLilyString = "\markup { "+Text.toLily(self)+"}"
        symbol = ""
        return_val = ""
        if hasattr(self, "placement"):
            if self.placement == "above":
                symbol = "^"
            if self.placement == "below":
                symbol = "_"
        if len(textLilyString) > 0:
            return_val = symbol + textLilyString
        return return_val
class RehearsalMark(Direction):
    def toLily(self):
        text ="\mark "
        if self.text == "":
            text += "\default"
        else:
            index = string.ascii_lowercase.index(self.text.lower()) + 1
            text += "#"+str(index)
        return text


class Forward(Direction):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        placement = None
        if "duration" in kwargs:
            self.duration = kwargs["duration"]
        if "type" in kwargs:
            self.type = kwargs["type"]
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        Direction.__init__(self, placement=placement, text=text, size=size, font=font)

    def toLily(self):
        lilystring = "percent repeat"
        return_list = [lilystring]
        if hasattr(self, "duration"):
            if self.duration is None:
                self.duration = 2
            return_list.append(int(self.duration))
        return return_list

class RepeatSign(Direction):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        placement = None
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
                text = "\musicglyph #\"scripts."+self.type+"\""
        if "placement" in kwargs:
            if kwargs["placement"] is not None:
                placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        Direction.__init__(self, placement=placement, text=text,size=size,font=font)

    def toLily(self):
        return "\mark " + Direction.toLily(self)

class Line(Direction):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        placement = None
        if "placement" in kwargs:
            placement = kwargs["placement"]

        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]
        Direction.__init__(self, text=text, size=size, font=font, placement=placement)

class OctaveShift(Line):
    def __init__(self, **kwargs):
        placement = None
        text = None
        font = None
        size = None
        type = None
        if "amount" in kwargs:
            if kwargs["amount"] is not None:
                self.amount = kwargs["amount"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            if kwargs["type"] is not None:
                type = kwargs["type"]
        Line.__init__(self, text=text, type=type, size=size, font=font, placement=placement)

    def toLily(self):
        return_val = "\n\ottava #"
        multiplier = 1
        octave = 0
        if hasattr(self, "type"):
            if self.type == "down":
                return_val += "-"

        if hasattr(self, "amount"):
            if self.amount == 8:
                octave = 1
            if self.amount == 15:
                octave = 2

        return_val += str(octave)+"\n"
        if hasattr(self, "type"):
            if self.type == "stop":
                return_val = "\n\ottava #0"
        return return_val

class WavyLine(Line):
    def toLily(self):
        if not hasattr(self, "type"):
            text = "\start"
        else:
            text = "\\"+self.type
        return text + "TrillSpan"

class Pedal(Line):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        type = None
        placement = None
        if "line" in kwargs:
            if kwargs["line"] is not None:
                self.line = kwargs["line"]
        if "placement" in kwargs:
            placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            type = kwargs["type"]
        Line.__init__(self, type=type, text=text, size=size, font=font, placement=placement)

    def toLily(self):
        return_val = ""
        if (hasattr(self, "type") and self.type != "stop") or not hasattr(self, "type"):
            if hasattr(self, "line"):
                if not self.line:
                    return_val += "\n\set Staff.pedalSustainStyle = #'text\n"
        return_val += "\sustain"
        if hasattr(self, "type"):
            if self.type == "stop":
                return_val += "Off\n"
            elif self.type == "start":
                return_val += "On\n"
        else:
            return_val += "On\n"
        return return_val
class Bracket(Line):
    def __init__(self, **kwargs):
        text = None
        size = None
        font = None
        type = None
        placement = None
        if "number" in kwargs:
            if kwargs["number"] is not None:
                self.number = kwargs["number"]
        if "ltype" in kwargs:
            if kwargs["ltype"] is not None:
                self.lineType = kwargs["ltype"]
        if "elength" in kwargs:
            if kwargs["elength"] is not None:
                self.endLength = kwargs["elength"]
        if "lineEnd" in kwargs:
            if kwargs["lineEnd"] is not None:
                self.lineEnd = kwargs["lineEnd"]
        if "placement" in kwargs:
            placement = kwargs["placement"]
        if "text" in kwargs:
            text = kwargs["text"]
        if "size" in kwargs:
            size = kwargs["size"]
        if "font" in kwargs:
            font = kwargs["font"]
        if "type" in kwargs:
            type = kwargs["type"]
        Line.__init__(self, type=type, text=text, size=size, font=font, placement=placement)
    def toLily(self):
        lilystring = ""
        style_line = ""
        if hasattr(self, "lineType"):
            if self.lineType == "solid":
                style_line = "\\override TextSpanner.dash-fraction = 1.0"
            elif self.lineType == "dashed":
                style_line = "\\override TextSpanner.dash-fraction = 0.5"
        if hasattr(self, "type") and self.type == "stop":
            lilystring += "\\stopTextSpanner"
        else:
            lilystring += "\\startTextSpanner"
        if style_line == "":
            return lilystring
        return [style_line, lilystring]

class Metronome(Direction):
    def __init__(self, **kwargs):
        size = None
        font = None
        text = None
        if "beat" in kwargs:
            self.beat = kwargs["beat"]
        if "min" in kwargs:
            self.min = kwargs["min"]
        if hasattr(self, "min"):
            if hasattr(self, "beat"):
                text = str(self.beat) + " = " + str(self.min)
            else:
                text = self.min
        if "size" in kwargs:
            size = kwargs["text"]
        if "font" in kwargs:
            font = kwargs["font"]
        Text.__init__(self,text=text,size=size,font=font)
        if "parentheses" in kwargs:
            if kwargs["parentheses"] is not None:
                self.parentheses = kwargs["parentheses"]
        else:
            self.parentheses = False
    def toLily(self):
        return_val = "\\tempo "
        if hasattr(self, "parentheses"):
            if self.parentheses:
                return_val += "\"\" "
        if hasattr(self, "beat"):
            converter = {"quarter":4,"eighth":8,"half":2}
            if self.beat in converter:
                return_val += str(converter[self.beat]) + "="
            else:
                return_val += str(self.beat) + "="
        if hasattr(self, "min"):
            return_val += str(self.min)
        return return_val

    def get_detail(self):
        ret_list = self.get()
        if hasattr(self, "beat"):
            ret_list.append(self.beat)
        if hasattr(self, "min"):
            ret_list.append(self.min)
        return ret_list


class Dynamic(Direction):
    def __init__(self, **kwargs):
        placement = None
        size = None
        font = None
        text = None
        if "mark" in kwargs:
            self.mark = kwargs["mark"]
            text = self.mark
        if "text" in kwargs:
            text = kwargs["text"]

        if "size" in kwargs:
            size = kwargs["size"]

        if "font" in kwargs:
            font = kwargs["font"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        Direction.__init__(self,placement=placement,
                           font=font,
                           size=size,
                           text=text)

    def toLily(self):
        return_val = "\\"
        if hasattr(self, "mark"):
            return_val += self.mark
        return return_val

class Wedge(Dynamic):
    def __init__(self, **kwargs):
        placement = None
        self.type = None
        if "placement" in kwargs:
            placement = kwargs["placement"]
        if "type" in kwargs:
            self.type = kwargs["type"]

        Dynamic.__init__(self,placement=placement,text=self.type)

    def toLily(self):
        return_val = "\\"
        if hasattr(self, "type"):
            if self.type == "crescendo":
                return_val += "<"
            if self.type == "diminuendo":
                return_val += ">"
            if self.type == "stop":
                return_val += "!"

        return return_val


class Slur(Direction):
    def __init__(self, **kwargs):
        placement = None
        size = None
        font = None
        if "size" in kwargs:
            size = kwargs["size"]

        if "font" in kwargs:
            font = kwargs["font"]
        if "placement" in kwargs:
            placement = kwargs["placement"]

        if "type" in kwargs:
            if kwargs["type"] is not None:
                self.type = kwargs["type"]

        Direction.__init__(self,placement=placement,
                           font=font,
                           size=size)

    def toLily(self):
        return_val = ""
        if hasattr(self, "type"):
            if self.type == "start":
                return_val += "("
            if self.type == "stop":
                return_val += ")"
        return return_val
