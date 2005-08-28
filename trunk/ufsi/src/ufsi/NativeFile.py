"""
An ``ufsi.FileInterface`` implementation for native file systems.

"""

import ufsi
import NativeUtils

import os


class NativeFile(ufsi.FileInterface):
    """
    The NativeFile class implements the ``ufsi.FileInterface`` for
    files on natively supported file systems.
    """


    def __init__(self,path):
        """
        Creates a NativeFile for the NativePath in ``path``.
        """
        self.__path=path
        self.__pathStr=str(path)
        self.__fileHandle=None


    def __str__(self):
        """
        Returns the path to this File.
        """
        return self.__pathStr


    def open(self,mode=None):
        """
        Opens the file for io using the read... and
        write... methods. Before opening the file it closes a
        previously opened file.
        """
        # TODO: change the default mode from None to 'r'
        self.close()

        try:
            if mode is None:
                self.__fileHandle=file(self.__pathStr)
            else:
                self.__fileHandle=file(self.__pathStr,mode)
        except Exception,e:
            NativeUtils.handleException(e,self.__pathStr)

    def read(self,size=None):
        """
        Reads up to ``size`` bytes of the file or to EOF if ``size``
        isn't provided. Returns the bytes as a string. If the file is
        already at EOF before attempting the read an empty string is
        returned.


        Preconditions:

        * The file must be open with a read mode.
        
        """
        # TODO: insert check for file being open
        if size is None:
            return self.__fileHandle.read()
        else:
            return self.__fileHandle.read(size)

    def readLine(self):
        """
        Reads the next line of the file. The trailing end of line
        character(s) are left on. If the file is already at EOF an
        empty string is returned. 

        Preconditions:

        * The file must be open with a read mode.
        """
        return self.__fileHandle.readline()

    def readLines(self):
        """
        Reads the rest of the file into a list of lines. Each line
        retains the trailing end of line character(s).
        """
        return self.__fileHandle.readlines()

    def write(self,s):
        """
        Writes the string to the file.
        """
        self.__fileHandle.write(s)

    def writeLines(self,lines):
        """
        Writes an array of strings to the file. No end of line
        character(s) are inserted between each line so each line
        should contain trailing end of line character(s).
        """
        self.__fileHandle.writelines(lines)

    def close(self):
        """
        Closes the file if it is open.


        Postconditions:

        * The file is closed.
        """
        if self.__fileHandle!=None:
            self.__fileHandle.close()
            self.__fileHandle==None


    def getStat(self):
        """
        Returns a dict of information about the file. The keys are:

        * size
        * accessTime
        * modificationTime
        * creationTime
        * permissions - a string of the octal unix permissions.
        
        """
        # TODO: update docstring
        try:
            return NativeUtils.convertStatObjectToDict(
                    os.stat(self.__pathStr))
        except Exception,e:
            NativeUtils.handleException(e,self.__pathStr)


    def getPath(self):
        """
        Returns a Path object for this File.
        """
        return self.__path



