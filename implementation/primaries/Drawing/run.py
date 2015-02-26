
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
    if os.path.exists(render.pdf):
        os.system("open "+render.pdf)
    else:
        raise(BaseException("BAD LILYPOND"))

testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases'
if len(sys.argv) > 3:
    file = os.path.join(testcases, sys.argv[1])
    Run(file)
else:
    for root, dirs, files in os.walk(os.path.join(testcases, "lilypond-provided-testcases")):
        for file in files:
            if file.endswith(".xml"):
                Run(os.path.join(root, file))




