'''
A basic class which defines what methods sub classes must implement using exceptions.
If methods are not implemented and should be, the dev will know because it tips over. For a worked example,
see the MuseScore api class.
'''
from implementation.primaries import exceptions
from implementation.primaries.GUI import helpers

import sys, os


class Api(object):
    env_key = None
    api_key = ''

    def __init__(self, folder=""):
        self.folder = folder

    def downloadFile(self, fname, secret, type='mxl'):
        '''
        this method should download a given file from the API
        :param fname: an ID or filename the api can use to download the file
        example:
            data["id"] = element["id"]
            data["secret"] = element["secret"]
            data["title"] = element["metadata"]["title"]
            data["composer"] = element["metadata"]["composer"]
            data["lyricist"] = element["metadata"]["poet"]
            data["parts"] = element["metadata"]["parts"]
        :param type: file extension to download
        :return: status code of request
        '''
        raise NotImplementedError

    @staticmethod
    def getKey():
        '''
        method to fetch the API key from the store. SHOULD NOT be just hard coded
        :return: string of api key
        '''
        if not getattr(sys, "frozen", False):
            # If this is running in the context of a frozen (executable) file,
            # we return the path of the main application executable
            if Api.env_key in os.environ:
                return os.environ[Api.env_key]
            else:
                raise exceptions.APIKeyNotFoundException('Error, MSCORE environment variable not set. Please set to your API key for musescore')
        else:
            from implementation.primaries.ImportOnlineDBs.classes import config
            # If we are running in script or debug mode, we need
            # to find the obfuscated file where it's located
            return config.k[Api.env_key]



    def getCollection(self):
        '''
        this method should get all the files on the API
        :return: list of json results
        '''
        raise NotImplementedError

    def cleanCollection(self):
        '''
        this method should get all the files on the api using getCollection, then clean them to what we need
        for the application
        :return: list of cleaned json results
        '''
        raise NotImplementedError

    def search(self, filters):
        '''
        this method should search the api using each filter in turn (i.e if filter = {'text':['hello','world']} it
        should do 'hello' and 'world' in separate requests, unless the api has a specific way to do this), then
        put the results into a dict indexed by the value used to filter the results
        :param filters: dictionary of filters. Each key should be matched with a list value
        :return: dictionary of responses
        '''
        raise NotImplementedError

    def searchForAnyMatch(self, filters):
        '''
        not sure if this method is necessary,given search should do the same job.
        :param filters:
        :return:
        '''
        pass

    def searchForExactMatch(self, filters):
        '''
        this method should be basically the same as search, except that at the end it should return a list of the
        results which exist in all responses. Optional depending on how API works.
        :param filters: see search
        :return: list of results which match the filters exactly.
        '''
        pass
