import sys, os
from implementation.primaries.exceptions import LilypondNotInstalledException
from implementation.primaries.GUI.helpers import get_base_dir


def setup_lilypond(path=None):
    defaults = ["/Applications/Lilypond.app/Contents/Resources/bin/lilypond", "C:/Program Files/LilyPond/usr/bin"]

    if sys.platform == "darwin":
        if path is None:
            mac_path = defaults[0]
        else:
            mac_path = path
        if os.path.exists(mac_path):
            fob = open(os.path.join(get_base_dir(), "scripts", "lilypond_mac.sh"), 'r')
            lines = fob.readlines()
            new_lines = [lines[0], "LILYPOND="+mac_path+"\n", lines[1]]
            fob.close()
            fob = open(os.path.join(get_base_dir(), "scripts", "lilypond"), 'w')
            fob.writelines(new_lines)
            fob.close()
            os.system("chmod u+x "+os.path.join(get_base_dir(), "scripts", "lilypond"))
            line = "export PATH=$PATH:"+os.getcwd()
            os.system(line)
        else:
            raise LilypondNotInstalledException('ERROR! Mac edition of Lilypond not in expected folder')

    elif sys.platform == "win32" or sys.platform == "win64":
        if path is None:
            win_path = defaults[1]
        else:
            win_path = path
        if os.path.exists(win_path):
            fob = open("lilypond_windows.bat", "r")
            lines = fob.readlines()
            new_lines = ["SET FOLD="+win_path, lines[0], lines[1]]
            fob.close()
            fob = open("lilypond", "w")
            fob.writelines(new_lines)
            fob.close()
            os.system("icacls lilypond /grant Everyone:F")
        else:
            raise LilypondNotInstalledException('ERROR! Windows edition of Lilypond not in expected folder')

setup_lilypond()
