from distutils.core import setup
import py2exe

setup(
    windows=[{"script":"implementation/main.py"}],
    name='FYP',
    version='',
    packages=['implementation', 'implementation.primaries', 'implementation.primaries.GUI',
              'implementation.primaries.GUI.pyqt_plugins', 'implementation.primaries.Drawing',
              'implementation.primaries.Drawing.tests', 'implementation.primaries.Drawing.tests.testHandlers',
              'implementation.primaries.Drawing.tests.testUsingXML',
              'implementation.primaries.Drawing.tests.testLilyMethods', 'implementation.primaries.Drawing.classes',
              'implementation.primaries.Drawing.classes.tree_cls', 'implementation.primaries.ExtractMetadata',
              'implementation.primaries.ExtractMetadata.tests',
              'implementation.primaries.ExtractMetadata.tests.test_files',
              'implementation.primaries.ExtractMetadata.tests.test_files.unzip_tests',
              'implementation.primaries.ExtractMetadata.classes', 'implementation.primaries.ImportOnlineDBs',
              'implementation.primaries.ImportOnlineDBs.tests', 'implementation.primaries.ImportOnlineDBs.classes'],
    url='http://github.com/Godley/FYP',
    license='',
    author='charlottegodley',
    author_email='me@charlottegodley.co.uk',
    description='',
    options={"py2exe":{"includes":["sip"]}})

