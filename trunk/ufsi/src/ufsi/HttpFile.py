"""
A HTTP implementation of ``ufsi.FileInterface``.
"""

import ufsi

import urllib2


class HttpFile(ufsi.FileInterface):
    """
    HttpFile is an implementation of ``ufsi.FileInterface`` that
    provides an interface to HTTP file systems. HTTP file systems
    (unless they are enhanced with WebDAV, or some other equivalent
    technology) are read-only file systems. Therefore, trying to write
    to one will result in an UnsupportedOperationError being raised.
    """


    def __init__(self,path):
        """
        Creates a HttpFile instance.
        """
        self.__path=path
        self.__pathStr=str(path)
        self.__fileHandle=None


    def __str__(self):
        """
        Returns the path (string) to the file.
        """
        return pathStr


    def open(self,mode=None):
        """
        Opens a HTTP connection to the file. If a previous connection
        was opened it is first closed. TODO: currently, mode is
        ignored but we should do a little more validation on it.
        """
        self.close()
        self.__fileHandle=urllib2.urlopen(self.__pathStr)
    
    def read(self,size=None):
        """
        Reads ``size`` bytes from the file (or a default number, if
        ``size`` isn't provided). If EOF is encountered before
        ``size`` bytes are read, all bytes to the EOF are returned.
        """
        if size is None:
            return self.__fileHandle.read()
        else:
            return self.__fileHandle.read(size)

    def readLine(self):
        """
        Reads a single line from the file.
        """
        return self.__fileHandle.readline()

    def readLines(self):
        """
        Reads the entire file into a list of lines.
        """
        return self.__fileHandle.readlines()

    def write(self,s):
        """
        HTTP doesn't allow writing. This method raises an
        UnsupportedOperationError.
        """
        raise ufsi.UnsupportedOperationError('HTTP has no facility to write.')

    def writeLines(self,lines):
        """
        HTTP doesn't allow writing. This method raises an
        UnsupportedOperationError.
        """
        raise ufsi.UnsupportedOperationError('HTTP has no facility to write.')

    def close(self):
        """
        Closes the HTTP connection.
        """
        if self.__fileHandle is not None:
            self.__fileHandle.close()


    def getStat(self):
        """
        Returns the HTTP response headers as a dictionary.
        """
        fh=urllib2.urlopen(self.__pathStr)
        d=fh.info()
        fh.close()

        return d


    def getPath(self):
        """
        Returns the http path to this file.
        """
        return self.__path


