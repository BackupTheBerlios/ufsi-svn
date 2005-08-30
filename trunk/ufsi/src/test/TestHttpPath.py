
"""
Tests the HttpPath implementation.

"""


import ufsi

import os
import stat
import unittest



class TestHttpPath(unittest.TestCase):
    """
    Tests the HttpPath implementation.
    
    """


    def setUp(self):
        """
        Creates the test data:

        * existing dir, contents unimportant
        * non existing dir

        TODO: update docstring
        TODO: add index.html or something like that to existingDir

        """
        # location of the testing server
        host='hyde'
        server='http://'+host+'/'
        
        # paths
        self.existingDirPathStr=server+'existingDir/'
        self.nonExistingDirPathStr=server+'nonexistingDir/'
        self.existingFilePathStr=server+'existing'
        self.nonExistingFilePathStr=server+'nonexisting'

        # TODO: test symlinks

        self.server=server
        self.host=host


    def testSplit(self):
        """
        Tests the split() method.

        1. empty urlPath
        2. urlPath of a fileBase only
        3. urlPath of a fileExt only
        4. urlPath of a fileBase with empty fileExt
        5. urlPath with a full fileName
        6. urlPath with a single dir
        7. urlPath with two dirs
        8. urlPath with two dirs, full fileName
        9. urlPath with a dir with a period

        TODO: also test port numbers, user and passwords

        """
        server=self.server
        data={
            # 1
            'emptyPath':
            [server+'',
             {'host':self.host,
              'urlPath':'',
              'fileBase':'',
              'fileExt':None,
              'dirs':[]}],

            # 2
            'fileBaseOnly':
            [server+'fileBase',
             {'host':self.host,
              'urlPath':'fileBase',
              'fileBase':'fileBase',
              'fileExt':None,
              'dirs':[]}],
            
            # 3
            'fileExtOnly':
            [server+'.ext',
             {'host':self.host,
              'urlPath':'.ext',
              'fileBase':'',
              'fileExt':'ext',
              'dirs':[]}],

            # 4
            'fileBaseEmptyFileExt':
            [server+'fileBase.',
             {'host':self.host,
              'urlPath':'fileBase.',
              'fileBase':'fileBase',
              'fileExt':'',
              'dirs':[]}],

            # 5
            'fullFileName':
            [server+'fileBase.ext',
             {'host':self.host,
              'urlPath':'fileBase.ext',
              'fileBase':'fileBase',
              'fileExt':'ext',
              'dirs':[]}],

            # 6
            'singleDir':
            [server+'dir/',
             {'host':self.host,
              'urlPath':'dir/',
              'fileBase':'',
              'fileExt':None,
              'dirs':['dir']}],

            # 7
            'twoDirs':
            [server+'dir1/dir2/',
             {'host':self.host,
              'urlPath':'dir1/dir2/',
              'fileBase':'',
              'fileExt':None,
              'dirs':['dir1','dir2']}],

            # 8
            'absolutePathTwoDirsFullFileName':
            [server+'dir1/dir2/fileBase.ext',
             {'host':self.host,
              'urlPath':'dir1/dir2/fileBase.ext',
              'fileBase':'fileBase',
              'fileExt':'ext',
              'dirs':['dir1','dir2']}],

            # 9
            'dirWithAPeriod':
            [server+'dir.dirExt/fileBase.fileExt',
             {'host':self.host,
              'urlPath':'dir.dirExt/fileBase.fileExt',
              'fileBase':'fileBase',
              'fileExt':'fileExt',
              'dirs':['dir.dirExt']}]
        }

        for k in data.iterkeys():
            s1=ufsi.HttpPath(data[k][0]).split()
            s2=data[k][1]
            for s2k in s2.iterkeys():
                self.assertEquals(s1[s2k],s2[s2k],
                                  '%s: Item %s of dict %r should be %s'
                                  %(k,s2k,s1,s2[s2k]))

    def testJoin(self):
        """
        Tests the join() method.

        1. append a relative path
        2. append an absolute path
        3. append to a path not terminated by a separator character
        4. append an empty path
        
        """
        server=self.server
        P=lambda p:ufsi.Path(p)
        data={
            # 1
            'relativePath':
            [server+'dir1/',P('dir2/fileBase.ext'),
             server+'dir1/dir2/fileBase.ext'],

            # 2
            'absolutePath':
            [server+'dir1/',P('/dir2/fileBase.ext'),
             str(P('/dir2/fileBase.ext'))],

            # 3
            'notSeparatorTerminatedPath':
            [server+'dir1',P('dir2/fileBase.ext'),
             server+'dir1/dir2/fileBase.ext'],

            # 4
            'emptyPath':
            [server+'dir1',P(''),server+'dir1/'],
        }

        for k in data.iterkeys():
            p1=ufsi.HttpPath(data[k][0])
            p2=data[k][1]
            r1=str(p1.join(p2))
            r2=data[k][2]
            self.assertEquals(r1,r2,
                              '%s: join result was %r but should have been %r'
                              %(k,r1,r2))


    def testIsAbsolute(self):
        """
        Tests the isAbsolute() method.

        1. server without trailing slash
        2. server with trailing slash
        3. server with file
        4. server with dir

        """
        server=self.server
        data={
            # 1
            'noTrailingSlash':[server[:-1],True],
            # 2
            'trailingSlash':[server,True],
            # 3
            'serverFile':[server+'file',True],
            # 4
            'serverDir':[server+'dir/',True]
        }

        for k in data.iterkeys():
            r1=ufsi.HttpPath(data[k][0]).isAbsolute()
            r2=data[k][1]
            self.assertEquals(r1,r2,
                              '%s: isAbsolute result was %r but should be %r'
                              %(k,r1,r2))


    def testIsFile(self):
        """
        Tests the isFile() method.

        1. existing file
        2. non-existing file
        # FIX: 3. existing file referenced through a symlink
        # FIX: 4. non-existing file referenced through a symlink
        5. existing dir

        """
        P=lambda p:ufsi.HttpPath(p)
        existingFilePath=P(self.existingFilePathStr)
        nonExistingFilePath=P(self.nonExistingFilePathStr)
        #existingValidFileSymlinkPath=P(self.existingValidSymlinkFilePathStr)
        #existingInvalidFileSymlinkPath=\
        #        P(self.existingInvalidSymlinkFilePathStr)
        existingDirPath=P(self.existingDirPathStr)


        # 1
        self.assertEquals(existingFilePath.isFile(),True,
                          '%r is a file'%str(existingFilePath))

        # 2
        self.assertEquals(nonExistingFilePath.isFile(),False,
                          'File %r does not exist'%str(nonExistingFilePath))

        # 3
        #self.assertEquals(existingValidFileSymlinkPath.isFile(),True,
        #                  '%r is a file'%str(existingValidFileSymlinkPath))

        # 4
        #self.assertEquals(existingInvalidFileSymlinkPath.isFile(),False,
        #                  '%r is an invalid symlink'
        #                  %str(existingInvalidFileSymlinkPath))

        # 5
        self.assertEquals(existingDirPath.isFile(),True,
                          '%r is a file'%str(existingDirPath))
        

    def testIsSymlink(self):
        """
        Tests the isSymlink() method.

        1. existing valid symlink
        2. existing invalid symlink
        3. non-existing symlink

        TODO: implement is symlink stuff
        """
        ## P=lambda p:ufsi.NativeUnixPath(p)
