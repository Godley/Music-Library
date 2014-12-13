from search import Finder

class Playlister(object):
    def __init__(self, folder='/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/SampleMusicXML/'):
        self.folder = folder
        self.finder = Finder(find=['part-name','movement-title'], folder=self.folder, byTag=True)
        self.finder.parse()

    def GetPlaylist(self):
        inp = raw_input("enter thing to match:")
        results = self.finder.Match(inp)
        for key,playlist in results.iteritems():
            print "common " + inp + " :" +key
            for item in playlist:
                print item
            print "\n"

p = Playlister()
p.GetPlaylist()