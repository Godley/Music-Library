class LilypondNotInstalledException(BaseException):

    '''ERROR! LILYPOND NOT FOUND'''


class APIKeyNotFoundException(BaseException):
    """ ERROR: Missing an API key.
    """


class BadAPIRequest(BaseException):
    """ ERROR: API did not give 200 response.
    """
