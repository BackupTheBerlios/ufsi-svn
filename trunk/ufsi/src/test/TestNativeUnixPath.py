"""
Tests the NativeUnixPath implementation.

"""


import ufsi

import os
import stat
import unittest



class TestNativeUnixPath(unittest.TestCase):
    """
    Tests the NativeUnixPath implementation.


    Preconditions: 

    * it is being run on a unix compatible operating system.
    
    """


    def setUp(self):
        """
        Creates the test data:

        * existing dir, contents unimportant
        * non existing dir

        TODO: update docstring

        """
        
        if os.name=='nt':
            raise Exception('This class must be run on a unix compatible os')

        # paths
        self.existingDirPathStr='data/existingDir/'
        self.nonExistingDirPathStr='data/nonexistingDir/'
        self.existingFilePathStr='data/existing'
        self.nonExistingFilePathStr='data/nonexisting'
        # symlinks (path of symlink file, then path to the real file)
        self.existingValidSymlinkFilePathStr='data/existingValidSymlinkFile'
        self.existingValidFileSymlinkPath='existing'
        self.existingValidSymlinkDirPathStr='data/existingValidSymlinkDir'
        self.existingValidDirSymlinkPath='existingDir'
        self.existingInvalidSymlinkFilePathStr=\
                'data/existingInvalidSymlinkFile'
        self.existingInvalidFileSymlinkPath='nonexisting'
        self.existingInvalidSymlinkDirPathStr='data/existingInvalidSymlinkDir'
        self.existingInvalidDirSymlinkPath='nonexistingDir'
        self.nonExistingSymlinkPathStr='data/nonExistingSymlink'

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

        # existing symlinks
        symlinks=[
            [self.existingValidSymlinkFilePathStr,
             self.existingValidFileSymlinkPath],
            [self.existingValidSymlinkDirPathStr,
             self.existingValidDirSymlinkPath],
            [self.existingInvalidSymlinkFilePathStr,
             self.existingInvalidFileSymlinkPath],
            [self.existingInvalidSymlinkDirPathStr,
             self.existingInvalidDirSymlinkPath]
        ]
        for (s,p) in symlinks:
            if not os.path.islink(s):
                os.symlink(p,s)
            assert os.path.islink(s)
            assert os.readlink(s)==p

        # nonexisting symlink
        p=self.nonExistingSymlinkPathStr
        if os.path.islink(p):
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

        """
        data={
            # 1
            'emptyPath':
            ['',{'fileBase':'',
                 'fileExt':None,
                 'dirs':[]}],

            # 2
            'fileBaseOnly':
            ['fileBase',{'fileBase':'fileBase',
                         'fileExt':None,
                         'dirs':[]}],
            
            # 3
            'fileExtOnly':
            ['.ext',{'fileBase':'',
                     'fileExt':'ext',
                     'dirs':[]}],

            # 4
            'fileBaseEmptyFileExt':
            ['fileBase.',{'fileBase':'fileBase',
                          'fileExt':'',
                          'dirs':[]}],

            # 5
            'fullFileName':
            ['fileBase.ext',{'fileBase':'fileBase',
                          'fileExt':'ext',
                          'dirs':[]}],

            # 6
            'singleDir':
            ['dir/',{'fileBase':'',
                          'fileExt':None,
                          'dirs':['dir']}],

            # 7
            'twoDirs':
            ['dir1/dir2/',{'fileBase':'',
                          'fileExt':None,
                          'dirs':['dir1','dir2']}],

            # 8
            'absolutePathTwoDirsFullFileName':
            ['/dir1/dir2/fileBase.ext',{'fileBase':'fileBase',
                                        'fileExt':'ext',
                                        'dirs':['','dir1','dir2']}],

            # 9
            'dirWithAPeriod':
            ['/dir.dirExt/fileBase.fileExt',{'fileBase':'fileBase',
                                             'fileExt':'fileExt',
                                             'dirs':['','dir.dirExt']}]
        }

        for k in data.iterkeys():
            s1=ufsi.NativeUnixPath(data[k][0]).split()
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
        P=lambda p:ufsi.NativeUnixPath(p)
        data={
            # 1
            'relativePath':
            ['/dir1/',P('dir2/fileBase.ext'),'/dir1/dir2/fileBase.ext'],

            # 2
            'absolutePath':
            ['/dir1/',P('/dir2/fileBase.ext'),'/dir2/fileBase.ext'],

            # 3
            'notSeparatorTerminatedPath':
            ['dir1',P('dir2/fileBase.ext'),'dir1/dir2/fileBase.ext'],

            # 4
            'emptyPath':
            ['dir1',P(''),'dir1/'],

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
        3. absolute home path
        4. absolute user path

        """
        data={
            # 1
            'relative':['dir/file',False],
            # 2
            'absoluteRoot':['/dir/file',True],
            # 3
            # FIX:'absoluteHome':['~/file',True]
            # 4
            # FIX:'absoluteUser':['~ufsiTest/file',True]
        }

        for k in data.iterkeys():
            r1=ufsi.NativeUnixPath(data[k][0]).isAbsolute()
            r2=data[k][1]
            self.assertEquals(r1,r2,
                              '%s: isAbsolute result was %r but should be %r'
                              %(k,r1,r2))


    def testIsFile(self):
        """
        Tests the isFile() method.

        1. existing file
        2. non-existing file
        3. existing file referenced through a symlink
        4. non-existing file referenced through a symlink
        5. existing dir

        """
        P=lambda p:ufsi.NativeUnixPath(p)
        existingFilePath=P(self.existingFilePathStr)
        nonExistingFilePath=P(self.nonExistingFilePathStr)
        existingValidFileSymlinkPath=P(self.existingValidSymlinkFilePathStr)
        existingInvalidFileSymlinkPath=\
                P(self.existingInvalidSymlinkFilePathStr)
        existingDirPath=P(self.existingDirPathStr)


        # 1
        self.assertEquals(existingFilePath.isFile(),True,
                          '%r is a file'%str(existingFilePath))

        # 2
        self.assertEquals(nonExistingFilePath.isFile(),False,
                          'File %r does not exist'%str(nonExistingFilePath))

        # 3
        self.assertEquals(existingValidFileSymlinkPath.isFile(),True,
                          '%r is a file'%str(existingValidFileSymlinkPath))

        # 4
        self.assertEquals(existingInvalidFileSymlinkPath.isFile(),False,
                          '%r is an invalid symlink'
                          %str(existingInvalidFileSymlinkPath))

        # 5
        self.assertEquals(existingDirPath.isFile(),False,
                          '%r is a dir'%str(existingDirPath))
        
    def testIsDir(self):
        """
        Tests the isDir() method.

        1. existing dir
        2. non-existing dir
        3. existing dir, no trailing slash
        4. existing dir referenced through a symlink
        5. non-existing dir referenced through a symlink
        6. existing file

        """
        P=lambda p:ufsi.NativeUnixPath(p)
        existingDirPath=P(self.existingDirPathStr)
        nonExistingDirPath=P(self.nonExistingDirPathStr)
        existingDirNoTrailingSlashPath=P(self.existingDirPathStr[:-1])
        existingValidDirSymlinkPath=P(self.existingValidSymlinkDirPathStr)
        existingInvalidDirSymlinkPath=P(self.existingInvalidSymlinkDirPathStr)
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
        self.assertEquals(existingValidDirSymlinkPath.isDir(),True,
                          '%r is a dir'%str(existingValidDirSymlinkPath))

        # 5
        self.assertEquals(existingInvalidDirSymlinkPath.isDir(),False,
                          '%r is an invalid symlink'
                          %str(existingInvalidDirSymlinkPath))

        # 6
        self.assertEquals(existingFilePath.isDir(),False,
                          '%r is a file'%str(existingFilePath))

    def testIsSymlink(self):
        """
        Tests the isSymlink() method.

        1. existing valid symlink
        2. existing invalid symlink
        3. non-existing symlink

        """
        P=lambda p:ufsi.NativeUnixPath(p)
        existingValidSymlinkPath=P(self.existingValidSymlinkFilePathStr)
        existingInvalidSymlinkPath=P(self.existingInvalidSymlinkFilePathStr)
        nonExistingSymlinkPath=P(self.nonExistingSymlinkPathStr)

        # 1
        self.assertEquals(existingValidSymlinkPath.isSymlink(),True,
                          'Symlink %r exists'
                          %str(existingValidSymlinkPath))

        # 2
        self.assertEquals(existingInvalidSymlinkPath.isSymlink(),True,
                          'Symlink %r exists'
                          %str(existingInvalidSymlinkPath))

        # 3
        self.assertEquals(nonExistingSymlinkPath.isSymlink(),False,
                          'Symlink %r does not exist'
                          %str(nonExistingSymlinkPath))


    def testGetSymlinkPath(self):
        """
        Tests the getSymlinkPath() method.

        1. existing symlink to a file
        2. existing symlink to a dir
        3. existing file
        4. existing dir
        5. non-existing symlink

        """
        P=lambda p:ufsi.NativeUnixPath(p)
        existingValidFileSymlinkPath=P(self.existingValidSymlinkFilePathStr)
        existingValidDirSymlinkPath=P(self.existingValidSymlinkDirPathStr)
        existingFilePath=P(self.existingFilePathStr)
        existingDirPath=P(self.existingDirPathStr)
        nonExistingSymlinkPath=P(self.nonExistingSymlinkPathStr)

        # 1
        r1=str(existingValidFileSymlinkPath.getSymlinkPath())
        r2=self.existingValidFileSymlinkPath
        self.assertEquals(r1,r2,'Symlink path expected %r. Got %r'%(r2,r1))
        
        # 2
        r1=str(existingValidDirSymlinkPath.getSymlinkPath())
        r2=self.existingValidDirSymlinkPath
        self.assertEquals(r1,r2,'Symlink path expected %r. Got %r'%(r2,r1))

        # 3
        self.assertRaises(ufsi.NotASymlinkError,
                          existingFilePath.getSymlinkPath)

        # 4
        self.assertRaises(ufsi.NotASymlinkError,
                          existingDirPath.getSymlinkPath)

        # 5
        self.assertRaises(ufsi.NotASymlinkError,
                          nonExistingSymlinkPath.getSymlinkPath)
