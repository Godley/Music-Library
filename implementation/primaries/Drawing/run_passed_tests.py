#!/usr/bin/python

try:
    from classes import MxmlParser, LilypondRender
except:
    from implementation.primaries.Drawing.classes import MxmlParser, LilypondRender
import os, unittest
import unittest

l = [["foo", "a", "a",], ["bar", "a", "b"], ["lee", "b", "b"]]

class TestSequense(unittest.TestCase):
    pass

def test_generator(output, expected):
    def test(self):
        output_obj = open(output, 'r')
        lines = output_obj.readlines()
        expected_obj = open(expected, 'r')
        expected_lines = expected_obj.readlines()
        for line, expected_line in zip(lines, expected_lines):
            self.assertEqual(line, expected_line)
    return test


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

testcases = '/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases/lilypond-passing-tests'
failed = []
if __name__ == '__main__':
    for root, dirs, files in os.walk(testcases):
        for file in files:
            if file.endswith(".xml"):
                result = Run(os.path.join(root, file))
                if result is not None:
                    failed.append(result)
                else:
                    output = file.split(".")[0]+".ly"
                    expected = os.path.join(testcases, "expected", output)
                    if os.path.exists(expected):
                        test_name = 'test_%s' % file
                        test = test_generator(os.path.join(testcases,output), expected)
                        setattr(TestSequense, test_name, test)
        unittest.main()



