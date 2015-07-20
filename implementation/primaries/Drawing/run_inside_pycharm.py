#!/usr/bin/python

try:
    from classes import MxmlParser, LilypondRender
except:
    from implementation.primaries.Drawing.classes import LilypondRender
    from implementation.primaries.Drawing.classes.Input import MxmlParser
import os
import sys


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




