class Part(object):
    def __init__(self):
        self.measures = {}

    def __str__(self):
        self.CheckDivisions()
        st = ""
        if hasattr(self, "name"):
            st += "name:"+self.name
        for key in self.measures.keys():
            st += "\n"
            st += "Measure: "
            st += str(key)
            st += "\n\r Details: \r"
            st += str(self.measures[key])
            st += "\n--------------------------------------------------------"
        return st

    def CheckDivisions(self):
        divisions = None
        for key in self.measures.keys():
            if hasattr(self.measures[key], "divisions"):
                divisions = self.measures[key].divisions
            else:
                self.measures[key].divisions = divisions
                self.measures[key].CheckDivisions()

    def RepeatMeasure(self, key, sid, measure_strings, fwd, repeat_num=2):
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
                measure_to_copy = self.measures[key]
                length = item[1][1]
                iterator = len(measure_to_copy.notes[sid])-1
                total = 0
                while total < length or iterator > -1:
                    # working backwards through the bar, compare the current note total to the amount that
                    # we need to repeat
                    total += measure_to_copy.notes[sid][iterator].duration
                    if total >= length:
                        break
                    iterator -= 1

                iterator_copy = iterator
                if iterator == -1:
                    # if the iterator's past the end of the list python will think we want the final element, rather than exact 0
                    # so reset it to the bottom of the list
                    iterator = 0
                # take the section of the lily string that won't be repeated
                excluded_section = measure_to_copy.toLily(1, start=0, end=iterator)
                iterator = iterator_copy
                # take the section of the lilystring we want to repeat
                section = measure_to_copy.toLily(1, start=iterator, end=len(measure_to_copy.notes[sid]))
                #smash it all together
                combined_result = excluded_section + " \\repeat percent "+str(repeat_num)+" {" + section + "}"
                # find the tuple we need to replace
                replace_key = [index for index in range(len(measure_strings)) if measure_strings[index][0] == key]
                new_tuple = (measure_strings[replace_key[0]][0], combined_result)
                measure_strings[replace_key[0]] = new_tuple
            indexer-=1
        return measure_strings

    def toLily(self):
        lilystring = ""
        if len(self.measures.keys()) > 0:
            staff_nums = self.measures[list(self.measures.keys())[0]].notes.keys()
            if len(staff_nums) > 1:
                lilystring += "\\new StaffGroup <<"
            for sid in staff_nums:
                lilystring += "\\new Staff"
                if hasattr(self, "name"):
                    lilystring += " \with { \ninstrumentName = #\""+ self.name +" \"\n}"
                lilystring += "{"
                measure_strings = [(key, self.measures[key].toLily(sid)) for key in self.measures if type(self.measures[key].toLily(sid)) is not list]
                forward_measures = [(key, self.measures[key].toLily(sid)) for key in self.measures if type(self.measures[key].toLily(sid)) is list]
                print(measure_strings, forward_measures)
                if len(forward_measures) > 0:
                    measure_strings = self.RepeatMeasure(forward_measures[len(forward_measures)-1][0]-1,sid, measure_strings, forward_measures)
                lilystring += "".join([item[1] for item in measure_strings])
                lilystring += "}"
            if len(staff_nums) > 1:
                lilystring += ">>"
        return lilystring