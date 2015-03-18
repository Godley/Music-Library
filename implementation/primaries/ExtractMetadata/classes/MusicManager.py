import os, shutil
import zipfile
from implementation.primaries.ExtractMetadata.classes import DataLayer, MetaParser

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

        if os.path.exists(os.path.join(self.folder, 'META-INF')):
            shutil.rmtree(os.path.join(self.folder, 'META-INF'))

class FolderBrowser(object):
    def __init__(self, db_files=[], folder='/Users/charlottegodley/PycharmProjects/FYP'):
        self.db_files = db_files
        self.folder = folder

    def resetDbFileList(self, files):
        self.db_files = files

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

    def getZipFiles(self):
        files = self.getFolderFiles()
        if "mxl" in files:
            return files["mxl"]

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
    def __init__(self, folder='/Users/charlottegodley/PycharmProjects/FYP'):
        self.folder = folder
        self.__data = DataLayer.MusicData(os.path.join(self.folder, "music.db"))
        self.setupFolderBrowser()

    def addPiece(self, filename, data):
        self.__data.addPiece(filename, data)

    def getPieceInfo(self, filenames):
        return self.__data.getAllPieceInfo(filenames)

    def getFileList(self):
        return self.__data.getFileList()

    def setupFolderBrowser(self):
        db_files = self.__data.getFileList()
        self.folder_browser = FolderBrowser(db_files=db_files, folder=self.folder)

    def handleZips(self):
        zip_files = self.folder_browser.getZipFiles()
        if zip_files is not None:
            unzipper = Unzipper(folder=self.folder, files=zip_files)
            unzipper.unzip()

    def refresh(self):
        db_files = self.__data.getFileList()
        self.folder_browser.resetDbFileList(db_files)
        self.handleZips()
        self.handleXMLFiles()

    def getPieceSummaryStrings(self, sort_method="title"):
        file_list = self.__data.getFileList()
        info = self.__data.getAllPieceInfo(file_list)
        summaries = [{"title":i["title"], "composer":i["composer"],"lyricist":i["lyricist"],
                      "filename":i["filename"]} for i in info]
        results = sorted(summaries, key=lambda k: str(k[sort_method]))
        summary_strings = []
        for result in results:
            summary = result["title"]
            if result["title"] == "":
                summary = "(noTitle)"
            if result["composer"] != -1 or result["lyricist"] != -1:
                summary += " by "
            if result["composer"] != -1:
                summary += result["composer"]
            if result["lyricist"] != -1:
                summary += ", "+result["lyricist"]
            summary += "("+result["filename"]+")"
            summary_strings.append((summary,result["filename"]))

        return summary_strings


    def parseOldFiles(self, file_list):
        '''
        method to remove or archive all the files in the list within the db
        :param file_list:
        :return:
        '''
        self.__data.archivePieces(file_list)

    def parseXMLFile(self, filename):
        parser = MetaParser.MetaParser()
        data_set = parser.parse(os.path.join(self.folder,filename))
        return data_set

    def parseNewFiles(self, file_list):
        '''
        method to call the sax parser on each of the new files then send the data to the data layer
        :param file_list:
        :return:
        '''
        for file in file_list:
            data_set = self.parseXMLFile(file)
            self.__data.addPiece(file, data_set)

    def handleXMLFiles(self):
        '''
        method to get all the new and old files from the folder browser and call parseNew and parseOld methods
        :return:
        '''
        files = self.folder_browser.getNewAndOldFiles()
        if "new" in files:
            self.parseNewFiles(files["new"])
        if "old" in files:
            self.parseOldFiles(files["old"])

    def getFileInfo(self, filename):
        data = self.__data.getAllPieceInfo([filename])
        return data

    def getPlaylists(self):
        result_set = {}
        clefs = self.__data.getPiecesByAllClefs()
        keys = self.__data.getPiecesByAllKeys()
        composers = self.__data.getPiecesByAllComposers()
        lyricists = self.__data.getPiecesByAllLyricists()
        instruments = self.__data.getPiecesByAllInstruments()
        timesigs = self.__data.getPiecesByAllTimeSigs()
        tempos = self.__data.getPiecesByAllTempos()
        if len(clefs) > 0:
            result_set["clefs"] = clefs
        if len(keys) > 0:
            result_set["keys"] = keys
        if len(composers) > 0:
            result_set["composers"] = composers
        if len(lyricists) > 0:
            result_set["lyricsts"] = lyricists
        if len(instruments) > 0:
            result_set["instruments"] = instruments
        if len(timesigs) > 0:
            result_set["time_signatures"] = timesigs
        if len(tempos) > 0:
            result_set["tempos"] = tempos
        return result_set

    def getPlaylistsFromPlaylistTable(self):
        data = self.__data.getAllUserPlaylists()
        return data

    def addPlaylist(self, data):
        self.__data.addPlaylist(data["name"], data["pieces"])

