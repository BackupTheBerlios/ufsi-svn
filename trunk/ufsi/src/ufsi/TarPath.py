import ufsi
import TarUtils

import tarfile


class TarPath(ufsi.PathInterface):
    def __init__(self,tarFilePath,tarPath):
        # TODO: currently tarFilePath must be a NativePath - seek method
        self.__tarFilePath=tarFilePath
        # TODO: raise Invalid Arg or something
        assert self.__tarFilePath.isFile()
        # TODO: change '\\' into '/'
        self.__tarPath=tarPath


    def __str__(self):
        return self.__tarPath


    def getTarFilePath(self):
        return self.__tarFilePath

    def getPathString(self):
        return self.__tarPath


    def join(self,other):
        if not isinstance(other,ufsi.PathInterface):
            other=ufsi.Path(other)

        if other.isAbsolute():
            return other

        otherStr=str(other)
        otherSep=other.getSeparator()
        pathSep=self.getSeparator()
        pathStr=self.__tarPath

        otherStr=otherStr.replace(otherSep,pathSep)
        if otherStr.startswith(pathSep):
            otherStr=otherStr[len(pathStr):]

        if not pathStr.endswith(pathSep):
            pathStr+=pathSep

        return TarPath(self.__tarFilePath,pathStr+otherStr)

    def split(self):
        """
        """
        # TODO: this should be put into a PathUtils module where a
        # basic <sep><dir><sep><dir><sep><fileBase>.<FileExt> path
        # is generically split by giving it a separator character

        dirs=self.__tarPath.split(self.getSeparator())
        fileName=dirs.pop()
        if '.' in fileName:
            (fileBase,fileExt)=fileName.rsplit('.',1)
        else:
            fileBase=fileName
            fileExt=None

        d={}
        d['dirs']=dirs
        d['fileName']=fileName
        d['fileBase']=fileBase
        d['fileExt']=fileExt
        return d


    def isAbsolute(self):
        return True

    def getSeparator(self):
        return '/'
    

    def getAuthentication(self):
        return self.__auth

    def setAuthentication(self,auth):
        self.__auth=auth


    def isFile(self):
        """
        The tar file impl. doesn't follow sym links to check file types
        """
        try:
            ti=TarUtils.getTarInfo(self.__tarFilePath,self.__tarPath)
            while ti.issym():
                ti=TarUtils.getTarInfo(self.__tarFilePath,ti.linkname)
            return ti.isfile()
        except ufsi.PathNotFoundError,e:
            return False

    def isDir(self):
        """
        Dirs must end in a slash char
        The tar file impl. doesn't follow sym links to check file
        types
        TODO: A symlink to a dir doesn't have a trailing slash.
        """
        try:
            dirPath=self.__tarPath
            if not dirPath.endswith(self.getSeparator()):
                dirPath+=self.getSeparator()
            ti=TarUtils.getTarInfo(self.__tarFilePath,dirPath)
            while ti.issym():
                ti=TarUtils.getTarInfo(self.__tarFilePath,ti.linkname)
            return ti.isdir()
        except ufsi.PathNotFoundError,e:
            return False

    def isSymlink(self):
        """
        """
        try:
            return TarUtils.getTarInfo(self.__tarFilePath,
                                       self.__tarPath).issym()
        except ufsi.PathNotFoundError,e:
            return False


    def getFile(self):
        """
        """
        return ufsi.TarFile(self)

    def getDir(self):
        """
        """
        return ufsi.TarDir(self)

    def getSymlinkPath(self):
        """
        """
        if not self.isSymlink():
            raise ufsi.NotASymlinkError('%r is not a symlink'%self.__tarPath)

        return ufsi.Path(TarUtils.getTarInfo(self.__tarFilePath,
                                             self.__tarPath).linkname)
