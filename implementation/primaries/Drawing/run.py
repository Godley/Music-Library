import os
try:
    from classes import MxmlParser, LilypondRender
except:
    from implementation.primaries.Drawing.classes import MxmlParser, LilypondRender
import os, sys

testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases'
file = os.path.join(testcases, sys.argv[1])
parser = MxmlParser.MxmlParser()
pieceObj = parser.parse(file)
render = LilypondRender.LilypondRender(pieceObj, file)
render.run()
os.system("open "+render.pdf)


