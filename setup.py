
from cx_Freeze import setup, Executable
import os, shutil, glob, sys


zips = ["implementation/primaries/GUI/designer_files",
         "implementation/primaries/GUI/themes", "implementation/primaries/GUI/images",
         "implementation/primaries/scripts", "implementation/primaries/GUI/designer_files/icons.qrc"]

buildexe_options = {}
buildexe_options['includes'] = ['sip', 'atexit']
buildexe_options['include_files'] = zips
#
# imageformats_path = None
# for path in qt_library_path:
#     if os.path.exists(os.path.join(path, 'imageformats')):
#         imageformats_path = os.path.join(path, 'imageformats')
#         local_imageformats_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'imageformats')
#
#         buildexe_options['include_files'] = ['imageformats']
#
#         if not os.path.exists(local_imageformats_path):
#             os.mkdir(local_imageformats_path)
#         for file in glob.glob(os.path.join(imageformats_path, '*')):
#             shutil.copy(file, os.path.join(local_imageformats_path, os.path.basename(file)))
base = None
if sys.platform == 'win32':
    base = 'Win32GUI'

options = {
    'build_exe': buildexe_options,
    'bdist_mac': {
        'bundle_name': 'MuseLib',
        'iconfile': 'icon.icns',
        'custom_info_plist': 'info.plist'
    }
}

executables = [
    Executable("implementation/primaries/GUI/Application.py", base=base, compress=False)
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