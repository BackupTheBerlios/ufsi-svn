"""
Notes: There are two possible ways of reading and writing files to ftp
- we can either cache everything on the first read call and cache
everything until the close for writing, or try to do it at runtime. I
think, because the ftplib module uses a file object that we have to go
with the former, at least for writing.

Therefore every transaction requires a separate connection (atm).
"""

import ufsi

import ftplib

# TODO: experiment with urllib2 support.
import urllib2


class FtpFile(ufsi.FileInterface):
    def __init__(self,path):
        self.__path=path
        self.__pathStr=str(path)
        self.__auth=None
        self.__ftpObject=None
        self.__ftpDataSocket=None
        self.__openFileCache=None


    def __str__(self):
        return self.__pathStr


    def open(self,mode=None):
        """
        Only supports r, rb, w and wb modes.
        """
        # close any previously open file
        self.close()

        # TODO: validate mode
        if mode not in ('r','rb','w','wb'):
            raise ufsi.UnsupportedOperationError(
                    'The mode "%s" is not supported by the FTP '\
                    'implementation of an ufsi.File object.'%mode)

        s=self.__path.split()
        host=s['host']
        dirs=s['dirs']
        fileBase=s['fileBase']
        fileExt=s['fileExt']
        filePath='/'.join(dirs)+(dirs and '/' or '')+fileBase
        if fileExt is not None:
            filePath+='.'+fileExt
            
        if 'r' in mode:
            # TODO: add use of authentication
            ftp=self.__ftpObject=ftplib.FTP(host,'d232925','d35cr1p70r')
            self.__ftpDataSocket=ftp.transfercmd('RETR '+filePath)

        else:
            # test for ability to create now and open and write on close
            pass


    def read(self,size=None):
        if size is not None:
            return self.__ftpDataSocket.recv(size)
        else:
            s=''
            # TODO: create constant for min transfer size
            r=self.__ftpDataSocket.recv(8192)
            while len(r)>0:
                s+=r
                r=self.__ftpDataSocket.recv(8192)

            return s
        """
        index=self.__openFileCache['index']
        buffer=self.__openFileCache['buffer']

        # if size is None read to the end of the buffer
        if size is None:
            return buffer[index:]
        else:
            return buffer[index:index+size]
        """

    def readLine(self):
        index=self.__openFileCache['index']
        buffer=self.__openFileCache['buffer']
        eolIndex=buffer.find(buffer,index)
        
        if eolIndex==-1:
            eolIndex=len(buffer)
        
        self.__openFileCache['index']=eolIndex
        return buffer[index:eolIndex]

    def readLines(self):
        index=self.__openFileCache['index']
        buffer=self.__openFileCache['buffer']
        self.__openFileCache['index']=len(buffer)
        return buffer[index:].splitlines(True)

    def write(self,s):
        buffer+=s

    def writeLines(self,lines):
        buffer+=''.join(lines)

    def close(self):
        """
        if self.__openFileCache is not None:
            if 'w' in self.__openFileCache['mode']:
                # TODO: write file to ftp

            # empty the cache
            self.__openFileCache=None
        """
        if self.__ftpDataSocket is not None:
            self.__ftpDataSocket.close()
            self.__ftpObject.voidresp()
            self.__ftpDataSocket=None
            self.__ftpObject.quit()

    def getStat(self):
        pass

    def getPath(self):
        """
        Returns a Path object for this file.
        """
        return self.__path

