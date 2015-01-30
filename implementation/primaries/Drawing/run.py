import os
from implementation.primaries.Drawing.classes import MxmlParser
import os

testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases'
file = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/accidentals.xml'
parser = MxmlParser.MxmlParser()
pieceObj = parser.parse(file)
lilypond_file = file.split(".")[0] + ".ly"
pdf_file = file.split(".")[0] + ".pdf"
fob = open(lilypond_file, 'w')
fob.write(pieceObj.toLily())
fob.close()

