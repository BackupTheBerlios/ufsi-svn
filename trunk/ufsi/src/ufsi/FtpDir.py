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
        """
        Creates a new FtpDir object.


        Preconditions:
        
        * path is a Path object.
        * The path exists and is a dir.
        """
        self.__path=path
        self.__pathStr=str(path)


    def __str__(self):
        """
        Returns the path to this FTP dir as a string.
        """
        return self.__pathStr


    def getDirList(self,filter=None):
        """
        Returns a list of strings, the name of each dir or file in
        this directory.
        """
        try:
            ftp=FtpUtils.getFtpConnection(self.__path)
            d=FtpUtils.getDirList(ftp,self.__path.split()['urlPath'])
        except Exception,e:
            FtpUtils.handleException(e,self.__pathStr)
        items=d.keys()
        if '.' in items: del items['.']
        if '..' in items: del items['..']
        return items


    def getStat(self):
        """
        Returns a dict of information about this directory. Common
        values are:

        * size - size of the file system (as a string - may contain
          commas). TODO: remove commas from size.
        * permissions - a unix permissions string like: '-rwxrwxrwx'
        * owner - the owner of the file
        * group - the group of the file
          
        """
        try:
            # We must find the dir name in it's parent directory
            s=self.__path.split()
            urlPath=s['urlPath']
            if urlPath.endswith('/'):
                urlPath.pop()
            # Currently can't get any details from the root dir
            if urlPath=='':
                return {}

            # get parent dir (even if it's empty)
            parentDir=''
            dirName=urlPath
            if '/' in urlPath:
                (parentDir,dirName)=urlPath.rsplit('/',1)
                # cater for a urlPath of /dir
                parentDir+='/'

            ftp=FtpUtils.getFtpConnection(self.__path)
            
            dirList=FtpUtils.getDirList(ftp,parentDir)
            if dirName not in dirList:
                raise ufsi.PathNotFoundError('Path "%s" not found.'
                                             %self.__path)
            return dirList[dirName]
        except Exception,e:
            FtpUtils.handleException(e,self.__pathStr)


    def getPath(self):
        """
        Returns the path to this dir as a Path object.
        """
        return self.__path


