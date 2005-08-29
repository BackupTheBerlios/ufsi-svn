"""
"""

import ufsi
import TarUtils

import tarfile



class TarFile(ufsi.FileInterface):
    """
    """


    def __init__(self,path):
        """
        """
        self.__path=path
        self.__tarPathStr=path.getPathString()
        self.__fileHandle=None
        self.__tarFileObject=None


    def __str__(self):
        """
        """
        return str(self.__path)


    def open(self,mode='r'):
        """
        """
        if mode not in ['r']:
            raise ufsi.InvalidArgumentError('mode must be "r"')

        tarFile=self.__path.getTarFilePath()
        tf=tarFile.getFile()
        tf.open('r')
        self.__tarFileObject=tar=tarfile.TarFile('','r',tf)
        self.__fileHandle=tar.extractfile(self.__tarPathStr)

        return self.__fileHandle

    def read(self,size=-1):
        return self.__fileHandle.read(size)

    def readLine(self):
        return self.__fileHandle.readline()

    def readLines(self):
        return self.__fileHandle.readlines()

    def write(self,s):
        raise UnsupportedOperationError('Tar files can only be read.')

    def writeLines(self,lines):
        raise UnsupportedOperationError('Tar files can only be read.')

    def close(self):
        if self.__fileHandle is not None:
            self.__fileHandle.close()
            self.__fileHandle=None
            self.__tarFileObject.close()
            self.__tarFileObject=None


    def getStat(self):
        ti=TarUtils.getTarInfo(self.__path.getTarFilePath(),self.__tarPathStr)
        return TarUtils.tarInfoToDict(ti)

    def getPath(self):
        return self.__path
