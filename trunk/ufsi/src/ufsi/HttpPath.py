"""
A HTTP implementation of ``ufsi.PathInterface``.

"""

import ufsi

import UrlPathUtils



class HttpPath(ufsi.PathInterface):
    """
    HttpPath is an implementation of ``ufsi.PathInterface`` that
    interfaces with HTTP file systems. A HTTP path is a standard url
    and therefore uses several of the ``UrlPathUtils`` functions.
    
    """
    
    def __init__(self,path):
        """
        Creates a Path object from a HTTP path.
        """
        self.__path=path
        self.__auth=None


    def __str__(self):
        """
        Returns the path as a string.
        """
        return self.__path


    def split(self):
        """
        Splits the path into:

        * protocol - should always be 'http'
        * user - optional user as part of the path. That is, if an
          Authentication object has been set it will not be used to
          populate this field.
        * password - only present if a user was given and even then
          it's optional.
        * host - either an ip address or a host name. Must be present
          for a valid HTTP url.
        * port - optional port number.
        * dirs - a list of directory names which will always be
          present.
        * fileBase - the part of the fileName before the last
          period. If no '/' is present after the host (or port), the
          fileBase value will be None, otherwise it will be a
          (possibly empty) string.
        * fileExt - the part of the fileName after the last period. If
          fileBase is None it will also be None and if no period
          exists in the fileName it will be None.

        TODO: test these requirements and perhaps move them to the
        url util function.
          
        """
        return UrlPathUtils._split(self.__path)

    def join(self,other):
        """
        Joins a relative path on to the end of this path, correcting
        separator characters if necessary. If ``other`` is an absolute
        path ``other`` is returned, otherwise a new Path object is
        created using the joined path and returned.
        """
        return UrlPathUtils._join(self.__path,other)


    def getSeparator(self):
        """
        Returns '/' which is the standard Url separator character.
        """
        return '/'

    def isAbsolute(self):
        """
        Returns True since all HTTP paths are absolute.
        """
        return True


    def getAuthorisation(self):
        """
        Returns the currently set Authorisation object or None if none
        have been set yet.
        """
        return self.__auth

    def setAuthorisation(self,auth):
        """
        Sets the Authorisation object to use when performing
        requests. HTTP only supports (user, password) style
        authorisation, so an instance of the UserPasswordAuthorisation
        class is required.
        """
        self.__auth=auth


    def isFile(self):
        """
        Returns True if the path exists. All HTTP paths refer to a
        file so if the path exists, it's a file.
        """
        # TODO: check to make sure the path actually exists
        return True

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
        # TODO: could/should it actually just be called Link? More generic.
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
