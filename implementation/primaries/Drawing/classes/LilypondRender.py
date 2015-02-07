import os

class LilypondRender(object):
    def __init__(self, piece_obj, fname, lyscript="/Users/charlottegodley/bin/lilypond"):
        self.piece_obj = piece_obj
        self.file = fname
        self.lyfile = self.file.split(".")[0] + ".ly"
        self.pdf = self.file.split(".")[0] + ".pdf"
        self.folder = "/".join(self.file.split("/")[:-1])
        self.lily_script = lyscript

    def run(self, wrappers=["",""]):
        opened_file = open(self.lyfile, 'w')
        lilystring = self.piece_obj.toLily()
        opened_file.writelines(wrappers[0]+"\\version \"2.18.2\" \n"+lilystring+wrappers[1])
        opened_file.close()
        os.system(self.lily_script + " --output="+self.folder + " "+self.lyfile)

    def cleanup(self, pdf=False):
        if os.path.exists(self.lyfile):
            os.remove(self.lyfile)

        if pdf:
            if os.path.exists(self.pdf):
                os.remove(self.pdf)
