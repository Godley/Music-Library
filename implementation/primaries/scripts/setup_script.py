import sys, os
from implementation.primaries.exceptions import LilypondNotInstalledException



def setup_lilypond(path="/Applications/Lilypond.app/Contents/Resources/bin/lilypond"):
    if sys.platform == "darwin":
        if os.path.exists('/Applications/Lilypond.app/Contents/Resources/bin/lilypond'):
            fob = open("lilypond_mac.sh", 'r')
            lines = fob.readlines()
            new_lines = [lines[0], "LILYPOND="+path+"\n", lines[1]]
            fob.close()
            fob = open("lilypond", 'w')
            fob.writelines(new_lines)
            fob.close()
            os.system("chmod u+x lilypond")
            line = "export PATH=$PATH:"+os.getcwd()
            os.system(line)
        else:
            raise LilypondNotInstalledException('ERROR! Mac edition of Lilypond not in expected folder')

    elif sys.platform == "win32" or sys.platform == "win64":
        if os.path.exists("C:/Program Files/LilyPond/usr/bin"):
            os.system("icacls lilypond_windows.bat /grant Everyone:F")
            os.rename("lilypond_windows.bat", "lilypond")
        else:
            raise LilypondNotInstalledException('ERROR! Windows edition of Lilypond not in expected folder')

setup_lilypond()
