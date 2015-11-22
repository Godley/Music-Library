import unittest, sys, os
from implementation.primaries.GUI import helpers

class testStylesheet(unittest.TestCase):
    def setUp(self):
        pass

    def testCleanPath(self):
        path = 'themes/item.png'
        if sys.platform == 'win32':
            expected = "themes\\item.png"
        else:
            expected = path
        self.assertEqual(expected, helpers.cleanPath(path))

    def testParseThemePath(self):
        path = 'themes/item.png'
        expected = "'" + os.path.join(helpers.get_base_dir(True), 'themes', 'item.png') + "'"
        cleaned_path = helpers.cleanPath(path)
        self.assertEqual(expected, helpers.parseThemePath(cleaned_path))

    def testParseThemePathWithCSS(self):
        line = 'background: url(/themes/zoom-out.png) center no-repeat;'
        expected = "background: url('" + os.path.join(helpers.get_base_dir(True), 'themes', "zoom-out.png")+ '\') center no-repeat;'
        cleaned_path = helpers.cleanPath(line)
        self.assertEqual(expected, helpers.parseThemePath(cleaned_path))

    def testParseIconPath(self):
        path = 'themes/icons/item.png'
        theme = 'ubuntu'
        new_path = os.path.join(helpers.get_base_dir(True), 'themes', 'icons', 'ubuntu', 'item.png')
        if sys.platform == 'win32':
            expected = "'" + new_path + "'"
        else:
            expected = new_path
        cleaned_path = helpers.cleanPath(path)
        themed_path = helpers.parseThemePath(cleaned_path)
        self.assertEqual(expected, helpers.parseIconPath(themed_path, theme))

    def testPostProcessor(self):
        lines = 'themes\\icons'
        expected = 'themes/icons'
        self.assertEqual(expected, helpers.postProcessLines(lines))