try:
    from implementation.primaries.ExtractMetadata.classes import MetaParser
except:
    from primaries.ExtractMetadata.classes import MetaParser
import xml.sax
from xml.sax import make_parser


class OnlineMetaParser(MetaParser.MetaParser):

    """
    class which applies same meta parsing rules to files which have been temporarily
    downloaded from an api.
    will ignore a select set of tags specified by the instantiator
    """

    def __init__(self, ignored=None, source=""):
        MetaParser.MetaParser.__init__(self)
        self.ignored = ignored
        [self.handlers.pop(i) for i in self.ignored]
        self.source = source

    def collatePartsIntoData(self):
        MetaParser.MetaParser.collatePartsIntoData(self)
        self.data["source"] = self.source

