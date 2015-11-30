from cx_Freeze import setup, Executable
import sys


zips = ["implementation/primaries/GUI/designer_files",
         "implementation/primaries/GUI/themes", "implementation/primaries/GUI/images",
         "implementation/primaries/scripts", "implementation/primaries/GUI/designer_files/icons.qrc"]


base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

shortcut_table = [
    ("DesktopShortcut",        # Shortcut
     "DesktopFolder",          # Directory_
     "DTI Playlist",           # Name
     "TARGETDIR",              # Component_
     "[TARGETDIR]Application.exe",# Target
     None,                     # Arguments
     None,                     # Description
     None,                     # Hotkey
     None,                     # Icon
     None,                     # IconIndex
     None,                     # ShowCmd
     'TARGETDIR'               # WkDir
     )
    ]
msi_data = {"Shortcut": shortcut_table}

# Change some default MSI options and specify the use of the above defined tables
bdist_msi_options = {'data': msi_data}
options = {
    'build_exe': {
        'includes': 'atexit',
        "include_files":zips
    },
    'bdist_mac': {
        'bundle_name': 'MuseLib',
        'custom_info_plist' : "info.plist"
    },
    'bdist_msi': bdist_msi_options
}



# Now create the table dictionary


executables = [
    Executable("implementation/primaries/GUI/Application.py", base=base, compress=False, shortcutName="MuseLib",
            shortcutDir="DesktopFolder")
]

setup(name='MuseLib',
      version='0.1',
      description='Sample cx_Freeze PyQt4 script',
      options=options,
      executables=executables,

      packages=['implementation', 'implementation.primaries', 'implementation.primaries.GUI', 'implementation.primaries.scripts',
              'implementation.primaries.GUI.pyqt_plugins', 'implementation.primaries.ExtractMetadata',
              'implementation.primaries.ExtractMetadata.classes', 'implementation.primaries.ImportOnlineDBs','implementation.primaries.ImportOnlineDBs.classes']
      )