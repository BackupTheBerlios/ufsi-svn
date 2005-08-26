"""
An FTP implementation of ``ufsi.PathInterface``.

"""

import ufsi

import ftplib


class FtpPath(ufsi.AbstractUrlPath):
    """
    """

    __super=ufsi.AbstractUrlPath


    def __init__(self,path):
        """
        Creates a Path object from an FTP path.
        """
        self.__super.__init__(self,path)
        self.__split=None


    def split(self):
        """
        """
        # check for a cached version
        if self.__split is not None:
            return self.__split.copy()

        # else split it and cache it
        d=self.__super.split(self)
        # TODO: later also split ;type?param#andFragments
        d.update(UrlPathUtils.splitHeirarchicalUrlPath(d['urlPath']))
        self.__split=d
        return d

    def join(self,other):
        """
        """
        return self.__super.join(self,other)


    def getSeparator(self):
        return '/'

    def isAbsolute(self):
        """
        Returns True since FTP paths are always absolute.
        """
        return True


    def isFile(self):
        pass

    def isDir(self):
        pass

    def isSymlink(self):
        # TODO: but how? Look for a l in the dir list
        pass


    def getFile(self):
        return ufsi.FtpFile(self)

    def getDir(self):
        return ufsi.FtpDir(self)

    def getSymlinkPath(self):
        # TODO: but how?
        return None
