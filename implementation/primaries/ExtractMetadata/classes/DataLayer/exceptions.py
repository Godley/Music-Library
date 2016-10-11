class BadTableException(BaseException):
    """Invalid table name on data entry"""


class BadPieceException(BaseException):
    """Invalid piece on data entry"""


class InvalidQueryException(BaseException):
    """Invalid clef or key"""
