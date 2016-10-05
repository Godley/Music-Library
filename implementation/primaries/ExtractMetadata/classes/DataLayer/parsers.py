class TempoParser(object):
    converter = {"crotchet": "quarter",
                 "quaver": "eighth",
                 "minim": "half",
                 "semibreve": "whole",
                 "quarter": "quarter",
                 "eighth": "eighth",
                 "half": "half",
                 "whole": "whole"}
    halvers = ['semi', 'hemi', 'demi']

    def splitParts(self, tempo):
        return tempo.split("=")

    def parseHalvers(self, tempo):
        seg_length = 4
        index = 0
        value = 8
        while tempo[index:index + seg_length] in self.halvers:
            value *= 2
            index += seg_length
        return value

    def parseHalversToString(self, tempo):
        halver_str = str(self.parseHalvers(tempo))
        if halver_str[-1] == "2":
            halver_str += 'nd'
        else:
            halver_str += 'th'
        return halver_str

    def convertToAmerican(self, entry):
        if entry in self.converter:
            return self.converter[entry]

    def getDots(self, entry):
        end_of_word = len(entry) - 1
        dots = ''
        while end_of_word > -1:
            if entry[end_of_word] == '.':
                dots += '.'
            else:
                break
            end_of_word -= 1
        new_word = entry[:end_of_word + 1]
        return dots, new_word

    def parseWord(self, word):
        dots, remaining = self.getDots(word)
        if word[:4] in self.halvers:
            value = self.parseHalversToString(remaining)
        else:
            value = self.convertToAmerican(remaining)
        return value + dots

    def decode(self, entry):
        parts = self.splitParts(entry)
        result = {}
        minute = None
        beat_2 = None
        beat = self.parseWord(parts[0])
        try:
            minute = int(parts[1])
        except ValueError:
            beat_2 = self.parseWord(parts[1])
        result['beat'] = beat
        result['minute'] = minute
        result['beat_2'] = beat_2
        return result

    def encode(self, entry):
        tempo_string = str(entry['beat']) + "="
        if entry['beat_2'] != None:
            tempo_string += str(entry['beat_2'])
        elif entry['minute'] != None:
            tempo_string += str(entry['minute'])
        return tempo_string

class MeterParser(object):
    def encode(self, entry):
        return "{}/{}".format(entry['beat'], entry['beat_type'])