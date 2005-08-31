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
        Creates an FtpFile object for the path.

        Preconditions:

        * The path actually exists and is a file.
        
        """
        self.__path=path
        self.__pathStr=str(path)
        self.__openMode=None
        self.__ftpObject=None
        self.__ftpDataSocket=None
        self.__ftpDataFile=None


    def __str__(self):
        """
        Returns the path to this file as a string.
        """
        return self.__pathStr


    def open(self,mode=None):
        """
        Opens a file for reading or writing. Mode must be one of
        r, rb, w or wb. If the file was previously open it is first
        closed.

        Raises:
        * PathNotFoundError if the file couldn't be found.
        * InvalidArgumentError if the mode isn't one of the accepted values.

        """
        # close any previously open file
        self.close()

        # do some validation on the mode
        if mode not in ('r','rb','w','wb'):
            raise ufsi.InvalidArgumentError(
                    'Invalid mode: "%s"'%mode)
        self.__openMode=mode

        urlPath=self.__path.split()['urlPath']
        if not urlPath:
            raise ufsi.PathNotFoundError(
                    'FTP path "%s" contains no file path.'%self.__path)

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
        """
        Reads up to size bytes from the file, or to the end of the file if
        size is omitted.
        """
        return self.__ftpDataFile.read(size)

    def readLine(self):
        """
        Reads the next line out of the file.
        """
        return self.__ftpDataFile.readline()

    def readLines(self):
        """
        Reads the rest of the file as a series of lines.
        """
        return self.__ftpDataFile.readlines()

    def write(self,s):
        """
        Writes a string to the file.
        """
        self.__ftpDataFile.write(s)

    def writeLines(self,lines):
        """
        Writes a series of strings (passed as a list) to the
        file. Note that no end of line character is written after
        writing each string, therefore you need to include it in the
        strings.
        """
        self.__ftpDataFile.writelines(lines)

    def close(self):
        """
        Closes the file if it is open, otherwise it does nothing.

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
            # TODO: got:
            '''
            *cmd* 'QUIT'
            *put* 'QUIT\r\n'
            *get* '221 You could at least say goodbye.\r\n'
            *resp* '221 You could at least say goodbye.'
            '''
            # Am i being rude? :-) investigate
            self.__ftpObject.quit()


    def getStat(self):
        """
        Returns a dict of information about this file.

        Expects the path to NOT end in a '/'.
        """
        try:
            s=self.__path.split()
            ftp=FtpUtils.getFtpConnection(self.__path)
            dl=FtpUtils.getDirList(ftp,s['urlPath'])
            ftp.quit()
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

