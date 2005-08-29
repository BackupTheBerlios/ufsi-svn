"""
Defines all of the standard UFSI errors.

TODO: standardise all error messages
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



class AuthorisationError(Error):
    """
    A base class for exceptions caused by insufficient access.
    """
    pass
    

class AccessDeniedError(Error):
    """
    The current authentication level is not sufficient to access this
    resource.
    """
    pass



class InvalidArgumentError(Error):
    """
    Raised whenever an operation is provided with an invalid argument.
    """
    pass

class InvalidPathError(InvalidArgumentError):
    """
    Raised whenever a path is provided that isn't of the correct
    format for a path of that type. Different to PathNotFoundError.
    """
    pass



class FSError(Error):
    pass


class PathNotFoundError(FSError):
    pass

class NotASymlinkError(FSError):
    """
    Raised when a symlink based operation is performed on a
    non-symlink file system item.
    """
    pass



class IOError(Error):
    pass


class EOFError(IOError):
    pass

class TimeoutError(IOError):
    pass
