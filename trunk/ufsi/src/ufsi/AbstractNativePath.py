"""

"""


import ufsi
import NativeUtils

import os


class AbstractNativePath(ufsi.PathInterface):
    def __init__(self,path):
        """
        """
        # check to make sure we're being given a string
        if not isinstance(path,basestring):
            raise TypeError('path must be a string.')
        
        self._path=path
        self._auth=None


    def __str__(self):
        """
        Returns this path as a string.
        """
        return self._path


    def join(self,other):
        """
        Joins ``other`` onto the end of this path and returns a new
        Path object. ``other`` must be a string or a Path object.
        """
        # TODO: should we take a list of other, as os.path does
        if not isinstance(other,ufsi.PathInterface):
            other=ufsi.Path(other)

        if other.isAbsolute():
            return other

        # Sort out separators
        selfSep=self.getSeparator()
        otherStr=str(other).replace(other.getSeparator(),selfSep)
        selfStr=self._path
        if not selfStr.endswith(selfSep):
            selfStr=selfStr+selfSep
        if otherStr.startswith(selfSep):
            otherStr=otherStr[len(selfSep):]

        return self.__class__(selfStr+otherStr)


    def isAbsolute(self):
        """
        Returns True if the path is an absolute path, False
        otherwise.
        """
        return os.path.isabs(self._path)


    def getAuthentication(self):
        """
        Returns the last Authentication object set on this Path object
        or None if none have been set. 
        """
        # TODO: do we need this??
        return self._auth

    def setAuthentication(self,auth):
        """
        Sets the Authentication object for this Path object and any
        File and Dir objects created by this Path.
        """
        self._auth=auth


    def isFile(self):
        """
        Returns True if this path refers to a file that exists on the
        native file system.
        """
        return os.path.isfile(self._path)

    def isDir(self):
        """
        Returns True if this path refers to a dir that exists on the
        native file system.
        """
        return os.path.isdir(self._path)

    def isSymlink(self):
        """
        Returns True if this path refers to a symlink that exists on
        the native file system.
        """
        return os.path.islink(self._path)


    def getFile(self):
        """
        Returns a File object for this path.
        """
        return ufsi.NativeFile(self)

    def getDir(self):
        """
        Returns a Dir object for this path.
        """
        return ufsi.NativeDir(self)

    def getSymlinkPath(self):
        """
        Returns a Path object that has the path that the symlink
        refers to.
        """
        if not self.isSymlink():
            raise ufsi.NotASymlinkError('%r is not a symlink'%self._path)

        try:
            return ufsi.Path(os.readlink(self._path))
        except Exception,e:
            NativeUtils.handleException(e,self._path)
