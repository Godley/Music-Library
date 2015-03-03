#!/usr/bin/python

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
    if not os.path.exists(render.pdf):
        return render.lyfile

testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/lilypond-provided-testcases'
failed = []
if len(sys.argv) > 1:
    file = os.path.join(testcases, sys.argv[1])
    Run(file)




