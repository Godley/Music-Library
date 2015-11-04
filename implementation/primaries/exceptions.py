class LilypondNotInstalledException(BaseException):

    '''ERROR! LILYPOND NOT FOUND'''

class APIKeyNotFoundException(BaseException):
    """ ERROR: did not find API key environment variable. Please request one and set your environment variable
    """