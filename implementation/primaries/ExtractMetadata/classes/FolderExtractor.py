from implementation.primaries.ExtractMetadata.classes import FolderBrowser, Extractor
import os, pickle
from xml.sax import make_parser, handler
class FolderExtractor(object):
    def __init__(self, folder=None, byTag=False, tags=['part-name','key','fifths','mode','clef','line','sign']):
        self.folder = folder
        self.byTag = byTag
        self.Browser = FolderBrowser.Browser(folder=self.folder)
        self.Browser.Load()
        self.tracked = {}
        self.tags = tags

    def Load(self):
        for f in self.Browser.xmlFiles:
            file_to_open = os.path.join(self.folder, f)
            self.file = f
            path_extractor = Extractor.Extractor(self, byTag=self.byTag)
            parser = make_parser()
            parser.setFeature(handler.feature_external_ges, False)
            parser.setContentHandler(path_extractor)
            fob = open(file_to_open, 'r')
            parser.parse(fob)

    def Save(self):
        if not self.byTag:
            file = os.path.join(self.folder, ".extractedchars")
        else:
            file = os.path.join(self.folder, ".extractedtags")
        fob = open(file, 'wb')
        pickler = pickle.Pickler(fob)
        pickler.dump(self.tracked)

    def Empty(self):
        self.tracked = {}

    def LoadCache(self):
        if not self.byTag:
            file = os.path.join(self.folder, ".extractedchars")
        else:
            file = os.path.join(self.folder, ".extractedtags")
        fob = open(file, 'rb')
        unpickler = pickle.Unpickler(fob)
        self.tracked.update(unpickler.load())




