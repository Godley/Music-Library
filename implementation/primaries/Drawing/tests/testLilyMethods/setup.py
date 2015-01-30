import unittest, os
from implementation.primaries.Drawing.classes import LilypondRender

class Lily(unittest.TestCase):
    def setUp(self):
        self.compile = False
        self.wrappers = []


    def testValue(self):
        if hasattr(self, "lilystring"):
            if hasattr(self, "item"):
                self.assertEqual(self.lilystring, self.item.toLily())

    def testCompilation(self):
        if hasattr(self, "compile"):
            if self.compile and hasattr(self, "item"):
                output = self.item.toLily()
                test_file = open("/Users/charlottegodley/testlily.ly", 'w')
                test_file.writelines(output)
                if os.path.exists("/Users/charlottegodley/testlily.pdf"):
                    os.remove("/Users/charlottegodley/testlily.pdf")
                ly = LilypondRender.LilypondRender(self.item, "/Users/charlottegodley/testlily.xml", "/Users/charlottegodley/bin/lilypond")
                if hasattr(self, "wrappers"):
                    ly.run(wrappers=self.wrappers)
                else:
                    ly.run()
                self.assertTrue(os.path.exists("/Users/charlottegodley/testlily.pdf"))

