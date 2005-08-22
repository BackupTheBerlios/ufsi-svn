"""
An ``ufsi.PathInterface`` implementation for native linux paths.

"""
# TODO: this should probably be called NativeUnixPath. Not Linux.

import ufsi

import os
import os.path


class NativeLinuxPath(ufsi.PathInterface):
    """
    TODO: fill in and change linux to unix
    
    """

    
    def __init__(self,path):
        """
        Creates a Path object for a native unix path
        """
        self.__path=path
        self.__authorisation=None


    def __str__(self):
        """
        Returns the path that this Path object represents.
        """
        return self.__path


    def split(self):
        """
        Splits the path into:

        * protocol - always has the value 'NativePath'.
        * dirs - a list of directory names.
        * fileBase - any part of the fileName before the last period.
        * fileExt - any part of the fileName after the last period, or
          None if no period is present in the fileName.
        """
        (head,tail)=os.path.split(self.__path)
        dirs=head.split('/')
        (fileBase,fileExt)=os.path.splitext(tail)

        d={}
        d['protocol']='NativePath'
        d['dirs']=dirs
        d['fileBase']=fileBase
        d['fileExt']=fileExt

        return d

    def join(self,other):
        """
        Joins ``other`` onto the end of this path and returns a new
        Path object. ``other`` must be a string or a Path object.
        """
        # TODO: should we take a list of other, as os.path does
        otherStr=str(other)
        return ufsi.Path(os.path.join(self.__path,otherStr))


    def isAbsolute(self):
        """
        Returns True if the path is an absolute path, False
        otherwise.
        """
        return os.path.isabs(self.__path)


    def getSeparator(self):
        """
        Returns the separator character for native unix paths.
        """
        return '/'


    def getAuthorisation(self):
        """
        Returns the last Authorisation object set on this Path object
        or None if none have been set. 
        """
        # TODO: do we need this??
        return self.__authorisation

    def setAuthorisation(self,auth):
        """
        Sets the Authorisation object for this Path object and any
        File and Dir objects created by this Path.
        """
        self.__authorisation=auth


    def isFile(self):
        """
        Returns True if this path refers to a file that exists on the
        native file system.
        """
        return os.path.isfile(self.__path)

    def isDir(self):
        """
        Returns True if this path refers to a dir that exists on the
        native file system.
        """
        return os.path.isdir(self.__path)

    def isSymlink(self):
        """
        Returns True if this path refers to a symlink that exists on
        the native file system.
        """
        return os.path.islink(self.__path)


    def getFile(self):
        """
        Returns a File object for this path.
        """
        # TODO: set authorisation (if needed)
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
        TODO: should this be joined with this path or not?
        """
        return ufsi.Path(os.readlink(self.__path))


















