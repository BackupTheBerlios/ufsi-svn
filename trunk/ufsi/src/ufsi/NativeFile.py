"""
NativeFile is an implementation of the ``ufsi.FileInterface`` for
paths natively handled by the built-in functions and the os module.

"""

import ufsi

import os

class NativeFile(ufsi.FileInterface):
    """
    """


    def __init__(self,path):
        """
        """
        self.__path=path
        self.__pathStr=str(path)
        self.__fileHandle=None


    def __str__(self):
        """
        self.close()
        self.open('r')
        s=''.join(self.readLines())
        self.close()
        return s
        """

        return self.__pathStr


    def open(self,mode=None):
        """
        """
        self.close()

        if mode is None:
            self.__fileHandle=file(self.__pathStr)
        else:
            self.__fileHandle=file(self.__pathStr,mode)

    def read(self,size=None):
        """
        """
        # TODO: insert check for file being open
        if size is None:
            return self.__fileHandle.read()
        else:
            return self.__fileHandle.read(size)

    def readLine(self):
        """
        """
        return self.__fileHandle.readline()

    def readLines(self):
        """
        """
        return self.__fileHandle.readlines()

    def write(self,s):
        """
        """
        self.__fileHandle.write(s)

    def writeLines(self,lines):
        """
        """
        self.__fileHandle.writelines(lines)

    def close(self):
        """
        """
        if self.__fileHandle!=None:
            self.__fileHandle.close()
            self.__fileHandle==None


    def getStat(self):
        """
        """
        # TODO: fix this to return a dict
        return os.stat(self.__pathStr)


    def getPath(self):
        """
        """
        return self.__path



