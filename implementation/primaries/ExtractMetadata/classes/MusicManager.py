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

class FolderBrowser(object):
    def __init__(self, db_files=[], folder='/Users/charlottegodley/PycharmProjects/FYP'):
        self.db_files = db_files
        self.folder = folder

    def getFolderFiles(self):
        '''
        method to search the given folder for all xml and mxl files
        :return: dictionary containing 2 optional indexes - xml and mxl depending whether any exist of either type
        '''
        folder_files = {}
        for root, dirs, files in os.walk(self.folder):
            for file in files:
                if file.endswith(".xml"):
                    if "xml" not in folder_files:
                        folder_files["xml"] = []
                    folder_files["xml"].append(file)
                if file.endswith(".mxl"):
                    if "mxl" not in folder_files:
                        folder_files["mxl"] = []
                    folder_files["mxl"].append(file)
        return folder_files

    def getNewFileList(self):
        '''
        method to determine from a list of collected xml files from getFolderFiles which ones are new to the DB
        :return: list of file names which aren't in the db
        '''
        files = self.getFolderFiles()
        new_files = []
        if "xml" in files:
            xml_files = files["xml"]
            new_files = [f for f in xml_files if f not in self.db_files]
        return new_files

    def getOldRecords(self):
        '''
        method to determine from a list of xml files from getFolderFiles which ones in the DB no longer exist in this folder
        :return: list of file names which are in the db but don't exist
        '''
        files = self.getFolderFiles()
        old_files = []
        if "xml" in files:
            xml_files = files["xml"]
            old_files = [f for f in self.db_files if f not in xml_files]
        return old_files

    def getNewAndOldFiles(self):
        '''
        method which will do both of the above methods without calling self.getFolderFiles twice which is probably inefficient
        :return: dict containing new and old files separated by relevant indices
        '''
        files = self.getFolderFiles()
        result_set = {}
        if "xml" in files:
            xml_files = files["xml"]
            old_files = [f for f in self.db_files if f not in xml_files]
            new_files = [f for f in xml_files if f not in self.db_files]
            result_set["old"] = old_files
            result_set["new"] = new_files
        return result_set

class MusicManager(object):
    pass

