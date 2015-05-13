from cx_Freeze import setup, Executable
import sys


zips = ["implementation/primaries/GUI/designer_files",
         "implementation/primaries/GUI/themes", "implementation/primaries/GUI/images",
         "implementation/primaries/scripts"]


base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': {
        'includes': 'atexit',
        "include_files":zips
    }
}

executables = [
    Executable("implementation/main.py", base=base)
]

setup(name='MuseLib',
      version='0.1',
      description='Sample cx_Freeze PyQt4 script',
      options=options,
      executables=executables,
      packages=['implementation', 'implementation.primaries', 'implementation.primaries.GUI', 'implementation.primaries.scripts',
              'implementation.primaries.GUI.pyqt_plugins', 'implementation.primaries.Drawing', 'implementation.primaries.Drawing.classes',
              'implementation.primaries.Drawing.classes.tree_cls', 'implementation.primaries.ExtractMetadata',
              'implementation.primaries.ExtractMetadata.classes', 'implementation.primaries.ImportOnlineDBs','implementation.primaries.ImportOnlineDBs.classes']
      )