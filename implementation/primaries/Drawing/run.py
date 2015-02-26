
try:
    from classes import MxmlParser, LilypondRender
except:
    from implementation.primaries.Drawing.classes import MxmlParser, LilypondRender
import os, sys


def Run(fname):
    parser = MxmlParser.MxmlParser()
    pieceObj = parser.parse(fname)
    render = LilypondRender.LilypondRender(pieceObj, fname)
    render.run()
    os.system("open "+render.pdf)

testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases'
if len(sys.argv) > 3:
    file = os.path.join(testcases, sys.argv[1])
    Run(file)
else:
    files = os.listdir(os.path.join(testcases, "lilypond-provided-testcases"))
    files = [file for file in files if file.endswith(".xml")]
    for file in files:
        print(file)
        Run(os.path.join(testcases, "lilypond-provided-testcases", file))




