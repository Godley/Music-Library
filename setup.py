from cx_Freeze import setup, Executable
import sys
import os


# GUI applications require a different base on Windows (the default is for a
# console application).
base = None
print(os.path.exists("implementation\main.py"))
if sys.platform == "win32":
    base = "Win32GUI"

files = {'implementation.primaries.GUI':["designer_files/*.ui",
         "themes/*.qss", "images/*.png"]}
zips = ["implementation/primaries/GUI/designer_files",
         "implementation/primaries/GUI/themes", "implementation/primaries/GUI/images",
         "implementation/primaries/scripts"]
build_exe_options = {"packages": ["os"], "excludes": ["tkinter"],
                     "include_files":zips}


setup(
    name='FYP',
    version='0.1',
    #package_data = files,
    packages=['implementation', 'implementation.primaries', 'implementation.primaries.GUI', 'implementation.primaries.scripts',
              'implementation.primaries.GUI.pyqt_plugins', 'implementation.primaries.Drawing', 'implementation.primaries.Drawing.classes',
              'implementation.primaries.Drawing.classes.tree_cls', 'implementation.primaries.ExtractMetadata',
              'implementation.primaries.ExtractMetadata.classes', 'implementation.primaries.ImportOnlineDBs','implementation.primaries.ImportOnlineDBs.classes'],
    url='http://github.com/godley/fyp',
    license='',
    author='charlottegodley',
    author_email='me@charlottegodley.co.uk',
    description='MuseLib',
    options = {"build_exe": build_exe_options},
    executables = [Executable("implementation/main.py", base=base)]
)
