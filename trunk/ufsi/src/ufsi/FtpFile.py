"""
Notes: There are two possible ways of reading and writing files to ftp
- we can either cache everything on the first read call and cache
everything until the close for writing, or try to do it at runtime. I
think, because the ftplib module uses a file object that we have to go
with the former, at least for writing.

Therefore every transaction requires a separate connection (atm).
"""

import ufsi

import urllib2


class FtpFile(ufsi.FileInterface):
    def __init__(self,path):
        self.__path=path
        self.__pathStr=str(path)
        self.__auth=None
        self.__ftpObject=None


    def __str__(self):
        return self.__pathStr


    def open(self,mode=None):
        # TODO: do something with the mode
        if 'r' in mode:
            host=self.__path.split()['host']
            # open now
            # TODO: add use of authentication
            self.__ftpObject=ftplib.FTP(host)
            
        else:
            # test for ability to create now and open and write on close
            pass




    def write(self):
        pass
