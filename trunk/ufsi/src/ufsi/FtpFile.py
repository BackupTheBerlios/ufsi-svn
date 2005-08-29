"""
An FTP implementation of ``ufsi.FileInterface``.

"""

import ufsi
import FtpUtils

import ftplib


class FtpFile(ufsi.FileInterface):
    """
    """


    def __init__(self,path):
        """
        """
        self.__path=path
        self.__pathStr=str(path)
        self.__openMode=None
        self.__ftpObject=None
        self.__ftpDataSocket=None
        self.__ftpDataFile=None


    def __str__(self):
        return self.__pathStr


    def open(self,mode=None):
        """
        Only supports r, rb, w and wb modes.
        """
        # close any previously open file
        self.close()

        # do some validation on the mode
        if mode not in ('r','rb','w','wb'):
            raise ufsi.UnsupportedOperationError(
                    'The mode "%s" is not supported by the FTP '
                    'implementation of an ufsi.File object.'%mode)
        self.__openMode=mode

        urlPath=self.__path.split()['urlPath']
        if urlPath is None or urlPath=='':
            raise ufsi.PathNotFoundError(
                    'FTP path "%s" contains no file path.'
                    %self.__path)

        try:
            ftp=self.__ftpObject=FtpUtils.getFtpConnection(self.__path)

            # execute the appropriate ftp command(s)
            if 'b' in mode:
                ftp.voidcmd('TYPE I')
            else:
                ftp.voidcmd('TYPE A')

            if 'r' in mode:
                ftpCmd='RETR '+urlPath
            else:
                ftpCmd='STOR '+urlPath

            self.__ftpDataSocket=ftp.transfercmd(ftpCmd)
            self.__ftpDataFile=self.__ftpDataSocket.makefile(mode)
        except Exception,e:
            FtpUtils.handleException(e,self.__pathStr)

    def read(self,size=-1):
        return self.__ftpDataFile.read(size)

    def readLine(self):
        return self.__ftpDataFile.readline()

    def readLines(self):
        return self.__ftpDataFile.readlines()

    def write(self,s):
        self.__ftpDataFile.write(s)

    def writeLines(self,lines):
        self.__ftpDataFile.writelines(lines)

    def close(self):
        """
        Closes the FTP transfer.

        TODO: Look into the socket module's closing methods - they
        don't seem to close the socket. I may well be wrong, but if
        errors start to occur - look there.
        """
        if self.__ftpDataFile is not None:
            self.__ftpDataFile.close()
            self.__ftpDataFile=None

            self.__ftpDataSocket.close()
            self.__ftpDataSocket=None

            # TODO: look at this - abort is probably ok to be send on
            # successful download of a file, but it's not
            # correct. However, we need to determine how much of the
            # file is left otherwise.
            if 'w' in self.__openMode:
                self.__ftpObject.voidresp()
            else:
                self.__ftpObject.abort()
            self.__ftpObject.quit()


    def getStat(self):
        """
        Returns a dict of information about this file.
        """
        try:
            s=self.__path.split()
            ftp=FtpUtils.getFtpConnection(self.__path)
            dl=FtpUtils.getDirList(ftp,s['urlPath'])
            if not dl:
                raise ufsi.PathNotFoundError('Path "%s" not found.'
                                             %self.__path,e)
            return dl[s['fileName']]
        except Exception,e:
            FtpUtils.handleException(e,self.__pathStr)
            

    def getPath(self):
        """
        Returns a Path object for this file.
        """
        return self.__path

