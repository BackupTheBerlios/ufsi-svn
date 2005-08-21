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



class AuthorisationError(Error):
    pass

class AuthorisationRequiredError(AuthorisationError):
    pass

class AuthorisationInvalidError(AuthorisationError):
    pass



class IOError(Error):
    pass

class PathNotFoundError(IOError):
    pass

class EOFError(IOError):
    pass

class TimeoutError(IOError):
    pass
