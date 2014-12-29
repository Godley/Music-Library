from implementation.primaries.ExtractMetadata.classes import FolderExtractor

class Playlister(object):
    def __init__(self, folder=None):
        self.folder = folder
        self.extractor = FolderExtractor.FolderExtractor(folder=self.folder, byTag=False)
        self.extractor.Load()


    def GetBasePlaylists(self):
        #method to get all lists of ordered files if they have more than one entry
        results = self.extractor.tracked
        playlists = {}
        for result in results.keys():
            if len(results[result].keys()) > 1:
                playlists[result] = list(results[result].keys())

        return playlists

    def ExtendPlaylistsByHalfMatches(self):
        # method that extends any existing lists by keys which were ignored the first round
        # because they don't have more than 1 in their list
        basics = self.GetBasePlaylists()
        keys = list(basics.keys())
        results = self.extractor.tracked
        r_keys = list(results.keys())
        next_level_playlists = basics
        excluded = [r for r in r_keys if r not in keys]
        for key in keys:
            for excl in excluded:
                if key in excl or excl in key:
                    for file in results[excl]:
                        if file not in next_level_playlists[key]:
                            next_level_playlists[key].append(file)

        return next_level_playlists

    def GetPartMatchesInExcluded(self):
        current_lists = self.ExtendPlaylistsByHalfMatches()
        curr_keys = list(current_lists.keys())
        full_list = self.extractor.tracked
        excluded = [key for key in full_list.keys() if key not in curr_keys]
        extra_playlists = {}
        index = ""
        copy = ""
        for key in range(len(excluded)):
            split_key = excluded[key].split(" ")
            matches = []
            for key_2 in range(key+1, len(excluded)):
                split_key_2 = excluded[key_2].split(" ")
                for k in split_key:
                    for k2 in split_key_2:
                        if k == k2:
                            for file in full_list[excluded[key_2]].keys():
                                if file not in matches:
                                    matches.append(file)
                            for file in full_list[excluded[key]].keys():
                                if file not in matches:
                                    matches.append(file)
                            index = k
                if index not in extra_playlists:
                    extra_playlists[index] = matches
                else:
                    for file in matches:
                        if file not in extra_playlists[index]:
                            extra_playlists[index].append(file)
        current_lists.update(extra_playlists)
        return current_lists

    def GetPartMatchesInExcludedAndCurrent(self):
        playlists = self.GetPartMatchesInExcluded()
        full_list = self.extractor.tracked
        keys_playlists = playlists.keys()
        keys_full = full_list.keys()
        excluded = [key for key in keys_full if key not in keys_playlists]
        for key in keys_playlists:
            for key_2 in excluded:
                split_2 = key_2.split(" ")
                for item in split_2:
                    if item in key and item != "major" and item != "minor":
                        for file in full_list[key_2].keys():
                            if file not in playlists[key]:
                                playlists[key].append(file)
        return playlists


