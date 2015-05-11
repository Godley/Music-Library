import sys, os
def setup_lilypond():
    if sys.platform == "darwin":
        os.system("chmod u+x lilypond_mac.sh")
        os.rename("lilypond_mac.sh", "lilypond")
        line = "export PATH=$PATH:"+os.getcwd()
        os.system(line)
    elif sys.platform == "win32" or sys.platform == "win64":
        os.system("icacls lilypond_windows.bat /grant Everyone:F")
        os.rename("lilypond_windows.bat", "lilypond")
