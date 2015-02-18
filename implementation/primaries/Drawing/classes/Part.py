try:
    from implementation.primaries.Drawing.classes.Measure import Measure
except:
    from classes.Measure import Measure

def NumbersToWords(number):
    # little function that converts numbers to words. This could be more efficient,
    # and won't work if the number is bigger than 999 but it's for stave names,
    # and I doubt any part would have more than 10 staves let alone 999.
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
        divisions = 8
        for staff in self.measures:
            for number in self.measures[staff]:
                if hasattr(self.measures[staff][number], "divisions") and self.measures[staff][number].divisions is not None:
                    divisions = self.measures[staff][number].divisions
            [self.measures[staff][key].SetDivisions(divisions) for key in self.measures[staff]]
            [self.measures[staff][key].CheckDivisions() for key in self.measures[staff]]

    def addMeasure(self, item, measure=1, staff=1):
        if staff not in self.measures:
            self.measures[staff] = {}
        self.measures[staff][measure] = item

    def addEmptyMeasure(self, measure=1, staff=1):
        if staff not in self.measures:
            self.measures[staff] = {}
        self.measures[staff][measure] = Measure()

    def getMeasure(self, measure=1, staff=1):
        item = None
        if staff in self.measures:
            try:
                if measure in self.measures[staff]:
                    item = self.measures[staff][measure]
            except:
                print(measure, self.measures[staff])
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
        # method to handle closing of alternative{ section in lilypond, based on whether we've reached the final
        # alternate ending
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

    def GetVariableName(self, staff):
        # small method to get the variable name for a specific part and staff
        # may run into issues if there are multiple parts with the same name, but let's hope not
        variable = ""
        if hasattr(self, "name") and (len(self.name) > 0 and self.name != " "):
            self.name = self.name.strip()
            split_name = self.name.split(' ')
            joined_name = "".join(split_name)
            first_letter = joined_name[0].lower()

            #lilypond won't allow numbers to be in variable names, so convert these to words
            if first_letter in ["0","1","2","3","4","5","6","7","8","9"]:
                first_letter = NumbersToWords(int(first_letter))
            variable += first_letter
            if len(joined_name) > 1:
                variable += joined_name[1:len(joined_name)]
        variable += "S"+NumbersToWords(staff)
        return variable

    def toLily(self):
        self.CheckDivisions()
        lilystring = ""
        staff_nums = list(self.measures.keys())

        # set up a couple of lists which will be our strings coming from each part, and their variable names
        variables = []
        variable_names = []
        for sid in staff_nums:
            variable = ""

            # create the staff variable name, based on the name of the part combined with the staff number in words
            variable = self.GetVariableName(sid)
            variable_names.append("\\"+variable)
            # set up the lilystring for that variable
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

            for key in self.measures[sid]:
                return_val = self.measures[sid][key].toLily()
                string_to_update = ""
                if return_val is not list:
                    string_to_update = return_val
                else:
                    string_to_update = return_val[1]
                string_to_update += self.handleBarlineAlternativeEndings(sid, key)
                if return_val is list:
                    # measure will only return a list if it contains a forward
                    forward_measures.append((key,[return_val[0],string_to_update]))
                else:
                    # otherwise it'll be a string
                    measure_strings.append((key, string_to_update))


            if len(forward_measures) > 0 and len(measure_strings) > 0:
                # update measure strings to reflect any repeats needed (forwards)
                measure_strings = self.RepeatMeasure(sid, forward_measures[len(forward_measures)-1][0]-1, measure_strings, forward_measures)

            # finally, put all the measure strings together into the variable assignment
            lilystring += "\n\n".join(["% measure " + str(item[0]) + "\n" + item[1] for item in measure_strings if type(item[1]) != list])
            lilystring += "}\n\n"
            variables.append(lilystring)
            lilystring = ""

        # this section sets up the grouping of each stave variable we've set up, known as this part's lilystring
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
        # lastly, return any variables and the lilystring of the part. These have to be separated as variables must
        # come a long way before each variable call in the staff section
        return variables, lilystring