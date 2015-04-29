import os, csv, re
from implementation.primaries.Drawing import tests

folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/Drawing/tests"
file_list = {}
csv_dict = {}

def Add(file, root):
    global file_list
    file_list[file] = root

def statement_type(line):
    if "class" in line:
        return "class"
    if "def" in line:
        return "func"
    if "assert" in line:
        return "assert"
    if "=" in line:
        return "assignment"

def ParseInstance(line):
    expected = ""
    params = line.split(",")
    expected += params[0] + " is of the object type " + params[1]
    return expected,None

def ParseNone(line):
    if isMethod(line):
        return line + " has the return value of None", None

def ParseBool(line):
    expected = ""
    if isMethod(line):
        if "hasattr" in line:
            params = removeParamBrackets(line[7:])
            split_params = params.split(",")
            expected += "object "+split_params[0]+" has the attribute "+split_params[1]
    elif "in" in line:
        word = ""
        for index in range(len(line)):
            word += line[index]
            if len(word) > 2:
                if  word[-2] + word[-1] == "in":
                    break
        word = word[:-2]
        expected += "the value " + word + "is in the iterable or string " + line[len(word)+2:]
    return expected, None

def removeParamBrackets(line):
    return line[1:-1]
def isMethod(line):
    if "(" in line:
        return True
    return False

def ParseEqual(line):
    parts = line.split(",")
    expected = ""
    variables = None
    if "\"" not in parts[0]:
        if parts[0] in assignments.keys():
            parts[0] = assignments[parts[0]]
    if isMethod(parts[1]):
        if "len" in parts[1]:
            thing = removeParamBrackets(parts[1][4:])
            expected += thing + " has a length of " + parts[0]
        else:
            expected += parts[1] + " has a return value of " + parts[0]
    else:
        expected += parts[1] + " is equal to " + parts[0]

    return expected, variables

for root, dirs, files in os.walk(folder, topdown=False):
    [Add(f, root.split("/")[-1]) for f in files if f.endswith("py") and f != "__init__.py"]
variables_second_pass = []
assignments = {}
for pyfile in file_list.keys():
    if file_list[pyfile] not in csv_dict:
        csv_dict[file_list[pyfile]] = {}
    csv_dict[file_list[pyfile]][pyfile] = {}
    fob = open(os.path.join(folder, file_list[pyfile], pyfile), 'r')
    classname = ""
    testname = ""

    for line in fob.readlines():
        class_regex = "class test"
        func_regex = "def test"
        assert_reg = "self.assert"
        if "=" in line:
            var_and_value = line.split("=")
            assignments[var_and_value[0]] = var_and_value[1]

        if class_regex in line:
            list_of_string = list(line)
            removed_class = line[6:]
            classname = "".join(removed_class).split("(")[0]
            csv_dict[file_list[pyfile]][pyfile][classname] = {}
        if func_regex in line:
            list_of_string = list(line)
            removed_def = line[8:]
            testname = "".join(removed_def).split("(")[0]
            csv_dict[file_list[pyfile]][pyfile][classname][testname] = ""
        if assert_reg in line:

            options = {"IsInstance":ParseInstance,"True":ParseBool,"Equal":ParseEqual,"False":ParseBool,"IsNone":ParseNone}
            listed_assert = list(line)
            index = 0
            found = False
            word = ""
            count = False
            while not found:
                if listed_assert[index] == "a":
                    count = True
                if count:
                    word += listed_assert[index]
                if listed_assert[index] == "t":
                    count = False
                if word == "assert":
                    found = True
                index += 1
            line_without_assert = listed_assert[index:]
            test = "".join(line_without_assert).split("(")[0]
            comparison = line_without_assert[len(test)+1:-2]
            value = "".join(comparison)
            expected, variables = options[test](value)
            csv_dict[file_list[pyfile]][pyfile][classname][testname] = [test,expected]
    fob.close()

fname = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/mytests.csv"

csv_list = []

for folder in csv_dict:
    #print("Folder: ", folder)
    for file in csv_dict[folder]:
        #print("File: ", file)
        for classname in csv_dict[folder][file]:
            #print("classname: ", classname)
            for function in csv_dict[folder][file][classname]:
                csv_list.append({"folder":folder, "file":file, "class": classname, "function": function})
                if csv_dict[folder][file][classname][function] != "":
                    csv_list[-1]["test type"] = csv_dict[folder][file][classname][function][0]
                    csv_list[-1]["expected result"] = csv_dict[folder][file][classname][function][1]
                #print("function: ", function)
                #print("assert: ", csv_dict[folder][file][classname][function][0], "expected result: ", csv_dict[folder][file][classname][function][1])

fields = ["folder","file","class","function","test type", "expected result"]
with open(fname, 'w') as csvfile:
    writer = csv.DictWriter(csvfile, fields)
    writer.writeheader()
    for entry in csv_list:
        writer.writerow(entry)