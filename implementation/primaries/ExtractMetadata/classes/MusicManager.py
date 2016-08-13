import os, shutil, zipfile, logging
from xml.sax._exceptions import *

import requests.exceptions


from implementation.primaries.ExtractMetadata.classes import MusicData, MetaParser, OnlineMetaParser
from implementation.primaries.ImportOnlineDBs.classes import ApiManager
from implementation.primaries.ExtractMetadata.classes.DataLayer.helpers import filter_dict, get_if_exists
from MuseParse.classes.Output import LilypondOutput
from MuseParse.classes import Exceptions
from MuseParse.classes.Input import MxmlParser
from Application import LOG_NAME
import logging

logger = logging.getLogger(LOG_NAME)

class Unzipper(object):
    """
    This class pretty much does what it says on the tin - takes a list of input files and unzips them all.
    Works only with mxl which is the default zip type for music xml
    """

    def __init__(
            self,
            folder="/Users/charlottegodley/PycharmProjects/FYP",
            files=[]):
        self.folder = folder
        """path to the folder where the music collection is stored"""
        self.files = files
        """list of mxl files to unzip"""

    def createOutputList(self):
        """
        Takes the file list (self.file) and produces their outputs with the xml extension

        Return value: list of xml files
        """
        result = [file.split('.')[0] + ".xml" for file in self.files]
        return result

    def unzipInputFiles(self):
        '''
        Method which takes self.files and iterates each one, producing a ZipFile class and extracting the files.
        It will then remove the unnecessary meta-inf folder and add the file to the result list if it managed to unzip
        it without issues.

        Return value: list of unzipped xml files
        '''
        resulting_file_list = []
        for file in self.files:
            path = os.path.join(self.folder, file)
            if os.path.exists(path):
                try:
                    zip_file = zipfile.ZipFile(path)
                    zip_file.extractall(path=self.folder)
                    file = list(filter(lambda k: "META-INF" not in k.filename, zip_file.filelist))
                    file = file[0].filename
                    resulting_file_list.append(file)
                    zip_file.close()
                except Exception as e:
                    logging.log(logging.ERROR, "file " + file + " was skipped: "+str(e))

        return resulting_file_list

    def unzip(self):
        """
        Method which pulls together the above two methods and renames each output file to match what it should be
        on input.

        Return value: None
        """
        output_list = self.createOutputList()
        results = self.unzipInputFiles()
        for expected, result in zip(output_list, results):
            output_path = os.path.join(self.folder, expected)
            result_path = os.path.join(self.folder, result)
            self.rename_output(result_path, output_path)


        if os.path.exists(os.path.join(self.folder, 'META-INF')):
            shutil.rmtree(os.path.join(self.folder, 'META-INF'))

    def rename_output(self, input_path, output_path):
        if input_path != output_path and os.path.exists(input_path):
            if os.path.exists(output_path):
                os.remove(output_path)
            try:
                os.rename(input_path, output_path)
            except Exception as e:
                logger.exception("File %s was skipped from renaming: %s" % (input_path, str(e)))

class FolderBrowser(object):
    """
    Class which takes a folder and a list of files in the database and produces 3 lists:

    - new files: files which aren't in the database but exist in the folder
    - old files: files which are in the database but no longer exist in the folder
    - zip files: files which end in the extension .mxl

    Works only with xml files and mxl files.
    """

    def __init__(
            self,
            db_files=[],
            folder='/Users/charlottegodley/PycharmProjects/FYP'):
        self.db_files = db_files
        """A list of files in the database"""
        self.folder = folder
        """the folder in which the collection is stored"""

    def resetDbFileList(self, files):
        self.db_files = files

    def getFolderFiles(self, extensions=['xml', 'mxl']):
        """
        method to search the given folder for all xml and mxl files

        Return value: dictionary containing 2 optional indexes - xml and mxl depending whether any exist of either type
        """
        folder_files = {}
        for root, dirs, files in os.walk(self.folder):
            index = len(self.folder)
            substr = root[index + 1:]
            for file in files:
                ending = file.split(".")[-1]
                if ending in extensions:
                    if ending not in folder_files:
                        folder_files[ending] = []
                    folder_files[ending].append(os.path.join(substr, file))
        return folder_files

    def getZipFiles(self):
        """Method which takes the result of the above method and returns only the zip files from that method"""
        files = self.getFolderFiles()
        if "mxl" in files:
            return files["mxl"]

    def getNewFileList(self, files):
        """
        method to determine from a list of collected xml files from getFolderFiles which ones are new to the DB

        Return value: list of file names which aren't in the db
        """
        new_files = []
        if "xml" in files:
            xml_files = files["xml"]
            new_files = [f for f in xml_files if f not in self.db_files]
        return new_files

    def getOldRecords(self, files):
        """
        method to determine from a list of xml files from getFolderFiles which ones in the DB no longer exist in this
        folder.

        Return value: list of file names which are in the db but don't exist
        """
        old_files = []
        if "xml" in files:
            xml_files = files["xml"]
            old_files = [f for f in self.db_files if f not in xml_files]
        return old_files

    def getNewAndOldFiles(self, files):
        """
        method which will do both of the above methods without calling self.getFolderFiles twice
        which is probably inefficient

        Return value: dict containing new and old files separated by relevant indices
        """
        result_set = {"new": self.getNewFileList(files), "old": self.getOldRecords(files)}
        return result_set

