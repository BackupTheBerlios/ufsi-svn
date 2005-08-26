"""
An FTP implementation of ``ufsi.FileInterface``.
"""

import ufsi

import ftplib


class FtpFile(ufsi.FileInterface):
    """
    """
    def __init__(self,path):
        """
        """
        self.__path=path
        self.__pathStr=str(path)
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

        # get the various parts required to perform the open
        s=self.__path.split()
        host=s['host']
        port=(s['port'] and s['port'] or 0)
        urlPath=s['urlPath']
        if urlPath is None or urlPath=='':
            raise ufsi.PathNotFoundError(
                    'FTP path "%s" contains no file path.'
                    %self.__path)

        # defaults
        user=''
        password=''
        auth=self.__path.getAuthorisation()
        if auth is not None:
            if isinstance(auth,ufsi.UserPasswordAuthentication):
                user=auth.getUser()
                password=auth.getPassword()
            else:
                raise ufsi.UnsupportedAuthenticationError(
                        'FTP only uses user,password authentication')
        
        # open the connection and log in
        ftp=self.__ftpObject=ftplib.FTP()
        ftp.connect(host,port)
        ftp.login(user,password)
        if 'r' in mode:
            ftpCmd='RETR '+urlPath
        else:
            ftpCmd='STOR '+urlPath

        self.__ftpDataSocket=ftp.transfercmd(ftpCmd)
        self.__ftpDataFile=self.__ftpDataSocket.makefile(mode)

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
            
            self.__ftpObject.voidresp()
            self.__ftpObject.quit()


    def getStat(self):
        pass

    def getPath(self):
        """
        Returns a Path object for this file.
        """
        return self.__path

