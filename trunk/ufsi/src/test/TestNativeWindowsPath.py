"""
Tests the NativeWindowsPath implementation.

"""


import ufsi

import os
import stat
import unittest



class TestNativeWindowsPath(unittest.TestCase):
    """
    Tests the NativeWindowsPath implementation.


    Preconditions: 

    * it is being run on a windows compatible operating system.
    
    """


    def setUp(self):
        """
        Creates the test data:

        * existing dir, contents unimportant
        * non existing dir

        """
        
        if os.name!='nt':
            raise Exception('This class must be run on a win compatible os')

        # paths
        self.existingDirPathStr='data\\existingDir\\'
        self.nonExistingDirPathStr='data\\nonexistingDir\\'
        self.existingFilePathStr='data\\existing'
        self.nonExistingFilePathStr='data\\nonexisting'

        # existing dir
        p=self.existingDirPathStr
        if not os.path.isdir(p):
            os.makedirs(p)
        assert os.path.isdir(p)

        # non existing file
        p=self.nonExistingDirPathStr
        if os.path.isdir(p):
            os.rmdir(p)
        assert os.path.exists(p)==False

        # existing file
        p=self.existingFilePathStr
        f=file(p,'w')
        f.close()
        assert os.path.isfile(p)

        # non existing file
        p=self.nonExistingFilePathStr
        if os.path.isfile(p):
            os.remove(p)
        assert os.path.exists(p)==False


    def testSplit(self):
        """
        Tests the split() method.

        1. empty path
        2. fileBase only
        3. fileExt only
        4. fileBase with empty fileExt
        5. full fileName
        6. single dir
        7. two dirs
        8. absolute path, two dirs, full fileName
        9. dir with a period
        10. drive based path
        11. drive relative path
        12. path with forward slashes

        """
        data={
            # 1
            'emptyPath':
            ['',{'drive':None,
                 'fileBase':'',
                 'fileExt':None,
                 'dirs':[]}],

            # 2
            'fileBaseOnly':
            ['fileBase',{'drive':None,
                         'fileBase':'fileBase',
                         'fileExt':None,
                         'dirs':[]}],
            
            # 3
            'fileExtOnly':
            ['.ext',{'drive':None,
                     'fileBase':'',
                     'fileExt':'ext',
                     'dirs':[]}],

            # 4
            'fileBaseEmptyFileExt':
            ['fileBase.',{'drive':None,
                          'fileBase':'fileBase',
                          'fileExt':'',
                          'dirs':[]}],

            # 5
            'fullFileName':
            ['fileBase.ext',{'drive':None,
                             'fileBase':'fileBase',
                             'fileExt':'ext',
                             'dirs':[]}],

            # 6
            'singleDir':
            ['dir\\',{'drive':None,
                      'fileBase':'',
                      'fileExt':None,
                      'dirs':['dir']}],

            # 7
            'twoDirs':
            ['dir1\\dir2\\',{'drive':None,
                             'fileBase':'',
                             'fileExt':None,
                             'dirs':['dir1','dir2']}],

            # 8
            'absolutePathTwoDirsFullFileName':
            ['\\dir1\\dir2\\fileBase.ext',{'drive':None,
                                           'fileBase':'fileBase',
                                           'fileExt':'ext',
                                           'dirs':['','dir1','dir2']}],

            # 9
            'dirWithAPeriod':
            ['\\dir.dirExt\\fileBase.fileExt',{'drive':None,
                                               'fileBase':'fileBase',
                                               'fileExt':'fileExt',
                                               'dirs':['','dir.dirExt']}],

            # 10
            'driveBased':
            ['c:\\dir\\file.ext',{'drive':'c',
                                  'fileBase':'file',
                                  'fileExt':'ext',
                                  'dirs':['','dir']}],

            # 11
            'driveRelative':
            ['c:dir\\file.ext',{'drive':'c',
                                'fileBase':'file',
                                'fileExt':'ext',
                                'dirs':['dir']}],

            # 12
            'forwardSlashes':
            ['c:/dir/file.ext',{'drive':'c',
                                'fileBase':'file',
                                'fileExt':'ext',
                                'dirs':['','dir']}],
        }

        for k in data.iterkeys():
            s1=ufsi.NativeWindowsPath(data[k][0]).split()
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
        5. append a non-native path
        
        """
        P=lambda p:ufsi.NativeWindowsPath(p)
        data={
            # 1
            'relativePath':
            ['\\dir1\\',P('dir2\\fileBase.ext'),'\\dir1\\dir2\\fileBase.ext'],

            # 2
            'absolutePath':
            ['\\dir1\\',P('C:\\dir2\\fileBase.ext'),'C:\\dir2\\fileBase.ext'],

            # 3
            'notSeparatorTerminatedPath':
            ['dir1',P('dir2\\fileBase.ext'),'dir1\\dir2\\fileBase.ext'],

            # 4
            'emptyPath':
            ['dir1',P(''),'dir1\\'],

            # 5
            'nonNativePath':
            ['dir1',ufsi.HttpPath('http://www.google.com.au/'),
             'http://www.google.com.au/']
        }

        for k in data.iterkeys():
            p1=P(data[k][0])
            p2=data[k][1]
            r1=str(p1.join(p2))
            r2=data[k][2]
            self.assertEquals(r1,r2,
                              '%s: join result was %r but should have been %r'
                              %(k,r1,r2))


    def testIsAbsolute(self):
        """
        Tests the isAbsolute() method.

        1. relative path
        2. absolute root path
        3. absolute drive based path
        4. absolute drive relative path
        5. absolute home path
        6. absolute user path

        """
        data={
            # 1
            'relative':['dir\\file',False],
            # 2
            'absoluteRoot':['\\dir\\file',True],
            # 3
            'absoluteDriveBase':['C:\\dir\\file',True],
            # 4 - TODO: check this one out
            'absoluteDriveRelative':['C:dir\\file',False],
            # 5
            # FIX:'absoluteHome':['~/file',True]
            # 6
            # FIX:'absoluteUser':['~ufsiTest/file',True]
        }

        for k in data.iterkeys():
            r1=ufsi.NativeWindowsPath(data[k][0]).isAbsolute()
            r2=data[k][1]
            self.assertEquals(r1,r2,
                              '%s: isAbsolute result was %r but should be %r'
                              %(k,r1,r2))


    def testIsFile(self):
        """
        Tests the isFile() method.

        1. existing file
        2. non-existing file
        3. existing dir

        """
        P=lambda p:ufsi.NativeWindowsPath(p)
        existingFilePath=P(self.existingFilePathStr)
        nonExistingFilePath=P(self.nonExistingFilePathStr)
        existingDirPath=P(self.existingDirPathStr)


        # 1
        self.assertEquals(existingFilePath.isFile(),True,
                          '%r is a file'%str(existingFilePath))

        # 2
        self.assertEquals(nonExistingFilePath.isFile(),False,
                          'File %r does not exist'%str(nonExistingFilePath))

        # 3
        self.assertEquals(existingDirPath.isFile(),False,
                          '%r is a dir'%str(existingDirPath))
        
    def testIsDir(self):
        """
        Tests the isDir() method.

        1. existing dir
        2. non-existing dir
        3. existing dir, no trailing slash
        4. existing file

        """
        P=lambda p:ufsi.NativeWindowsPath(p)
        existingDirPath=P(self.existingDirPathStr)
        nonExistingDirPath=P(self.nonExistingDirPathStr)
        existingDirNoTrailingSlashPath=P(self.existingDirPathStr[:-1])
        existingFilePath=P(self.existingFilePathStr)

        # 1
        self.assertEquals(existingDirPath.isDir(),True,
                          '%r is a dir'%str(existingDirPath))

        # 2
        self.assertEquals(nonExistingDirPath.isDir(),False,
                          '%r does not exist'%str(nonExistingDirPath))

        # 3
        self.assertEquals(existingDirNoTrailingSlashPath.isDir(),True,
                          '%r is a dir'%str(existingDirNoTrailingSlashPath))

        # 4
        self.assertEquals(existingFilePath.isDir(),False,
                          '%r is a file'%str(existingFilePath))

    def testIsSymlink(self):
        """
        Tests the isSymlink() method.

        1. existing file
        2. existing dir

        """
        P=lambda p:ufsi.NativeWindowsPath(p)
        existingFilePath=P(self.existingFilePathStr)
        existingDirPath=P(self.existingDirPathStr)

        # 1
        self.assertEquals(existingFilePath.isSymlink(),False,
                          '%r is not a symlink'
                          %str(existingFilePath))

        # 2
        self.assertEquals(existingDirPath.isSymlink(),False,
                          '%r is not a symlink'
                          %str(existingDirPath))


    def testGetSymlinkPath(self):
        """
        Tests the getSymlinkPath() method.

        1. existing file
        2. existing dir

        """
        P=lambda p:ufsi.NativeWindowsPath(p)
        existingFilePath=P(self.existingFilePathStr)
        existingDirPath=P(self.existingDirPathStr)

        # 1
        self.assertRaises(ufsi.NotASymlinkError,
                          existingFilePath.getSymlinkPath)

        # 2
        self.assertRaises(ufsi.NotASymlinkError,
                          existingDirPath.getSymlinkPath)