class QueryLayer(object):
    def __init__(self, folder):
        self.folder = folder
        self._data = MusicData(
            os.path.join(
                self.folder,
                "music.db"))

    def getPlaylistsFromPlaylistTable(self):
        data = self._data.getAllUserPlaylists()
        return data

    def addPlaylist(self, data):
        self._data.addPlaylist(data["name"], data["pieces"])

    def deletePlaylists(self, names):
        [self._data.deletePlaylist(name) for name in names]



    def handleTextQueries(self, search_data, online=False):
        # check title, composer, lyricist, instruments for matches
        results = {}
        all_matched = True
        instruments = self._data.getInstrumentNames()
        instrument_list = []
        for value in search_data["text"]:
            combined = {}
            file_result = self._data.getRoughPiece(value, online=online)
            combined["filename"] = file_result

            title_result = self._data.getPieceByTitle(
                value, online=online)
            combined["Title"] = title_result

            composer_result = self._data.getPiecesByComposer(
                value, online=online)
            combined["Composer"] = composer_result

            lyricist_result = self._data.getPiecesByLyricist(
                value, online=online)
            combined["Lyricist"] = lyricist_result

            if value in instruments:
                instrument_list.append(value)

            combined = filter_dict(combined)
            if len(combined) > 0:
                results.update(combined)
            else:
                all_matched = False

        if len(search_data['text']) == len(instrument_list):
            all_matched = True

        if len(instrument_list) > 0:
            instrument_result = self._data.getPiecesByAnyAndAllInstruments(
                instrument_list, online=online)
            if len(instrument_result) > 0:
                results.update(instrument_result)
                if "All Instruments" not in results:
                    all_matched = False
        return results, all_matched

    def handleInstrumentQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        result_data = {}


        for instrument in search_data["instrument"]:
            if "key" in search_data:
                if instrument not in search_data["key"]:
                    result_data[instrument] = search_data[
                        "instrument"][instrument]
            if "clef" in search_data:
                if instrument not in search_data["clef"]:
                    result_data[instrument] = search_data[
                        "instrument"][instrument]

        if "key" not in search_data and "clef" not in search_data:
            result_data = search_data["instrument"]
        if len(result_data) > 0:
            instrument_data = self._data.getPiecesByInstruments(
                result_data, online=online)
            if len(instrument_data) > 0:
                results["Instruments"] = instrument_data
            else:
                all_matched = False
        return results, all_matched

    def handleTempoQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        tempo_data = self._data.getPieceByTempo(
                search_data["tempo"], online=online)
        if len(tempo_data) > 0:
            results["Tempo"] = tempo_data
        else:
            all_matched = False
        return results, all_matched

    def handleTimeQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        time_data = self._data.getPieceByMeter(
            search_data["time"], online=online)
        if len(time_data) > 0:
            results["Meter/Time signature"] = time_data
        else:
            all_matched = False
        return results, all_matched

    def handleKeyQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        if "other" in search_data["key"]:
            keydata = self._data.getPieceByKeys(
                search_data["key"]["other"], online=online)
            if len(keydata) > 0:
                results["Keys"] = keydata
            else:
                all_matched = False
            search_data["key"].pop("other")
        if len(search_data["key"]) > 0:
            new_results = self._data.getPieceByInstrumentInKeys(
                search_data["key"], online=online)
            if len(new_results) > 0:
                results["Instruments in Keys"] = new_results
            else:
                all_matched = False
        return results, all_matched

    def handleTranspositionQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        transpos = self._data.getPieceByInstrumentsOrSimilar(
                search_data["transposition"], online=online)
        if len(transpos) > 0:
            results["Instrument or transposition"] = transpos
        else:
            all_matched = False
        return results, all_matched

    def handleClefQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        if "other" in search_data["clef"]:
            clefs = self._data.getPieceByClefs(
                search_data["clef"]["other"], online=online)
            if len(clefs) > 0:
                results["Clefs"] = clefs
            else:
                all_matched = False
            search_data["clef"].pop("other")
        if len(search_data["clef"]) > 0:
            instrument_by_clef = self._data.getPieceByInstrumentInClefs(
                search_data["clef"], online=online)
            if len(instrument_by_clef) > 0:
                results["Instrument in Clefs"] = instrument_by_clef
            else:
                all_matched = False
        return results, all_matched

    def handleFilenameQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        files = self._data.getFileList(online=online)
        result_files = [
            filename for filename in search_data["filename"] if filename in files]
        if len(result_files) > 0:
            results["Filename"] = result_files
        else:
            all_matched = False
        return results, all_matched

    def handleTitleQueries(self, search_data, online=False):
        results = {}
        files = {}
        all_matched = True
        for title in search_data["title"]:
            file_list = self._data.getPieceByTitle(title, online=online)
            if len(file_list) > 0:
                files["Title: " + title] = file_list
        if len(files) > 0:
            results.update(files)
        else:
            all_matched = False
        return results, all_matched

    def handleComposerQueries(self, search_data, online=False):
        files = {}
        results = {}
        all_matched = True
        for title in search_data["composer"]:
            file_list = self._data.getPiecesByComposer(
                title, online=online)
            if len(file_list) > 0:
                files["Composer: " + title] = file_list
        if len(files) > 0:
            results.update(files)
        else:
            all_matched = False
        return results, all_matched

    def handleLyricistQueries(self, search_data, online=False):
        files = {}
        results = {}
        all_matched = True
        for title in search_data["lyricist"]:
            file_list = self._data.getPiecesByLyricist(
                title, online=online)
            if len(file_list) > 0:
                files["Lyricist: " + title] = file_list
        if len(files) > 0:
            results.update(files)
        else:
            all_matched = False
        return results, all_matched

    def runQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        method_table = {"text": self.handleTextQueries, "instrument": self.handleInstrumentQueries,
                        "tempo": self.handleTempoQueries, "time": self.handleTimeQueries,
                        "key": self.handleKeyQueries, "transposition": self.handleTranspositionQueries,
                        "clef": self.handleClefQueries, "filename": self.handleFilenameQueries,
                        "title": self.handleTitleQueries, "composer": self.handleComposerQueries,
                        "lyricist": self.handleLyricistQueries}

        for key in search_data:
            key_result, all_matched = method_table[key](search_data, online=online)
            results.update(key_result)



        summaries = {}
        if all_matched:
            intersection = set.intersection(
                *[set(results[key]) for key in results])
            results["Exact Matches"] = intersection
        for key in results:
            summaries[key] = self.getPieceSummary(
                filter(None, results[key]), online=online)
        return summaries

    def getPlaylistFileInfo(self, playlist):
        data = self._data.getAllPieceInfo(playlist)
        return data

    def getFileInfo(self, filename):
        data = self._data.getAllPieceInfo([filename])
        return data

    def updatePlaylistTitle(self, new_title, old_title):
        row_id = self._data.getUserPlaylist(old_title)
        data = {"title": new_title}
        self._data.updateUserPlaylist(row_id, data)

    def getPlaylistByFilename(self, filename):
        data = self._data.getUserPlaylistsForFile(filename)
        return data

    def getPlaylists(self, select_method="all"):
        result_set = {}
        playlist_table = {"clefs": self._data.getPiecesByAllClefs,
                          "time signatures": self._data.getPiecesByAllTimeSigs,
                          "keys": self._data.getPiecesByAllKeys,
                          "instruments": self._data.getPiecesByAllInstruments,
                          "tempos": self._data.getPiecesByAllTempos}
        if select_method == "all":
            clefs = self._data.getPiecesByAllClefs()
            keys = self._data.getPiecesByAllKeys()
            composers = self._data.getPiecesByAllComposers()
            lyricists = self._data.getPiecesByAllLyricists()
            instruments = self._data.getPiecesByAllInstruments()
            timesigs = self._data.getPiecesByAllTimeSigs()
            tempos = self._data.getPiecesByAllTempos()
            result_set["clefs"] = clefs
            result_set["keys"] = keys
            result_set["composers"] = composers
            result_set["lyricsts"] = lyricists
            result_set["instruments"] = instruments
            result_set["time_signatures"] = timesigs
            result_set["tempos"] = tempos

        else:
            result_set[select_method] = playlist_table[select_method]()

        return filter_dict(result_set)

