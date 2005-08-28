"""
Common native ufsi implementation utility functions.

"""

import ufsi

import os
import stat
import errno


def _raisePathNotFoundError(e,path):
    raise ufsi.PathNotFoundError('Path "%s" not found.'%path,e)


def handleException(e,path):
    """
    Handles any exceptions that are generated by the native ufsi
    implementations.
    """
    if isinstance(e,EnvironmentError):
        if os.name=='nt' and isinstance(e,WindowsError):
            if e.errno in [2,3]:
                _raisePathNotFoundError(e,path)
            
        if isinstance(e,OSError) or isinstance(e,IOError):
            if e.errno==errno.ENOENT:
                _raisePathNotFoundError(e,path)
            if e.errno==errno.EINVAL:
                raise ufsi.InvalidArgumentError('Invalid argument.',e)


    raise e
    

def convertStatObjectToDict(s):
    """
    Converts the stat tuple returned from os.stat into a dict. The
    following keys are set:

    * size - size of the file or dir
    * accessTime
    * modificationTime
    * creationTime
    * userId - id of the user that owns the file or dir
    * groupId - id of the group that owns the file or dir
    * mode - the permissions of the file or dir
    * inodeNumber
    * inodeDevice
    * inodeLinks - the number of links to the inode
    
    """
    d={}
    d['size']=s[stat.ST_SIZE]
    d['accessTime']=s[stat.ST_ATIME]
    d['modificationTime']=s[stat.ST_MTIME]
    d['creationTime']=s[stat.ST_CTIME]
    d['userId']=s[stat.ST_UID]
    d['groupId']=s[stat.ST_GID]
    d['mode']=s[stat.ST_MODE]
    d['inodeNumber']=s[stat.ST_INO]
    d['inodeDevice']=s[stat.ST_DEV]
    d['inodeLinks']=s[stat.ST_NLINK]
    return d
