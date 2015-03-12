import os
import zipfile

class Unzipper(object):
    def __init__(self, folder="/Users/charlottegodley/PycharmProjects/FYP", files=[]):
        self.folder = folder
        self.files = files

    def createOutputList(self):
        result = [file.split('.')[0] + ".xml" for file in self.files]
        return result

    def unzipInputFiles(self):
        resulting_file_list = []
        for file in self.files:
            path = os.path.join(self.folder, file)
            if os.path.exists(path):
                zip_file = zipfile.ZipFile(path)
                zip_file.extractall(path=self.folder)
                file = [f.filename for f in zip_file.filelist if "META-INF" not in f.filename]
                resulting_file_list.append(file[0])
        return resulting_file_list


    def unzip(self):
        output_list = self.createOutputList()
        output_paths = [os.path.join(self.folder, file) for file in output_list]
        results = self.unzipInputFiles()
        for expected, result, path in zip(output_list, results, output_paths):
            if result != expected:
                os.rename(os.path.join(self.folder, result), path)


