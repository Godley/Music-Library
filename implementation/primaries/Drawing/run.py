import os
from implementation.primaries.Drawing.classes import Piece, MxmlParser
import os

testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases'
file = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/accidentals.xml'
parser = MxmlParser.MxmlParser()
pieceObj = parser.parse(file)
lilypond_file = file.split(".")[0] + ".ly"
fob = open(lilypond_file, 'w')
fob.write(pieceObj.toLily())
fob.close()
os.system("/Users/charlottegodley/bin/lilypond --output "+testcases+" "+lilypond_file)
