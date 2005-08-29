"""
An ``ufsi.DirInterface`` implementation for native file systems.

"""

import ufsi
import NativeUtils

import os


class NativeDir(ufsi.DirInterface):
    """
    The NativeDir class implements the ``ufsi.DirInterface`` for
    natively supported file systems. It is currently os generic.

    TODO: internally use a path object with the '/' stripped, then
    fileName is the name of this dir. Or write a getDirName method to
    get the 'dir' part from '/dir/' or 'dir' from '/dir', and a
    parentDir method too.
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
        try:
            # TODO: implement re filtering
            return os.listdir(self.__pathStr)
        except Exception,e:
            NativeUtils.handleException(e,self.__pathStr)


    def getStat(self):
        """
        Returns a dict of information about this directory.
        """
        try:
            return NativeUtils.convertStatObjectToDict(
                    os.stat(self.__pathStr))
        except Exception,e:
            NativeUtils.handleException(e,self.__pathStr)


    def getPath(self):
        """
        Returns the path to this dir as a Path object.
        """
        return self.__path

