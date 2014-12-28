from implementation.primaries.ExtractMetadata.classes import FolderExtractor

class Finder(object):
    def __init__(self, folder=None):
        self.folder = folder
        self.extractor = FolderExtractor.FolderExtractor(folder=folder, byTag=False)

    def Run(self):
        self.extractor.LoadCache()
        self.extractor.Load()

    def IsValidInput(self, entry):
        if len(entry) > 0:
            return True
        return False

    def Match(self, entry):
        results = {}
        if not self.IsValidInput(entry):
            return None
        if len(self.extractor.tracked.keys()) == 0:
            self.Run()
        for value in self.extractor.tracked.keys():
            if entry in value or entry == value:
                results[value] = self.extractor.tracked[value]
        return results
