from implementation.primaries.SearchWIthSax.search import Finder
from implementation.primaries.Loading.MxmlParser import MxmlParser
import os

class SearchLoad(object):
    def __init__(self, folder='/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/Loading/reading/'):
        self.folder = folder
        self.finder = Finder(find=['part-name','creator','movement-title'],folder=self.folder)
        self.finder.parse()
        self.parser = MxmlParser()

    def Load(self, file):
        fob = open(file, 'r')
        piece = self.parser.parse(fob)
        print str(piece)

    def validFile(self, file):
        if os.path.exists(os.path.join(self.folder, file)):
            return True
        return False

    def GetInput(self):
        inp = raw_input('Enter search term ')
        self.results = self.finder.searchAndPrint(inp)
        file = raw_input('Enter desired file from list')
        if(self.validFile(file)):
            self.Load(os.path.join(self.folder, file))
        else:
            print "file entered incorrectly"

s = SearchLoad()
s.GetInput()