"""

"""


import ufsi

import os

class NativeWindowsPath(ufsi.AbstractNativePath):
    """
    """

    __super=ufsi.AbstractNativePath


    def __init__(self,path):
        """
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
        

    def getSeparator(self):
        return '\\'

