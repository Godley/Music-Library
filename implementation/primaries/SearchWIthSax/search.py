import xml.sax
from os import listdir
from os.path import isfile, join

from implementation.primaries.SearchWIthSax import Extractor


class Finder(object):
    def __init__(self, find=[], folder='/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/Loading/reading/'):
        self.tags = find
        self.tracked = {}
        self.folder = folder
        self.files = [ f for f in listdir(self.folder) if isfile(join(self.folder,f)) and (f.endswith('xml') or f.endswith('mxl'))]

    def parse(self):

        for f in self.files:
            path = join(self.folder, f)
            fob = open(path, 'r')
            self.handler = Extractor.Extractor(self, f)
            xml.sax.parse(fob, self.handler)

    def search(self, item):
        found = {}
        for key in self.tracked.keys():
            if item.lower() in key.lower():
                found[key] = self.tracked[key]
        return found

    def searchAndPrint(self, inp):
        results = self.search(inp)
        if len(results) > 0:
            print "results found matching " + inp + " : \n"
        for key, value in results.iteritems():
            print "value: " + key
            print "file: " + value[0]
            print "tag: " + value[1]
            print "attributes: ", value[2]
        return results





