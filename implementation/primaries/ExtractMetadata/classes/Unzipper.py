import os, zipfile
class Unzipper(object):
    def __init__(self, zip_folder=None, dest=None):
        self.folder = zip_folder
        self.fileList = []
        self.dest = dest

    def Load(self):
        for file in os.listdir(self.folder):
            if file.endswith('mxl'):
                self.fileList.append(file)

    def Unzip(self):
        files = [zipfile.ZipFile(os.path.join(self.folder, f)) for f in self.fileList]

        for zipper in files:
            names = zipper.namelist()
            to_unzip = None
            for name in names:
                if "/" not in name:
                    to_unzip = name
            extract_dest_file = to_unzip.split('.')[0] + '.xml'
            zipper.extract(to_unzip, self.dest)