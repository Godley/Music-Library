import os, shutil, zipfile, logging
from xml.sax._exceptions import *

import requests.exceptions


from implementation.primaries.ExtractMetadata.classes import MusicData, MetaParser, OnlineMetaParser
from implementation.primaries.ImportOnlineDBs.classes import ApiManager
from implementation.primaries.ExtractMetadata.classes.DataLayer.helpers import filter_dict, get_if_exists
from implementation.primaries.ExtractMetadata.classes.helpers import get_set_of_dict_values
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

            composer_result = self._data.get_pieces_by_creator(
                value, online=online)
            combined["Composer"] = composer_result

            lyricist_result = self._data.get_pieces_by_creator(
                value, online=online, creator_type='lyricist')
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
            results, all_matched = self.create_results(["Instruments"], [instrument_data])
        return results, all_matched

    def handleTempoQueries(self, search_data, online=False):
        tempo_data = self._data.getPieceByTempo(
                search_data["tempo"], online=online)
        return self.create_results(["Tempo"], tempo_data)

    def handleTimeQueries(self, search_data, online=False):
        time_data = self._data.getPieceByMeter(
            search_data["time"], online=online)
        return self.create_results(["Meter/Time signature"], [time_data])

    def handle_clef_or_key_queries(self, search_data, online=False, query='key'):
        keys = []
        data = []
        if "other" in search_data[query]:
            keydata = self._data.get_piece_by_join(search_data[query]["other"], query)

            search_data[query].pop("other")
            data.append(keydata)
            keys.append("{}s".format(query.capitalize()))

        if len(search_data[query]) > 0:
            instrument_data = []
            if query == 'clef':
                instrument_data = self._data.getPieceByInstrumentInClefs(
                search_data[query], online=online)
            elif query == 'key':
                instrument_data = self._data.getPieceByInstrumentInKeys(
                search_data[query], online=online)
            data.append(instrument_data)
            keys.append("Instruments in {}s".format(query.capitalize()))
        return self.create_results(keys, data)

    def handleTranspositionQueries(self, search_data, online=False):
        results = self.fetch_results(search_data["transposition"], "Instrument or transposition",
                                           self._data.getPieceByInstrumentsOrSimilar, online=online)
        return self.create_results(results.keys(), results.items())

    def create_results(self, keys, values, method=lambda n: len(n) > 0):
        results = {}
        all_matched = True
        for key, value in zip(keys, values):
            if method(value):
                results[key] = value
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

    def fetch_results(self, data, key, method, *args, **kwargs):
        results = {}
        for elem in data:
            files = method(elem, *args, **kwargs)
            if len(files) > 0:
                results["{}: {}".format(key, elem)] = files
        return results

    def fetch_and_form_results(self, data, key, method, *args, **kwargs):
        files = self.fetch_results(data, key, method, *args, **kwargs)
        return self.create_results(files.keys(), files.values())

    def handle_bibliography_queries(self, data, query='creator', online=False):
        method = self._data.get_pieces_by_creator
        if query == 'title':
            method = self._data.getPieceByTitle
        return self.fetch_and_form_results(data[query], query.capitalize(),
                                           method, creator_type=query, online=False)

    def getPieceSummary(self, file_list, sort_method="title", online=False):
        info = self._data.getAllPieceInfo(file_list, online=online)
        ids = ["title","composer","lyricist","filename"]
        summary_strings = []
        for elem in info:
            entry = " ".join(["{}: {}".format(key, elem[key]) for key in ids if key in elem and elem[key] != ''])
            summary_strings.append((entry, elem['filename']))
        return summary_strings

    def runQueries(self, search_data, online=False):
        results = {}
        all_matched = True
        method_table = {"text": self.handleTextQueries, "instrument": self.handleInstrumentQueries,
                        "tempo": self.handleTempoQueries, "time": self.handleTimeQueries,
                        "transposition": self.handleTranspositionQueries,
                        "filename": self.handleFilenameQueries}

        simpler_method_table = {"title": self.handle_bibliography_queries,
                                "lyricist": self.handle_bibliography_queries,
                                "composer": self.handle_bibliography_queries,
                                "clef": self.handle_clef_or_key_queries,
                                "key": self.handle_clef_or_key_queries}

        for key in search_data:
            if key in simpler_method_table:
                key_result, all_matched = simpler_method_table[key](search_data, query=key, online=online)
            else:
                key_result, all_matched = method_table[key](search_data, online=online)
            results.update(key_result)

        summaries = {}
        if all_matched:
            intersection = set.intersection(
                *get_set_of_dict_values(results))
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
        elem_ids = ["clefs", "keys", "composers", "lyricists"]
        playlist_table = {"time signatures": self._data.getPiecesByAllTimeSigs,
                          "instruments": self._data.getPiecesByAllInstruments,
                          "tempos": self._data.getPiecesByAllTempos}
        if select_method == "all":
            clefs = self._data.get_piece_by_all_elem(elem='clefs')
            keys = self._data.get_piece_by_all_elem(elem='keys')
            composers = self._data.get_piece_by_all_elem(elem='composers')
            lyricists = self._data.get_piece_by_all_elem(elem='lyricists')
            instruments = self._data.getPiecesByAllInstruments()
            timesigs = self._data.getPiecesByAllTimeSigs()
            tempos = self._data.getPiecesByAllTempos()
            result_set["clefs"] = clefs
            result_set["keys"] = keys
            result_set["composers"] = composers
            result_set["lyricists"] = lyricists
            result_set["instruments"] = instruments
            result_set["time_signatures"] = timesigs
            result_set["tempos"] = tempos

        else:
            if select_method not in elem_ids:
                result_set[select_method] = playlist_table[select_method]()
            else:
                result_set[select_method] = self._data.get_piece_by_all_elem(elem=select_method)

        return filter_dict(result_set)

class MusicManager(QueryLayer):
    """
    Grand master class which pulls together features from every other class. This class is instantiated by the Application
    class and should provide methods for the application to access everything else, from rendering to info extraction
    to API access.
    """

    def __init__(self, parent, folder='/Users/charlottegodley/PycharmProjects/FYP'):
        super(MusicManager, self).__init__(folder)
        self.parent = parent
        """the application instance in which this manager resides"""
        self.wifi = True

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
        source = self._data.get_value_for_filename(filename, 'source')
        if source is not None:
            source = source['source']
        secret = self._data.get_value_for_filename(filename, 'secret')
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



    def getLicense(self, filename):
        result = self._data.get_value_for_filename(filename, 'license')
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




