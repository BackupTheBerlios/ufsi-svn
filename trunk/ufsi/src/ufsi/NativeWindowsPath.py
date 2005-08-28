"""

"""


import ufsi

import os
import re

class NativeWindowsPath(ufsi.AbstractNativePath):
    """
    """

    __super=ufsi.AbstractNativePath


    def __init__(self,path):
        """
        """
        # windows recognises '/' characters (but we'll be correct)
        path=path.replace('/','\\')
        self.__super.__init__(self,path)
        self.__split=None


    def split(self):
        """
        """
        # check for a cached version
        if self.__split is not None:
            return self.__split.copy()

        # else split it and cache it
        # format [C:][\]dir\file.ext

        p=self._path

        # defaults
        drive=None
        dirs=[]
        fileBase=''
        fileExt=None

        # drive
        if re.match('[A-Za-z]:',p):
            drive=p[0]
            p=p[2:]

        # dirs
        dirs=p.split('\\')
        fileBase=dirs.pop()
        if '.' in fileBase:
            (fileBase,fileExt)=fileBase.rsplit('.',1)

        # create the dict, cache it and return a copy
        d={}
        d['drive']=drive
        d['dirs']=dirs
        d['fileBase']=fileBase
        d['fileExt']=fileExt
        self.__split=d
        return d.copy()


    def getSeparator(self):
        """
        Returns the standard Windows dir separator of '\\'. A path on
        windows may also be created using '/' characters as Windows
        does recognise them, but all '/' characters are converted to
        '\\' characters on creation of a Path object.
        """
        return '\\'

