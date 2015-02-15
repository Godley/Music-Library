try:
    from implementation.primaries.Drawing.classes.Measure import Measure
except:
    from classes.Measure import Measure

def NumbersToWords(number):
    units = ['one','two','three','four','five','six','seven','eight','nine']
    tens = ['ten','twenty','thirty','forty','fifty','sixty','seventy','eighty','ninety']
    output = ""
    if number > 0:
        str_val = str(number)
        if 4 > len(str_val) > 2:
            output += units[int(str_val[0])-1]
            output += "hundred"
            if str_val[1] != 0:
                output += "and" + tens[int(str_val[1])-1]
                if str_val[2] != 0:
                    output += units[int(str_val[2])-1]
        if 3 > len(str_val) > 1:
            output += tens[int(str_val[0])-1]
            if str_val[1] != 0:
                output += units[int(str_val[1])-1]
        if 2 > len(str_val) == 1:
            output += units[int(str_val[0])-1]
    return output

class Part(object):
    def __init__(self):
        self.measures = {}

    def __str__(self):
        self.CheckDivisions()
        st = ""
        if hasattr(self, "name"):
            st += "name:"+self.name
        for stave in self.measures.keys():
            st += "\n"
            st += "Staff: "
            st += str(stave)
            st += "\n\r Details: \r"
            for key in self.measures[stave]:
                st += "Measure: "
                st += str(key)
                st += str(self.measures[stave][key])
            st += "\n--------------------------------------------------------"
        return st

    def CheckDivisions(self):
        divisions = None
        for stave in self.measures:
            for key in self.measures[stave].keys():
                if hasattr(self.measures[stave][key], "divisions"):
                    divisions = self.measures[stave][key].divisions
                else:
                    self.measures[stave][key].divisions = divisions
                    self.measures[stave][key].CheckDivisions()

    def addMeasure(self, key, item, staff):
        if staff not in self.measures:
            self.measures[staff] = {}
        self.measures[staff][key] = item

    def addEmptyMeasure(self, key, staff):
        if staff not in self.measures:
            self.measures[staff] = {}
        self.measures[staff][key] = Measure()

    def getMeasure(self, key, staff):
        item = None
        if staff in self.measures:
            try:
                if key in self.measures[staff]:
                    item = self.measures[staff][key]
            except:
                print(key, self.measures[staff])
        return item

    def RepeatMeasure(self, sid, key, measure_strings, fwd, repeat_num=2):
        # recursive method. Handles situations where a bar or several bars need to use a percentage repeat.
        #we start by working backwards through each bar that has a forward
        indexer = len(fwd)
        while indexer > 0:
            item = fwd[indexer-1]
            # check whether the bar we're trying to duplicate is not another forwarded bar
            result = [True for k in measure_strings if k[0] == key]
            if len(result) == 0 or not result[0]:
                # if it is (aka, not in measure_strings) recurse!
                return self.RepeatMeasure(key-1, sid, measure_strings, fwd,repeat_num=repeat_num+1)
            else:
                # otherwise, copy the measure and set up another iterator
                measure_to_copy = self.measures[sid][key]
                length = item[1][1]
                iterator = len(measure_to_copy.notes)-1
                total = 0
                while total < length and iterator > -1:
                    # working backwards through the bar, compare the current note total to the amount that
                    # we need to repeat
                    total += measure_to_copy.notes[iterator].duration
                    if total >= length:
                        break
                    iterator -= 1

                iterator_copy = iterator
                if iterator == -1:
                    # if the iterator's past the end of the list python will think we want the final element, rather than exact 0
                    # so reset it to the bottom of the list
                    iterator = 0
                # take the section of the lily string that won't be repeated
                excluded_section = measure_to_copy.toLily(start=0, end=iterator)
                iterator = iterator_copy
                # take the section of the lilystring we want to repeat
                section = measure_to_copy.toLily(start=iterator, end=len(measure_to_copy.notes))
                #smash it all together
                combined_result = excluded_section + " \\repeat percent "+str(repeat_num)+" {" + section + "}"
                # find the tuple we need to replace
                replace_key = [index for index in range(len(measure_strings)) if measure_strings[index][0] == key]
                new_tuple = (measure_strings[replace_key[0]][0], combined_result)
                measure_strings[replace_key[0]] = new_tuple
            indexer-=1
        return measure_strings

    def handleBarlineAlternativeEndings(self, staff_id, measure_id):
        lilystring = ""
        barline = self.measures[staff_id][measure_id].GetBarline("right")
        if barline is not None:
            if hasattr(barline, "ending"):
                if measure_id+1 < len(self.measures[staff_id]) -1:
                    next_barline = self.measures[staff_id][measure_id+1].GetBarline("left")
                    if next_barline is not None:
                        if not hasattr(next_barline, "ending"):
                            lilystring = "}"
                    else:
                        lilystring = "}"
                else:
                    lilystring = "}"
        return lilystring


    def toLily(self):
        self.CheckDivisions()
        lilystring = ""
        staff_nums = list(self.measures.keys())
        variables = []
        variable_names = []
        for sid in staff_nums:
            variable = ""
            if hasattr(self, "name"):
                part_name = self.name.split(' ')
                first_part = part_name[0][0].lower() + part_name[0][1:-1]
                variable += first_part
                if len(part_name) > 1:
                    variable += "".join(part_name[1:-1])
            variable = "".join(variable)+"S"+NumbersToWords(sid)
            variable_names.append("\\"+variable)
            lilystring += variable + " = "
            lilystring += "\\new Staff"
            if hasattr(self, "name") and len(staff_nums) == 1:
                lilystring += " \with {\n"
                lilystring += "instrumentName = #\""+ self.name +" \"\n"
                lilystring += " }"
            lilystring += "{"
            lilystring += "\\autoBeamOff "
            measure_strings = []
            forward_measures = []
            opened = False
            closed = False
            for key in self.measures[sid]:
                return_val = self.measures[sid][key].toLily()
                string_to_update = ""
                if return_val is not list:
                    string_to_update = return_val
                else:
                    string_to_update = return_val[1]
                string_to_update += self.handleBarlineAlternativeEndings(sid, key)
                if return_val is list:
                    forward_measures.append((key,[return_val[0],string_to_update]))
                else:
                    measure_strings.append((key, string_to_update))


            if len(forward_measures) > 0 and len(measure_strings) > 0:
                measure_strings = self.RepeatMeasure(sid, forward_measures[len(forward_measures)-1][0]-1, measure_strings, forward_measures)
            lilystring += "\n\n".join(["% measure " + str(item[0]) + "\n" + item[1] for item in measure_strings if type(item[1]) != list])
            lilystring += "}\n\n"
            variables.append(lilystring)
            lilystring = ""

        if len(staff_nums) > 0:
            if len(staff_nums) > 1:
                lilystring += "\\new StaffGroup"
                if hasattr(self, "name"):
                    lilystring += " \with { \ninstrumentName = #\""
                    if len(self.name) > 10 and hasattr(self, "shortname"):
                        lilystring += self.shortname
                    else:
                        lilystring += self.name
                    lilystring += " \"\n}"

                lilystring+= " <<"
        lilystring += "\n".join(variable_names)
        if len(staff_nums) > 1:
            lilystring += ">>"
        return variables, lilystring