#!/usr/bin/python

try:
    from classes import MxmlParser, LilypondRender
except:
    from implementation.primaries.Drawing.classes import MxmlParser, LilypondRender
import os, sys


def Run(fname):
    parser = MxmlParser.MxmlParser()
    try:
        pieceObj = parser.parse(fname)
    except BaseException as e:
        return [fname, str(e)]
    render = LilypondRender.LilypondRender(pieceObj, fname)
    try:
        render.run()
    except Exception as e:
        return [render.lyfile, str(e)]
    if not os.path.exists(render.pdf):
        return render.lyfile

testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases'
failed = []
if len(sys.argv) > 3 or sys.argv[1].endswith(".xml"):
    file = os.path.join(testcases, sys.argv[1])
    Run(file)
else:
    for root, dirs, files in os.walk(os.path.join(testcases, "lilypond-provided-testcases")):
        for file in files:
            if file.endswith(".xml"):
                result = Run(os.path.join(root, file))
                if result is not None:
                    failed.append(result)
    file = os.path.join(testcases, "lilypond-provided-testcases", "73a-Percussion.xml")
    Run(file)

print("The following files failed")
for f in failed:
    if type(f) is list:

        print("File:",f[0])
        print("failed with Exception:",f[1])
    else:
        print("File:",f[0], " failed parsing through Lilypond")
        os.system("open "+f)




