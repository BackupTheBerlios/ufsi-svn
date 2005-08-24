"""
The ufsi module and its various classes.
"""

# import required standard modules
import re


# import UFSI interfaces
from PathInterface import PathInterface
from FileInterface import FileInterface
from DirInterface import DirInterface


# import UFSI errors
from Errors \
import Error, \
       InvalidPathError, \
       UnsupportedOperationError, \
       AuthorisationError, \
       AuthorisationRequiredError, \
       AuthorisationInvalidError, \
       IOError, \
       PathNotFoundError, \
       EOFError, \
       TimeoutError


# import UFSI implementations
from NativePath import NativePath
from NativeFile import NativeFile
from NativeDir import NativeDir

from HttpPath import HttpPath
from HttpFile import HttpFile

from FtpFile import FtpFile


def Path(path):
    """
    Determines what type of path we have and creates the appropriate
    Path object.
    """
    
    lcPath=path.lower()
    protocolRePat='(?P<protocol>[^:/]+)://'
    protocolRe=re.compile(protocolRePat)

    protocolMo=protocolRe.match(lcPath)

    if protocolMo is None:
        return NativePath(path)        

    protocol=protocolMo.group('protocol')
    
    if protocol=='http':
        return HttpPath(path)
       
    else:
        return None


