"""
An ``ufsi.DirInterface`` implementation for native file systems.

"""

import ufsi

import os


class NativeDir(ufsi.DirInterface):
    """
    """

    
    def __init__(self,path):
        """
        """
        self.__path=path
        self.__pathStr=str(path)


    def __str__(self):
        """
        """
        return self.__pathStr


    def getDirList(self,filter=None):
        """
        """
        # TODO: implement re filtering
        return map(ufsi.Path,os.listdir(self.__pathStr))


    def getStat(self):
        """
        """
        # TODO: return a dict
        return os.stat(self.__pathStr)


    def getPath(self):
        """
        """
        return self.__path

