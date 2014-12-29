from implementation.primaries.ExtractMetadata.classes import FolderBrowser, FolderExtractor, Unzipper, Playlister
import os

class FolderParser(object):
    def __init__(self, folder=None):
        self.folder = folder
        self.browser = FolderBrowser.Browser(folder=self.folder)
        self.unzipper = Unzipper.Unzipper(zip_folder=os.path.join(self.folder, "zipped"), dest=self.folder)
        self.extractor = FolderExtractor.FolderExtractor(folder=self.folder)
        self.ZipFiles = []
        self.MusicFiles = []

    def LoadFiles(self):
        self.browser.Load()
        self.ZipFiles = self.browser.mxlFiles
        self.MusicFiles = self.browser.xmlFiles

    def MoveZipFiles(self):
        self.browser.CopyZippedFiles()
        self.browser.removeCopiedFilesFromMainFolder()
        self.ZipFiles = self.browser.mxlFiles

    def UnzipFiles(self):
        if len(self.ZipFiles) > 0:
            self.unzipper.fileList = self.ZipFiles
        else:
            self.unzipper.Load()
        self.unzipper.Unzip()
        self.LoadFiles()

    def MetaParse(self):
        self.extractor.Load()
        self.MusicData = self.extractor.tracked
