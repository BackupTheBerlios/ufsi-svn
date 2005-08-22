"""
An ``ufsi.DirInterface`` implementation for native file systems.

"""

import ufsi

import os


class NativeDir(ufsi.DirInterface):
    """
    The NativeDir class implements the ``ufsi.DirInterface`` for
    natively supported file systems. It is currently os generic.
    """

    
    def __init__(self,path):
        """
        Create a NativeDir object for the NativePath in ``path``.
        """
        self.__path=path
        self.__pathStr=str(path)


    def __str__(self):
        """
        Returns the path to this dir.
        """
        return self.__pathStr


    def getDirList(self,filter=None):
        """
        Returns a list of strings? or Path's that exist in this
        directory. 
        """
        # TODO: implement re filtering
        return map(ufsi.Path,os.listdir(self.__pathStr))


    def getStat(self):
        """
        Returns a dict of information about this directory.
        """
        # TODO: return a dict
        return os.stat(self.__pathStr)


    def getPath(self):
        """
        Returns the path to this dir as a Path object.
        """
        return self.__path

