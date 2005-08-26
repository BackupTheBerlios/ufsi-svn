"""
An ``ufsi.PathInterface`` implementation for native unix paths.

"""


import ufsi

import os
import os.path


class NativeUnixPath(ufsi.AbstractNativePath):
    """
    TODO: fill in
    
    """

    __super=ufsi.AbstractNativePath
    
    def __init__(self,path):
        """
        Creates a Path object for a native unix path
        """
        self.__super.__init__(self,path)
        self.__split=None


    def split(self):
        """
        Splits the path into:

        * protocol - always has the value 'NativePath'.
        * dirs - a list of directory names.
        * fileBase - any part of the fileName before the last period.
        * fileExt - any part of the fileName after the last period, or
          None if no period is present in the fileName.
        """
        # check for a cached version
        if self.__split is not None:
            return self.__split.copy()

        # else split it and cache it
        (head,tail)=os.path.split(self.__path)
        dirs=head.split('/')
        (fileBase,fileExt)=os.path.splitext(tail)

        d={}
        d['protocol']='NativePath'
        d['dirs']=dirs
        d['fileBase']=fileBase
        d['fileExt']=fileExt

        self.__split=d
        return d


    def getSeparator(self):
        """
        Returns the separator character for native unix paths.
        """
        return '/'

