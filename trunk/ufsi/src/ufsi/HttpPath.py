"""
A HTTP implementation of ``ufsi.PathInterface``.

"""

import ufsi
import UrlPathUtils
import HttpUtils

import urllib2


class HttpPath(ufsi.AbstractUrlPath):
    """
    HttpPath is an implementation of ``ufsi.PathInterface`` that
    interfaces with HTTP file systems. A HTTP path is a standard url
    and therefore uses several of the ``UrlPathUtils`` functions.
    
    """
    __super=ufsi.AbstractUrlPath


    def __init__(self,path):
        """
        Creates a Path object from a HTTP path.
        """
        self.__super.__init__(self,path)
        self.__split=None


    def split(self):
        """
        Splits the path into:

        * protocol - should always be 'http'
        * user - optional user. This will only be populated if the
          user is actually included in the path. That is, if an
          Authentication object has been set it will not be used to
          populate this field.
        * password - only present if a user was given and even then
          it's optional.
        * host - either an ip address or a host name. Must be present
          for a valid HTTP url.
        * port - optional port number.
        * urlPath - everything after the '/' after the host and
          optional port or None.
        * dirs - a list of directory names which will always be
          present.
        * fileBase - the part of the fileName before the last
          period. If no '/' is present after the host (or port), the
          fileBase value will be None, otherwise it will be a
          (possibly empty) string.
        * fileExt - the part of the fileName after the last period. If
          fileBase is None it will also be None and if no period
          exists in the fileName it will be None.

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
        Joins a relative path on to the end of this path, correcting
        separator characters if necessary. If ``other`` is an absolute
        path ``other`` is returned, otherwise a new Path object is
        created using the joined path and returned.
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
        Returns True since all HTTP paths are absolute.
        """
        return True


    def isFile(self):
        """
        Returns True if the path exists. All HTTP paths refer to a
        file so if the path exists, it's a file.
        """
        try:
            f=self.getFile()
            f.open()
            f.close()
            return True
        except ufsi.PathNotFoundError,e:
            return False
        except Exception,e:
            # Some other error - handle it
            HttpUtils.handleException(e,self._path)

    def isDir(self):
        """
        All HTTP paths refer to a file so it can't be a directory.
        """
        return False

    def isSymlink(self):
        """
        Returns True if the path is a symbolic link to another
        path. This means if a HTTP request results in a 301 or 302
        code it is a symlink.
        """
        # TODO: look at 302 and 301 codes for symlinks...
        return False


    def getFile(self):
        return ufsi.HttpFile(self)

    def getDir(self):
        raise UnsupportedOperationError

    def getSymlinkPath(self):
        """
        Returns a Path object for the path that the symlink points
        to. It will always be ``join``ed with this Path.
        """
        # TODO: as in isSymlink
        raise NotImplementedError


