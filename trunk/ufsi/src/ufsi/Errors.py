"""
Defines all of the standard UFSI errors.
"""


class Error(Exception):
    def __init__(self,msg,causedBy=None):
        self.__msg=msg
        self.__causedBy=causedBy


    def __str__(self):
        s=self.__msg
        if self.__causedBy is not None:
            s+='\nCaused by:\n'+str(self.__causedBy)

        return s


    def getCausedBy(self):
        return self.__causedBy



class InvalidPathError(Error):
    pass



class UnsupportedOperationError(Error):
    pass



class AuthenticationError(Error):
    pass

class AuthenticationRequiredError(AuthenticationError):
    """
    Raised when the file system requires some form of authorisation
    but none was provided.
    """
    pass

class AuthenticationInvalidError(AuthenticationError):
    """
    Raised when the authentication provided was rejected by the file
    system.
    """
    pass

class UnsupportedAuthenticationError(AuthenticationError):
    """
    Raised when a form of authentication was provided that the specific
    file system doesn't support.
    """
    pass



class IOError(Error):
    pass

class PathNotFoundError(IOError):
    pass

class EOFError(IOError):
    pass

class TimeoutError(IOError):
    pass