##         existingValidSymlinkPath=P(self.existingValidSymlinkFilePathStr)
##         existingInvalidSymlinkPath=P(self.existingInvalidSymlinkFilePathStr)
##         nonExistingSymlinkPath=P(self.nonExistingSymlinkPathStr)

##         # 1
##         self.assertEquals(existingValidSymlinkPath.isSymlink(),True,
##                           'Symlink %r exists'
##                           %str(existingValidSymlinkPath))

##         # 2
##         self.assertEquals(existingInvalidSymlinkPath.isSymlink(),True,
##                           'Symlink %r exists'
##                           %str(existingInvalidSymlinkPath))

##         # 3
##         self.assertEquals(nonExistingSymlinkPath.isSymlink(),False,
##                           'Symlink %r does not exist'
##                           %str(nonExistingSymlinkPath))


    def testGetSymlinkPath(self):
        """
        Tests the getSymlinkPath() method.

        1. existing symlink to a file
        2. existing symlink to a dir
        3. existing file
        4. existing dir
        5. non-existing symlink

        TODO: implement is symlink stuff

        """
##         P=lambda p:ufsi.NativeUnixPath(p)
##         existingValidFileSymlinkPath=P(self.existingValidSymlinkFilePathStr)
##         existingValidDirSymlinkPath=P(self.existingValidSymlinkDirPathStr)
##         existingFilePath=P(self.existingFilePathStr)
##         existingDirPath=P(self.existingDirPathStr)
##         nonExistingSymlinkPath=P(self.nonExistingSymlinkPathStr)

##         # 1
##         r1=str(existingValidFileSymlinkPath.getSymlinkPath())
##         r2=self.existingValidFileSymlinkPath
##         self.assertEquals(r1,r2,'Symlink path expected %r. Got %r'%(r2,r1))
        
##         # 2
##         r1=str(existingValidDirSymlinkPath.getSymlinkPath())
##         r2=self.existingValidDirSymlinkPath
##         self.assertEquals(r1,r2,'Symlink path expected %r. Got %r'%(r2,r1))

##         # 3
##         self.assertRaises(ufsi.NotASymlinkError,
##                           existingFilePath.getSymlinkPath)

##         # 4
##         self.assertRaises(ufsi.NotASymlinkError,
##                           existingDirPath.getSymlinkPath)

##         # 5
##         self.assertRaises(ufsi.NotASymlinkError,
##                           nonExistingSymlinkPath.getSymlinkPath)
