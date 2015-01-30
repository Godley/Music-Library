from implementation.primaries.Drawing.classes import MxmlParser, LilypondRender
import unittest, os
script = "/Users/charlottegodley/bin/lilypond"
class testRun(unittest.TestCase):
    def setUp(self):
        if hasattr(self, "item"):
            self.lp = LilypondRender.LilypondRender(self.item, self.file, script)
            self.lp.run()

    def testRun(self):
        if hasattr(self, "file"):
            pdf = self.file.split(".")[0] + ".pdf"
            self.assertTrue(os.path.exists(pdf))

parser = MxmlParser.MxmlParser()
for root, folders, files in os.walk('/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/testcases'):
    for file in files:
        if file.endswith("xml") and "metadata" not in root:
            class testFile(testRun):
                def setUp(self):
                    self.item = parser.parse(os.path.join(root, file))
                    self.file = os.path.join(root, file)
                    testRun.setUp(self)
            print(os.path.join(root,file))
            suite = unittest.TestLoader().loadTestsFromTestCase(testFile)
            unittest.TextTestRunner(verbosity=2).run(suite)