class MusicManager(QueryLayer):
    """
    Grand master class which pulls together features from every other class. This class is instantiated by the Application
    class and should provide methods for the application to access everything else, from rendering to info extraction
    to API access.
    """

    def __init__(self, parent, folder='/Users/charlottegodley/PycharmProjects/FYP'):
        self.parent = parent
        """the application instance in which this manager resides"""
        self.wifi = True
        super(MusicManager, self).__init__(folder)
        self.apiManager = ApiManager.ApiManager(folder=self.folder)
        self.setupFolderBrowser()

    def updateWifi(self, wifi):
        self.apiManager.wifi = wifi

    def addInstruments(self, data):
        self._data.addInstruments(data)

    def startRenderingTask(self, fname):
        """
        method which parses a piece, then runs the renderer class on it which takes the lilypond
        output, runs lilypond on it and gets the pdf. This is not generally called directly,
        but rather called by a thread class in thread_classes.py

        * Parameter fname: xml filename

        * Return value: list of problems encountered
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
            logger.exception("Drum tab found in piece:{} - {}".format(fname, str(e)))
        except Exceptions.TabNotImplementedException as e:
            errorList.append(
                "Guitar tab found in this piece: this application does not handle guitar tab.")
            logger.exception("Guitar tab found in piece:{} - {}".format(fname, str(e)))
        except SAXParseException as e:
            errorList.append(
                "Sax parser had a problem with this file:" + str(e))
            logger.exception("Exception SAX parsing file:{} - {}".format(fname, str(e)))

        try:
            loader = LilypondOutput.LilypondRenderer(
                piece_obj,
                os.path.join(
                    self.folder,
                    fname))
            loader.run()
        except BaseException as e:
            errorList.append(str(e))
            logger.exception("Exception rendering lilypond with file:{} - {}".format(fname, str(e)))
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
            logger.exception("Exception connecting to api to download files:{}".format(str(e)))

        return results

    def getNewFiles(self):
        cleaned_set = self.apiManager.fetchAllData()
        filelist = self.getFileList(online=True)
        for file in filelist:
            source = self._data.getPieceSource(file)[0]
            id = file.split(".")[0]
            if id in cleaned_set[source]:
                cleaned_set[source].pop(id)
        return cleaned_set

    def parseApiFiles(self, debug=False):
        """
        method to extract data from apis and parse each created file for metadata
        :return: dictionary of data indexed by filename
        """
        parsing_errors = {}
        result_set = {}
        try:
            new_files = self.getNewFiles()
            file_set = self.unzipApiFiles(new_files)
            for source in file_set:
                result_set[source] = {}
                for file in file_set[source]:
                    ignore_list = self.apiManager.getSourceIgnoreList(source)
                    parser = OnlineMetaParser.OnlineMetaParser(
                        ignored=ignore_list, source=source)
                    data = self.parseXMLFile(file, parser=parser)
                    # path_to_file = os.path.join(self.folder, file)
                    # if os.path.exists(path_to_file):
                    #     os.remove(path_to_file)
                    if type(data) != tuple:
                        result_set[source][file] = data
                        file_id = file.split("/")[-1].split(".")[0]
                        result_set[source][file].update(new_files[source][file_id])
                    else:
                        parsing_errors[data[1]] = data[0]
        except requests.exceptions.ConnectionError as e:
            parsing_errors[
                "Connection"] = "error connecting to the internet. Sources not refreshed."
        self.log_errors(parsing_errors)
        return result_set

    def log_errors(self, errors):
        if len(errors) > 0:
            if self.parent is not None:
                    self.parent.updateStatusBar("Errors updating database. Contact developer if problem persists")
            for error in errors:
                logger.error("Error {} : {}".format(error, errors[error]))

    def addApiFiles(self, data):
        for source in data:
            for file in data[source]:
                self.addPiece(file, data[source][file])

    def cleanupApiFiles(self, data, extensions=['mxl', 'xml']):
        for source in data:
            for file in data[source]:
                for ext in extensions:
                    file_ext = file.split(".")[0] + "." + ext
                    if os.path.exists(os.path.join(self.folder, file_ext)):
                        os.remove(os.path.join(self.folder, file_ext))

    def downloadFile(self, filename):
        file_info = filename.split(".")
        fname = file_info[0]
        source = self._data.getPieceSource(filename)
        if source is not None:
            source = source['source']
        secret = self._data.getSecret(filename)
        if secret is not None:
            secret = secret['secret']
        try:
            status_code = self.apiManager.downloadFile(
                source=source, file=fname, secret=secret, extension='pdf')
            if status_code == 200:
                self._data.downloadPiece(filename)
                return True
        except requests.exceptions.ConnectionError as e:
            logger.exception("Error downloading file - {} exception {}".format(filename, str(e)))
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
        self.cleanupApiFiles(result_set)

    def addPiece(self, filename, data):
        self._data.addPiece(filename, data)

    def getPieceInfo(self, filenames):
        return self._data.getAllPieceInfo(filenames)

    def getFileList(self, online=False):
        return self._data.getFileList(online=online)

    def setupFolderBrowser(self):
        db_files = self._data.getFileList()
        self.folder_browser = FolderBrowser(
            db_files=db_files,
            folder=self.folder)

    def handleZips(self):
        zip_files = self.folder_browser.getZipFiles()
        if zip_files is not None:
            unzipper = Unzipper(folder=self.folder, files=zip_files)
            unzipper.unzip()



    def refresh(self):
        if self.wifi:
            self.runApiOperation()
        self.refreshWithoutDownload()

    def refreshWithoutDownload(self):
        db_files = self._data.getFileList()
        self.folder_browser.resetDbFileList(db_files)
        self.handleZips()
        self.handleXMLFiles()

    def getPieceSummary(self, file_list, sort_method="title", online=False):
        info = self._data.getAllPieceInfo(file_list, online=online)
        ids = ["title","composer","lyricist","filename"]
        summary_strings = []
        for elem in info:
            entry = " ".join(["{}: {}".format(key, elem[key]) for key in ids if key in elem and elem[key] != ''])
            summary_strings.append((entry, elem['filename']))
        return summary_strings

    def getLicense(self, filename):
        result = self._data.getLicense(filename)
        # eventually we should open up a file and get the text based on the license name,
        # but for now we need to do this
        if result is not None:
            result = result['license']
            folder = '/users/charlottegodley/PycharmProjects/FYP/implementation/primaries' \
                     '/ImportOnlineDBs/licenses'
            file = os.path.join(folder, result)
            if os.path.exists(file):
                fob = open(file, 'r')
                lines = fob.readlines()
                result = "\n".join(lines)

        return result

    def getPieceSummaryStrings(self, sort_method="title"):
        file_list = self._data.getFileList()
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
        self._data.archivePieces(file_list)

    def parseXMLFile(self, filename, parser=None):
        errorTuple = []
        if parser is None:
            parser = MetaParser.MetaParser()
        try:
            data_set = parser.parse(os.path.join(self.folder, filename))
            return data_set
        except Exception as e:
            errorTuple.append(str(e))
            errorTuple.append(filename)
            logger.exception("Exception parsing {} - {}".format(filename, str(e)))
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
            self._data.addPiece(file, data_set)

    def handleXMLFiles(self):
        """
        method to get all the new and old files from the folder browser and call parseNew and parseOld methods
        :return:
        """
        files = self.folder_browser.getNewAndOldFiles(self.folder_browser.getFolderFiles())
        if "new" in files:
            self.parseNewFiles(sorted(files["new"]))
        if "old" in files:
            self.parseOldFiles(sorted(files["old"]))



    def copyFiles(self, filenames):
        """
        method to copy a list of files from one folder to another
        :param filenames: list of files including extension and folder
        :return: none
        """
        for file in filenames:
            folder_file_split = os.path.split(file)
            f = folder_file_split[-1]
            shutil.copyfile(file, os.path.join(self.folder, f))




