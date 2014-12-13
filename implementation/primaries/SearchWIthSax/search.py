import xml.sax
from os import listdir
from os.path import isfile, join
import pickle
from implementation.primaries.SearchWIthSax import Extractor
import zipfile, os
import pprint


class Finder(object):
    def __init__(self, find=[], folder='/Users/charlottegodley/PycharmProjects/FYP/implementation/primaries/Loading/reading/', byTag=False):
        self.tags = find
        self.byTag = byTag
        self.tracked = {}
        self.folder = folder
        self.extract_list = []
        self.track_temp = {}
        self.Unzip()
        if byTag:
            if not os.path.exists(os.path.join(self.folder, '.parsedtags')):
                f=open(os.path.join(self.folder, '.parsedtags'), 'w+')
                f.close()
            self.meta = file(os.path.join(self.folder, '.parsedtags'), 'r+')
        else:
            if not os.path.exists(os.path.join(self.folder, '.parseddata')):
                f=open(os.path.join(self.folder, '.parseddata'), 'w+')
                f.close()
            self.meta = file(os.path.join(self.folder, '.parseddata'), 'r+')
        if hasattr(self, "meta"):
            self.load_data = pickle.Unpickler(self.meta)
            try:
                self.track_temp = self.load_data.load()
            except:
                self.track_temp = {}
        self.ignore_list = []
        for key, val in self.track_temp.iteritems():
            self.ignore_list.extend([f[0] for f in val])
        self.files = [ f for f in listdir(self.folder) if isfile(join(self.folder,f)) and (f.endswith('xml')) and f not in self.ignore_list]

    def Unzip(self):
        self.extracted = file(os.path.join(self.folder, '.extracted'), 'r+b')
        if os.path.exists(os.path.join(self.folder, '.extracted')):
            self.extract_list = pickle.Unpickler(self.extracted)
            try:
                self.extract_list = self.extract_list.load()
            except:
                self.extract_list = []
        self.mxl = [ f for f in listdir(self.folder) if isfile(join(self.folder,f)) and f.endswith('mxl') and f not in self.extract_list]
        for f in self.mxl:
            if f not in self.extract_list:
                zip = zipfile.ZipFile(os.path.join(self.folder,f), 'r')
                names = [fi for fi in zip.namelist() if fi.endswith('xml')]
                name = f.split('.')[0]
                zip.extract(names[1], path=self.folder)
                os.rename(os.path.join(self.folder,names[1]), os.path.join(self.folder,name+'.xml'))
                self.extract_list.append(f)
        pickle.dump(self.extract_list, self.extracted)

    def parse(self):

        for f in self.files:
            path = join(self.folder, f)
            fob = open(path, 'r')
            self.handler = Extractor.Extractor(self, f, byTag=self.byTag)
            xml.sax.parse(fob, self.handler)
        self.tracked.update(self.track_temp)
        pickle.dump(self.tracked,self.meta)

    def search(self, item):
        found = {}
        for key in self.tracked.keys():
            if item.lower() in key.lower():
                found[key] = self.tracked[key]
        return found

    def Match(self, tag):
        dataset = self.tracked[tag]
        playlists = {}
        previous = ""
        for i in range(len(dataset)):
            value = dataset[i][1]
            if value != " ":
                if tag == "part-name":
                    value = value.split(' ')[0]
                    plur = list(value)
                    valid = True
                    for p in plur:
                        if p != " ":
                            print value
                            break
                        else:
                            valid = False
                    if valid == False:
                        print "helo"
                        continue
                    if len(plur) > 0:
                        if plur[-1] == 's':
                            value = "".join(plur[0:len(plur)-1])
                if value != previous:
                    results = [dataset[j][0] for j in range(i+1,len(dataset)) if value in dataset[j][1] and dataset[j][0] != dataset[i][0]]
                    if len(results) > 0:
                        results.append(dataset[i][0])
                        playlists[value] = results
            previous = value
        return playlists

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





