"""
An FTP implementation of ``ufsi.PathInterface``.

"""

import ufsi
import UrlPathUtils

import ftplib


class FtpPath(ufsi.AbstractUrlPath):
    """
    An FTP implementation of ``ufsi.PathInterface``. Based on the
    AbstractUrlPath class.

    TODO: Look at creating an FTP Adapter class, as well as a
    streamToRandomAccessFile Adapter.
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
        Splits the path into:

        * protocol - will always be 'ftp'
        * user - None unless a user name is part of the path
        * password - None unless a password is part of the path
        * host - always present
        * port - None unless a port number is part of the path
        * urlPath - anything after the '/' after the host and optional
          port number.
        * dirs - a list of dir names. Possibly an empty list.
        * fileBase
        * fileExt

        Caches the result, so that subsequent calls are efficient.

        Raises:
        
        * InvalidPathError if the path doesn't match the expected
          format of an FTP path. See RFC1738 and AbstractUrlPath.
        
        """
        # check for a cached version
        if self.__split is not None:
            # TODO: perform a deep copy for dirs and other lists..
            return self.__split.copy()

        # else split it and cache it
        d=self.__super.split(self)
        # TODO: later also split ;type?param#andFragments
        d.update(UrlPathUtils.splitHeirarchicalUrlPath(d['urlPath']))
        self.__split=d
        return d

    def join(self,other):
        """
        Joins a relative path onto the end of this path, inserting or
        removing separator characters as required. If ``other`` is an
        absolute path it is returned instead, otherwise a new Path
        object is created using the joined path and returned.
        """
        return self.__super.join(self,other)


    def getSeparator(self):
        """
        Returns '/' which is the standard heirarchical url separator
        character.
        """
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
        """
        Returns an FTP File object.
        """
        return ufsi.FtpFile(self)

    def getDir(self):
        """
        Returns an FTP Dir object.
        """
        return ufsi.FtpDir(self)

    def getSymlinkPath(self):
        """
        Returns a Path object for the item that the symlink points to.
        to.
        """
        # TODO: but how?
        return None
