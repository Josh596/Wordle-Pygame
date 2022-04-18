class Error(Exception):
    """Base class for other exceptions"""
    pass


class NotEnoughLetters(Error):
    """Raised when the word is not complete"""
    pass

class NotInWordList(Error):
    """Raised when the word is not in word list"""
    pass