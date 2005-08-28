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
       UnsupportedOperationError, \
       AuthenticationError, \
       AuthenticationRequiredError, \
       AuthenticationInvalidError, \
       UnsupportedAuthenticationError, \
       InvalidArgumentError, \
       InvalidPathError, \
       FSError, \
       PathNotFoundError, \
       NotASymlinkError, \
       IOError, \
       EOFError, \
       TimeoutError

# import UFSI abstractions
from AbstractNativePath import AbstractNativePath
from AbstractUrlPath import AbstractUrlPath

# import UFSI implementations
from NativePath import NativePath
from NativeUnixPath import NativeUnixPath
from NativeWindowsPath import NativeWindowsPath
from NativeFile import NativeFile
from NativeDir import NativeDir

from HttpPath import HttpPath
from HttpFile import HttpFile

from FtpPath import FtpPath
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
       
    if protocol=='ftp':
        return FtpPath(path)

    else:
        return None


