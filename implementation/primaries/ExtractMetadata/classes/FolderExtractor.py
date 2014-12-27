from implementation.primaries.ExtractMetadata.classes import FolderBrowser, Extractor
import os
from xml.sax import make_parser, handler
class FolderExtractor(object):
    def __init__(self, folder=None, byTag=False):
        self.folder = folder
        self.Browser = FolderBrowser.Browser(folder=self.folder)
        self.Browser.Load()
        self.tracked = {}
        self.tags = ['part-name','key','fifths','mode','clef','line','sign']

    def Load(self):
        for f in self.Browser.xmlFiles:
            file_to_open = os.path.join(self.folder, f)
            self.file = f
            path_extractor = Extractor.Extractor(self)
            parser = make_parser()
            parser.setFeature(handler.feature_external_ges, False)
            parser.setContentHandler(path_extractor)
            fob = open(file_to_open, 'r')
            parser.parse(fob)

