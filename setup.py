from distutils.core import setup

setup(
    name='FYP',
    version='0.1',
    packages=['implementation', 'implementation.primaries', 'implementation.primaries.GUI',
              'implementation.primaries.Drawing', 'implementation.primaries.Drawing.tests',
              'implementation.primaries.Drawing.tests.testHandlers',
              'implementation.primaries.Drawing.tests.testUsingXML',
              'implementation.primaries.Drawing.tests.testLilyMethods', 'implementation.primaries.Drawing.classes',
              'implementation.primaries.Drawing.classes.tree_cls', 'implementation.primaries.ExtractMetadata',
              'implementation.primaries.ExtractMetadata.tests',
              'implementation.primaries.ExtractMetadata.tests.test_files',
              'implementation.primaries.ExtractMetadata.tests.test_files.unzip_tests',
              'implementation.primaries.ExtractMetadata.classes'],
    url='http://github.com/fyp',
    license='',
    author='charlottegodley',
    author_email='me@charlottegodley.co.uk',
    description='my final year project'
)
