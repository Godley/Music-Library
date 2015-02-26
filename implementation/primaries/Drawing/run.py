
try:
    from classes import MxmlParser, LilypondRender
except:
    from implementation.primaries.Drawing.classes import MxmlParser, LilypondRender
import os, sys


testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases'
file = os.path.join(testcases, "lg-213324487.xml")
parser = MxmlParser.MxmlParser()
pieceObj = parser.parse(file)
render = LilypondRender.LilypondRender(pieceObj, file)
render.run()
os.system("open "+render.pdf)


