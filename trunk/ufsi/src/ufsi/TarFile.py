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
        if mode in ['r','rb']:
            tarFile=self.__path.getTarFilePath()
            tf=tarFile.getFile()
            tf.open('r')
            self.__tarFileObject=tar=tarfile.TarFile('','r',tf)
            try:
                self.__fileHandle=tar.extractfile(self.__tarPathStr)
            except KeyError,e:
                raise ufsi.PathNotFoundError('Path "%s" not found'
                                             %self.__tarPathStr,e)

        elif mode in ['w','wb','a','ab']:
            raise ufsi.UnsupportedOperationError("Write is not supported")
        else:
            raise ufsi.InvalidArgumentError('mode must be "r" or "rb"')

    def read(self,size=-1):
        # TODO: apparently tarfile won't take -1 as a size
        if size<0:
            s=self.__fileHandle.read()
        else:
            s=self.__fileHandle.read(size)
        return s

    def readLine(self):
        return self.__fileHandle.readline()

    def readLines(self):
        return self.__fileHandle.readlines()

    def write(self,s):
        raise ufsi.UnsupportedOperationError('Tar files can only be read.')

    def writeLines(self,lines):
        raise ufsi.UnsupportedOperationError('Tar files can only be read.')

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
