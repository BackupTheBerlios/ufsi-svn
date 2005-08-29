"""
(Modification time on iis)

Unix:
Is it hard links? inodes?
(?P<permissions>[a-z\\-]+)\s+(?P<hardLinks>[0-9]+)\s+(?P<user>[A-Za-z\\-]+)\s+(?P<group>[A-Za-z\\-])\s+(?P<size>[0-9]+)\s+(?P<date>[A-Za-z]+\s+[0-9]+\s+[0-9:]+)\s+(?P<fileName>.+)
-rwxrwxrwx   1 owner    group              32 Aug 28 20:09 existing^M
-rwxrwxrwx   1 owner    group               0 Aug 28 20:09 whoi-or-what the hell is this meant to come up as.txt^M


MsDos:
(?P<date>[0-9]+-[0-9]+-[0-9]+\s+[0-9]+:[0-9]+(AM|PM))\s+(?P<size>[0-9]+)\s+(?P<fileName>.+)
08-28-05  08:10PM                   32 existing^M
08-28-05  08:09PM                    0 whoi-or-what the hell is this meant to come up as.txt^M


"""


import ufsi
import FtpUtils

import ftplib



class FtpDir(ufsi.DirInterface):
    """
    """

    def __init__(self,path):
        self.__path=path


    def __str__(self):
        return str(self.__path)


    def getDirList(self,filter=None):
        """
        """
        ftp=FtpUtils.getFtpConnection(self.__path)
        d=FtpUtils.getDirList(ftp,self.__path.split()['urlPath'])
        return d.keys()


    def getStat(self):
        """
        Returns a dict of information about this directory.
        """
        try:
            # TODO: finish fixing this up for a trailing slash
            # TODO: alternately - is is better to strip a trailing slash? - we know it's a dir...? Trent?
            s=self.__path.split()
            urlPath=s['urlPath']
            if urlPath.endswith('/'):
                urlPath.pop()
            ftp=FtpUtils.getFtpConnection(self.__path)
            
            dl=FtpUtils.getDirList(ftp,urlPath)
            if not dl:
                raise ufsi.PathNotFoundError('Path "%s" not found.'
                                             %self.__path,e)
            return dl[s['fileName']]
        except Exception,e:
            FtpUtils.handleException(e,self.__pathStr)


    def getPath(self):
        """
        Returns the path to this dir as a Path object.
        """
        return self.__path


