import sys, os
from implementation.primaries.exceptions import LilypondNotInstalledException
from implementation.primaries.GUI.helpers import get_base_dir
from MuseParse.helpers import setup_lilypond

def do_setup(path=None):
    defaults = ["/Applications/Lilypond.app/Contents/Resources/bin", "C:/Program Files (x86)/LilyPond/usr/bin"]
    filepath = None
    lpond_path = None
    if sys.platform == "darwin":
        if path is None:
            lpond_path = defaults[0]
        else:
            lpond_path = os.path.join(path, "Contents/Resources/bin")
            filepath = os.path.join(lpond_path, "lilypond")

    elif sys.platform == "win32" or sys.platform == "win64":
        if path is None:
            lpond_path = defaults[1]
        else:
            lpond_path = path
            filepath = os.path.join(lpond_path, "lilypond.exe")
    if filepath is not None and os.path.exists(filepath):
        setup_lilypond(lpond_path)
    else:
        raise LilypondNotInstalledException('ERROR! Windows edition of Lilypond not in expected folder')
