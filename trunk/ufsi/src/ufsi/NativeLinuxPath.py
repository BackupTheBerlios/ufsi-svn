"""
An ``ufsi.PathInterface`` implementation for native linux paths.

"""
# TODO: this should probably be called NativeUnixPath. Not Linux.

import ufsi

import os
import os.path


class NativeLinuxPath(ufsi.PathInterface):
    def __init__(self,path):
        """
        """
        self.__path=path
        self.__authorisation=None


    def __str__(self):
        """
        """
        return self.__path


    def split(self):
        """
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
        """
        # TODO: should we take a list of other, as os.path does
        otherStr=str(other)
        return ufsi.Path(os.path.join(self.__path,otherStr))


    def isAbsolute(self):
        """
        """
        return os.path.isabs(self.__path)


    def getSeparator(self):
        """
        """
        return '/'


    def getAuthorisation(self):
        """
        """
        # TODO: do we need this??
        return self.__authorisation

    def setAuthorisation(self,auth):
        """
        """
        self.__authorisation=auth


    def isFile(self):
        """
        """
        return os.path.isfile(self.__path)

    def isDir(self):
        """
        """
        return os.path.isdir(self.__path)

    def isSymlink(self):
        """
        """
        return os.path.islink(self.__path)


    def getFile(self):
        """
        """
        # TODO: set authorisation (if needed)
        return ufsi.NativeFile(self)

    def getDir(self):
        """
        """
        return ufsi.NativeDir(self)

    def getSymlinkPath(self):
        """
        """
        return ufsi.Path(os.readlink(self.__path))


















