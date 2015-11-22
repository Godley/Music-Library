import sys
import os
from implementation.primaries.exceptions import LilypondNotInstalledException
from implementation.primaries.GUI.helpers import get_base_dir
from MuseParse.classes.Output.helpers import setupLilypondClean as setupLilypond


def do_setup(path=None):
    defaults = {'darwin': "/Applications/Lilypond.app/Contents/Resources/bin",
                'win32': "C:/Program Files (x86)/LilyPond/usr/bin"}
    n_path = path
    if n_path is None:
        n_path = defaults[sys.platform]
    filename = {'darwin': 'lilypond.sh', 'win32': 'lilypond.exe'}
    filepath = os.path.join(n_path, filename[sys.platform])
    if os.path.exists(filepath):
        setupLilypond(n_path)
    else:
        raise LilypondNotInstalledException('ERROR! Lilypond not installed or filepath incorrect. Please provide the folder which contains '+filename[sys.platform])

