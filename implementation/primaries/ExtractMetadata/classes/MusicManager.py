import os, shutil, sys, zipfile
from xml.sax._exceptions import *

import requests.exceptions

from implementation.primaries.ExtractMetadata.classes import DataLayer, MetaParser, OnlineMetaParser
from implementation.primaries.ImportOnlineDBs.classes import ApiManager
from implementation.primaries.GUI.helpers import get_base_dir
from MuseParse.classes.Output import LilypondOutput
from MuseParse.classes import Exceptions
from MuseParse.classes.Input import MxmlParser


class Unzipper(object):

    def __init__(
            self,
            folder="/Users/charlottegodley/PycharmProjects/FYP",
            files=[]):
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
                try:
                    zip_file = zipfile.ZipFile(path)
                    zip_file.extractall(path=self.folder)
                    file = [
                        f.filename for f in zip_file.filelist if "META-INF" not in f.filename]
                    resulting_file_list.append(file[0])
                except:
                    print("file "+file+" was skipped: exception occurred when unzipping")

        return resulting_file_list

    def unzip(self):
        output_list = self.createOutputList()
        output_paths = [
            os.path.join(
                self.folder,
                file) for file in output_list]
        results = self.unzipInputFiles()
        result_paths = [os.path.join(self.folder, file) for file in results]
        for expected, result, path in zip(output_list, result_paths, output_paths):
            if result != expected and os.path.exists(result):
                os.rename(result, path)

        if os.path.exists(os.path.join(self.folder, 'META-INF')):
            shutil.rmtree(os.path.join(self.folder, 'META-INF'))


