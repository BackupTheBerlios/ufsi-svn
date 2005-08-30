"""
A HTTP implementation of ``ufsi.FileInterface``.

"""

import ufsi
import HttpUtils

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
        return self.__pathStr


    def open(self,mode='r'):
        """
        Opens a HTTP connection to the file. If a previous connection
        was opened it is first closed. TODO: currently, mode is
        ignored but we should do a little more validation on it.

        TODO: add this level of error checking to other open methods
        TODO: make mode='r' for all, ie part of the interface
        TODO: write Interface Implementation certification code to
        ensure an implementation adheres to at least the method sigs

        Note: if you get freezes from any of the methods that open a
        connection to the server, it may be some issue between the
        sockets (or something to do with the makefile layer of
        socket). I have only experienced these problems using
        IIS5.something. Good Luck! :-)
        
        """
        self.close()
        if mode in ('r','rb'):
            try:
                self.__fileHandle=urllib2.urlopen(self.__pathStr)
            except Exception,e:
                HttpUtils.handleException(e,self.__pathStr)
        elif mode in ('w','wb','a','ab'):
            raise ufsi.UnsupportedOperationError(
                    'HTTP has no facility to write.')
        else:
            raise ufsi.InvalidArgumentError('Unknown mode %r'%mode)
        
    def read(self,size=-1):
        """
        Reads ``size`` bytes from the file (or a default number, if
        ``size`` isn't provided). If EOF is encountered before
        ``size`` bytes are read, all bytes to the EOF are returned.

        """
        if size==-1:
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
            self.__fileHandle=None


    def getStat(self):
        """
        Returns the HTTP response headers as a dictionary.
        """
        try:
            fh=urllib2.urlopen(self.__pathStr)
            d=fh.info()
            fh.close()
        except Exception,e:
            HttpUtils.handleException(e,self.__pathStr)

        return d


    def getPath(self):
        """
        Returns the http path to this file.
        """
        return self.__path


