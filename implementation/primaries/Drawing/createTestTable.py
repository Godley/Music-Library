import os, csv, re
from implementation.primaries.Drawing import tests

folder = "/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/Drawing/tests"
file_list = {}
csv_dict = {}

def Add(file, root):
    global file_list
    file_list[file] = root


for root, dirs, files in os.walk(folder, topdown=False):
    [Add(f, root.split("/")[-1]) for f in files if f.endswith("py") and f != "__init__.py"]

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
            csv_dict[file_list[pyfile]][pyfile][classname][testname] = line

for folder in csv_dict:
    print("Folder: ", folder)
    for file in csv_dict[folder]:
        print("File: ", file)
        for classname in csv_dict[folder][file]:
            print("classname: ", classname)
            for function in csv_dict[folder][file][classname]:
                print("function: ", function)
                print("assert: ", csv_dict[folder][file][classname][function])