class FolderBrowser(object):

    def __init__(
            self,
            db_files=[],
            folder='/Users/charlottegodley/PycharmProjects/FYP'):
        self.db_files = db_files
        self.folder = folder

    def resetDbFileList(self, files):
        self.db_files = files

    def getFolderFiles(self):
        """
        method to search the given folder for all xml and mxl files
        :return: dictionary containing 2 optional indexes - xml and mxl depending whether any exist of either type
        """
        folder_files = {}
        for root, dirs, files in os.walk(self.folder):
            index = len(self.folder)
            substr = root[index+1:]
            for file in files:
                if file.endswith(".xml"):
                    if "xml" not in folder_files:
                        folder_files["xml"] = []
                    folder_files["xml"].append(os.path.join(substr,file))
                if file.endswith(".mxl"):
                    if "mxl" not in folder_files:
                        folder_files["mxl"] = []
                    folder_files["mxl"].append(os.path.join(substr,file))
        return folder_files

    def getZipFiles(self):
        files = self.getFolderFiles()
        if "mxl" in files:
            return files["mxl"]

    def getNewFileList(self):
        """
        method to determine from a list of collected xml files from getFolderFiles which ones are new to the DB
        :return: list of file names which aren't in the db
        """
        files = self.getFolderFiles()
        new_files = []
        if "xml" in files:
            xml_files = files["xml"]
            new_files = [f for f in xml_files if f not in self.db_files]
        return new_files

    def getOldRecords(self):
        """
        method to determine from a list of xml files from getFolderFiles which ones in the DB no
        longer exist in this folder
        :return: list of file names which are in the db but don't exist
        """
        files = self.getFolderFiles()
        old_files = []
        if "xml" in files:
            xml_files = files["xml"]
            old_files = [f for f in self.db_files if f not in xml_files]
        return old_files

    def getNewAndOldFiles(self):
        """
        method which will do both of the above methods without calling self.getFolderFiles twice
        which is probably inefficient
        :return: dict containing new and old files separated by relevant indices
        """
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

    def __init__(self, parent, folder='/Users/charlottegodley/PycharmProjects/FYP'):
        self.parent = parent
        self.folder = folder
        self.__data = DataLayer.MusicData(
            os.path.join(
                self.folder,
                "music.db"))
        self.setupFolderBrowser()
        self.script = os.path.join(get_base_dir(), "scripts", "lilypond")
        if sys.platform.startswith("linux"):
            self.script = ""
        if sys.platform == "win32":
            self.script = os.path.join(get_base_dir(), "scripts", "lilypond_windows.bat")
        self.apiManager = ApiManager.ApiManager(folder=self.folder)

    def startRenderingTask(self, fname):
        """
        method which parses a piece, then runs the renderer class on it which takes the lilypond
        output, runs lilypond on it and gets the pdf. This is not generally called directly,
        but rather called by a thread class in thread_classes.py
        :param fname: xml filename
        :return: list of problems encountered
        """
        errorList = []
        parser = MxmlParser.MxmlParser()
        piece_obj = None

        path_to_file = os.path.join(self.folder, fname)

        try:
            piece_obj = parser.parse(path_to_file)
        except Exceptions.DrumNotImplementedException as e:
            errorList.append(
                "Drum tab found in piece: this application does not handle drum tab.")
        except Exceptions.TabNotImplementedException as e:
            errorList.append(
                "Guitar tab found in this piece: this application does not handle guitar tab.")
        except SAXParseException as e:
            errorList.append("Sax parser had a problem with this file:"+str(e))
        if piece_obj is not None:
            try:
                if sys.platform == "win32":
                    self.script = ""

                loader = LilypondOutput.LilypondRenderer(
                    piece_obj,
                    path_to_file,
                lyscript=self.script)
                loader.run()
                pdfpath = fname.split("/")[-1].split(".")[0] + ".pdf"
                new_path = "/".join(fname.split("/")[:-1])+"/"+pdfpath
                current = os.path.join(os.getcwd(), pdfpath)
                if os.path.exists(current):
                    shutil.copy(current, new_path)
            except BaseException as e:
                errorList.append(str(e))
        return errorList

    def unzipApiFiles(self, data_set):
        """
        method to download API files and unzip them as necessary
        :return: dictionary of results indexed by source name
        """
        results = {}
        try:
            file_set = self.apiManager.downloadFiles(data_set)
            self.handleZips()
            for source in file_set:
                results[source] = []
                for file in file_set[source]:
                    file_path = os.path.join(self.folder, file)
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    n_filename = file.split(".")[0] + ".xml"
                    results[source].append(n_filename)
        except requests.exceptions.ConnectionError as e:
            print(str(e))

        return results

    def parseApiFiles(self):
        """
        method to extract data from apis and parse each created file for metadata
        :return: dictionary of data indexed by filename
        """
        parsing_errors = {}
        result_set = {}
        try:
            cleaned_set = self.apiManager.fetchAllData()
            filelist = self.getFileList(online=True)
            for file in filelist:
                source = self.__data.getPieceSource(file)[0]
                id = file.split(".")[0]
                if id in cleaned_set[source]:
                    cleaned_set[source].pop(id)
            file_set = self.unzipApiFiles(cleaned_set)
            for source in file_set:
                result_set[source] = {}
                for file in file_set[source]:
                    ignore_list = self.apiManager.getSourceIgnoreList(source)
                    parser = OnlineMetaParser.OnlineMetaParser(ignored=ignore_list, source=source)
                    data = self.parseXMLFile(file, parser=parser)
                    path_to_file = os.path.join(self.folder, file)
                    if os.path.exists(path_to_file):
                        os.remove(path_to_file)
                    if type(data) != tuple:
                        result_set[source][file] = data
                        file_id = file.split("/")[-1].split(".")[0]
                        if "title" in cleaned_set[source][file_id]:
                            result_set[source][file]["title"] = cleaned_set[
                                source][file_id]["title"]
                        if "composer" in cleaned_set[source][file_id]:
                            result_set[source][file]["composer"] = cleaned_set[
                                source][file_id]["composer"]

                        if "lyricist" in cleaned_set[source][file_id]:
                            result_set[source][file]["lyricist"] = cleaned_set[
                                source][file_id]["lyricist"]
                        if "secret" in cleaned_set[source][file_id]:
                            result_set[source][file]["secret"] = cleaned_set[source][file_id]["secret"]
                        if "license" in cleaned_set[source][file_id]:
                            result_set[source][file]["license"] = cleaned_set[source][file_id]["license"]
                    else:
                        parsing_errors[data[1]] = data[0]
        except requests.exceptions.ConnectionError as e:
            parsing_errors["Connection"] = "error connecting to the internet. Sources not refreshed."
        if len(parsing_errors) > 0:
            error_string = "".join([error + " : " + parsing_errors[error] for error in parsing_errors])
            self.parent.errorPopup(error_string)
        return result_set

    def addApiFiles(self, data):
        for source in data:
            for file in data[source]:
                self.addPiece(file, data[source][file])

    def cleanupApiFiles(self, data, extensions=['mxl', 'xml']):
        for source in data:
            for file in data[source]:
                for ext in extensions:
                    file_ext = file.split(".")[0]+"."+ext
                    if os.path.exists(os.path.join(self.folder, file_ext)):
                        os.remove(os.path.join(self.folder, file_ext))

    def downloadFile(self, filename):
        file_info = filename.split(".")
        fname = file_info[0]
        source = self.__data.getPieceSource(filename)
        if source is not None:
            source = source[0]
        secret = self.__data.getSecret(filename)
        if secret is not None:
            secret = secret[0]
        try:
            status_code = self.apiManager.downloadFile(source=source, file=fname, secret=secret, extension='pdf')
            if status_code == 200:
                self.__data.downloadPiece(filename)
                return True
        except requests.exceptions.ConnectionError as e:
            print("Error downloading file!")
        return False


    def runApiOperation(self):
        """
        method which gets all the data from the apis, unzips them,
        parses them for data, puts the data in the database and finally
        deletes the files
        :return:
        """
        result_set = self.parseApiFiles()
        self.addApiFiles(result_set)
        #self.cleanupApiFiles(result_set)


    def addPiece(self, filename, data):
        self.__data.addPiece(filename, data)

    def getPieceInfo(self, filenames):
        return self.__data.getAllPieceInfo(filenames)

    def getFileList(self, online=False):
        return self.__data.getFileList(online=online)

    def setupFolderBrowser(self):
        db_files = self.__data.getFileList()
        self.folder_browser = FolderBrowser(
            db_files=db_files,
            folder=self.folder)

    def handleZips(self):
        zip_files = self.folder_browser.getZipFiles()
        if zip_files is not None:
            unzipper = Unzipper(folder=self.folder, files=zip_files)
            unzipper.unzip()

    def refresh(self):
        self.runApiOperation()
        self.refreshWithoutDownload()


    def refreshWithoutDownload(self):
        db_files = self.__data.getFileList()
        self.folder_browser.resetDbFileList(db_files)
        self.handleZips()
        self.handleXMLFiles()

    def getPieceSummary(self, file_list, sort_method="title", online=False):
        info = self.__data.getAllPieceInfo(file_list, online=online)
        summaries = [{"title": i["title"],
                      "composer":i["composer"],
                      "lyricist":i["lyricist"],
                      "filename":i["filename"]} for i in info]
        results = sorted(summaries, key=lambda k: str(k[sort_method]))
        summary_strings = []
        for result in results:
            summary = ""
            if result["title"] is not None and result["title"] != "":
                summary += result["title"]
            else:
                summary += "(noTitle)"
            if result["composer"] != -1 or result["lyricist"] != -1:
                summary += " by "
            if result["composer"] != -1:
                summary += result["composer"]
            if result["lyricist"] != -1:
                summary += ", " + result["lyricist"]
            summary += "(" + result["filename"] + ")"
            summary_strings.append((summary, result["filename"]))
        return summary_strings

    def getLicense(self, filename):
        result = self.__data.getLicense(filename)
        # eventually we should open up a file and get the text based on the license name,
        # but for now we need to do this
        if result is not None:
            result = result[0]
            folder = '/users/charlottegodley/PycharmProjects/FYP/implementation/primaries' \
                     '/ImportOnlineDBs/licenses'
            file = os.path.join(folder, result)
            if os.path.exists(file):
                fob = open(file, 'r')
                lines = fob.readlines()
                result = "\n".join(lines)

        return result

    def getPieceSummaryStrings(self, sort_method="title"):
        file_list = self.__data.getFileList()
        summary_strings = self.getPieceSummary(
            file_list,
            sort_method=sort_method)

        return summary_strings

    def parseOldFiles(self, file_list):
        """
        method to remove or archive all the files in the list within the db
        :param file_list: files to archive
        :return: None
        """
        self.__data.archivePieces(file_list)

    def parseXMLFile(self, filename, parser=None):
        errorTuple = []
        if parser is None:
            parser = MetaParser.MetaParser()
        try:
            data_set = parser.parse(os.path.join(self.folder, filename))
            return data_set
        except SAXException as e:
            errorTuple.append(str(e))
            errorTuple.append(filename)
            return tuple(errorTuple)


    def parseError(self, exception):
        string_val = str(exception)
        self.parent.errorPopup(string_val)

    def parseNewFiles(self, file_list):
        """
        method to call the sax parser on each of the new files then send the data to the data layer
        :param file_list:
        :return:
        """
        for file in file_list:
            data_set = self.parseXMLFile(file)
            self.__data.addPiece(file, data_set)

    def handleXMLFiles(self):
        """
        method to get all the new and old files from the folder browser and call parseNew and parseOld methods
        :return:
        """
        files = self.folder_browser.getNewAndOldFiles()
        if "new" in files:
            self.parseNewFiles(files["new"])
        if "old" in files:
            self.parseOldFiles(files["old"])

    def runQueries(self, search_data, online=False):
        results = {}
        all_matched = True

        if "text" in search_data:
            # check title, composer, lyricist, instruments for matches
            for value in search_data["text"]:
                combined = {}
                file_result = self.__data.getRoughPiece(value, online=online)
                if len(file_result) > 0:
                    combined["filename"] = [result[1]
                                            for result in file_result]

                title_result = self.__data.getPieceByTitle(value, online=online)
                if len(title_result) > 0:
                    combined["Title"] = title_result

                composer_result = self.__data.getPiecesByComposer(value, online=online)
                if len(composer_result) > 0:
                    combined["Composer"] = composer_result

                lyricist_result = self.__data.getPiecesByLyricist(value, online=online)
                if len(lyricist_result) > 0:
                    combined["Lyricist"] = lyricist_result

                instrument_result = self.__data.getPiecesByInstruments([value], online=online)
                if len(instrument_result) > 0:
                    combined["Instruments"] = instrument_result

                if len(combined) > 0:
                    results.update(combined)
                else:
                    all_matched = False

        if "instrument" in search_data:
            result_data = {}
            if "key" in search_data:
                for instrument in search_data["instrument"]:
                    if instrument not in search_data["key"]:
                        result_data[instrument] = search_data[
                            "instrument"][instrument]
            if "clef" in search_data:
                for instrument in search_data["instrument"]:
                    if instrument not in search_data["clef"]:
                        result_data[instrument] = search_data[
                            "instrument"][instrument]
            elif "key" not in search_data and "clef" not in search_data:
                result_data = search_data["instrument"]
            if len(result_data) > 0:
                instrument_data = self.__data.getPiecesByInstruments(
                    result_data, online=online)
                if len(instrument_data) > 0:
                    results["Instruments"] = instrument_data
                else:
                    all_matched = False

        if "tempo" in search_data:
            tempo_data = self.__data.getPieceByTempo(search_data["tempo"], online=online)
            if len(tempo_data) > 0:
                results["Tempo"] = tempo_data
            else:
                all_matched = False

        if "time" in search_data:
            time_data = self.__data.getPieceByMeter(search_data["time"], online=online)
            if len(time_data) > 0:
                results["Time Signatures"] = time_data
            else:
                all_matched = False

        if "key" in search_data:
            if "other" in search_data["key"]:
                keydata = self.__data.getPieceByKeys(
                    search_data["key"]["other"], online=online)
                if len(keydata) > 0:
                    results["Keys"] = keydata
                else:
                    all_matched = False
                search_data["key"].pop("other")
            if len(search_data["key"]) > 0:
                new_results = self.__data.getPieceByInstrumentInKeys(
                    search_data["key"], online=online)
                if len(new_results) > 0:
                    results["Instruments in Keys"] = new_results
                else:
                    all_matched = False

        if "transposition" in search_data:
            transpos = self.__data.getPieceByInstrumentsOrSimilar(
                search_data["transposition"], online=online)
            if len(transpos) > 0:
                results["Instrument or transposition"] = transpos
            else:
                all_matched = False

        if "clef" in search_data:
            if "other" in search_data["clef"]:
                clefs = self.__data.getPieceByClefs(
                    search_data["clef"]["other"], online=online)
                if len(clefs) > 0:
                    results["Clefs"] = clefs
                else:
                    all_matched = False
                search_data["clef"].pop("other")

            if len(search_data["clef"]) > 0:
                instrument_by_clef = self.__data.getPieceByInstrumentInClefs(
                    search_data["clef"], online=online)
                if len(instrument_by_clef) > 0:
                    results["Instrument in Clefs"] = instrument_by_clef
                else:
                    all_matched = False

        if "filename" in search_data:
            # todo: implement wildcard functionality
            files = self.__data.getFileList(online=online)
            result_files = [
                filename for filename in search_data["filename"] if filename in files]
            if len(result_files) > 0:
                results["Filename"] = result_files
            else:
                all_matched = False

        if "title" in search_data:
            files = {}
            for title in search_data["title"]:
                file_list = self.__data.getPieceByTitle(title, online=online)
                if len(file_list) > 0:
                    files["Title: " + title] = file_list
            if len(files) > 0:
                results.update(files)
            else:
                all_matched = False

        if "composer" in search_data:
            files = {}
            for title in search_data["composer"]:
                file_list = self.__data.getPiecesByComposer(title, online=online)
                if len(file_list) > 0:
                    files["Composer: " + title] = file_list
            if len(files) > 0:
                results.update(files)
            else:
                all_matched = False

        if "lyricist" in search_data:
            files = {}
            for title in search_data["lyricist"]:
                file_list = self.__data.getPiecesByLyricist(title, online=online)
                if len(file_list) > 0:
                    files["Lyricist: " + title] = file_list
            if len(files) > 0:
                results.update(files)
            else:
                all_matched = False

        summaries = {}
        if len(results) > 0:
            if all_matched:
                intersection = set.intersection(
                    *[set(results[key]) for key in results])
                if len(intersection) > 0:
                    results["Exact Matches"] = intersection
            for key in results:
                summaries[key] = self.getPieceSummary(results[key], online=online)
        return summaries

    def getPlaylistFileInfo(self, playlist):
        data = self.__data.getAllPieceInfo(playlist)
        return data

    def getFileInfo(self, filename):
        data = self.__data.getAllPieceInfo([filename])
        return data

    def updatePlaylistTitle(self, new_title, old_title):
        row_id = self.__data.getUserPlaylist(old_title)
        data = {"title": new_title}
        self.__data.updateUserPlaylist(row_id, data)

    def getPlaylistByFilename(self, filename):
        data = self.__data.getUserPlaylistsForFile(filename)
        return data

    def getPlaylists(self, select_method="all"):
        result_set = {}
        if select_method == "all":
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

        if select_method == "clefs":
            clefs = self.__data.getPiecesByAllClefs()
            if len(clefs) > 0:
                result_set["clefs"] = clefs

        if select_method == "time signatures":
            timesigs = self.__data.getPiecesByAllTimeSigs()
            if len(timesigs) > 0:
                result_set["time_signatures"] = timesigs

        if select_method == "keys":
            keys = self.__data.getPiecesByAllKeys()
            if len(keys) > 0:
                result_set["keys"] = keys

        if select_method == "instruments":
            instruments = self.__data.getPiecesByAllInstruments()
            if len(instruments) > 0:
                result_set["instruments"] = instruments

        if select_method == "tempos":
            tempos = self.__data.getPiecesByAllTempos()
            if len(tempos) > 0:
                result_set["tempos"] = tempos

        return result_set

    def copyFiles(self, filenames):
        """
        method to copy a list of files from one folder to another
        :param filenames: list of files including extension and folder
        :return: none
        """
        for file in filenames:
            folder_file_split = file.split("/")
            f = folder_file_split[-1]
            shutil.copyfile(file, os.path.join(self.folder, f))

    def getPlaylistsFromPlaylistTable(self):
        data = self.__data.getAllUserPlaylists()
        return data

    def addPlaylist(self, data):
        self.__data.addPlaylist(data["name"], data["pieces"])

    def deletePlaylists(self, names):
        [self.__data.deletePlaylist(name) for name in names]
