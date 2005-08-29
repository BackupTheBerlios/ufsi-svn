"""
"""


import ufsi
import TarUtils

import tarfile


class TarDir(ufsi.DirInterface):

    def __init__(self,path):
        self.__path=path
        self.__tarPathStr=path.getPathString()


    def __str__(self):
        return self.__tarPathStr


    def getDirList(self,pattern=None):
        """
        TODO: a dir must end in a '/' char
        """
        ms=TarUtils.getMembers(self.__path.getTarFilePath())
        ms=map(lambda ti:ti.name,ms)
        ms=filter(lambda s:s.startswith(self.__tarPathStr),ms)
        if not ms:
            raise ufsi.PathNotFoundError('Path "%s" not found'%self.__path)
        ms=map(lambda s:s[len(self.__tarPathStr):],ms)
        ms=filter(lambda s:'/' not in s,ms)
        ms=filter(str,ms)
        return ms


    def getStat(self):
        ti=TarUtils.getTarInfo(self.__path.getTarFilePath(),self.__tarPathStr)
        return TarUtils.tarInfoToDict(ti)


    def getPath(self):
        return self.__path

