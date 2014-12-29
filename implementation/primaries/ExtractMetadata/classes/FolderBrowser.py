import os, shutil

class Browser(object):
    def __init__(self, folder=None):
        self.folder = folder
        self.zipped_folder = os.path.join(folder, "zipped")
        self.xmlFiles = []
        self.mxlFiles = []
        self.i = 0

    def Load(self):
        for file in os.listdir(self.folder):
            if file.endswith('xml'):
                if file not in self.xmlFiles:
                    self.xmlFiles.append(file)
            if file.endswith('mxl'):
                if os.path.exists(os.path.join(self.folder, file)):
                    if file not in self.mxlFiles:
                        self.mxlFiles.append(file)

    def CopyZippedFiles(self):
        zipFolder = os.path.join(self.folder, "zipped")
        if not os.path.exists(os.path.join(self.folder, "zipped")):
            os.mkdir(zipFolder)
        for file in self.mxlFiles:
            path = os.path.join(self.folder, file)
            dest = os.path.join(self.folder, "zipped", file)
            if not os.path.exists(dest):
                shutil.copyfile(path, dest)

    def removeCopiedFilesFromMainFolder(self):
        zipped_paths = [os.path.join(self.zipped_folder, file) for file in self.mxlFiles]
        main_paths = [os.path.join(self.folder, file) for file in self.mxlFiles]
        [os.remove(path) for path in main_paths if os.path.exists(path)]
        self.mxlFiles = []
