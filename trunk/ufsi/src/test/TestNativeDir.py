"""
Tests the NativeDir implementation.

"""


import ufsi

import os
import stat
import unittest



class TestNativeDir(unittest.TestCase):
    """
    Tests the NativeDir implementation
    
    """


    def setUp(self):
        """
        Creates the test data:

        * existing dir, containing files: test1,test2
        * non existing dir

        """
        
        self.windows=False
        if os.name=='nt':
            self.windows=True

        # paths
        self.existingDirPathStr='data/existingDir'
        self.existingDirDirList=['test1','test2']
        self.nonExistingDirPathStr='data/nonexistingDir'

        # existing dir
        if not os.path.isdir(self.existingDirPathStr):
            os.makedirs(self.existingDirPathStr)
        assert os.path.isdir(self.existingDirPathStr)
        for fn in self.existingDirDirList:
            p=os.path.join(self.existingDirPathStr,fn)
            f=file(p,'w')
            f.close()
            assert os.path.isfile(p)

        # non existing file
        if os.path.isdir(self.nonExistingDirPathStr):
            os.rmdir(self.nonExistingDirPathStr)
        assert os.path.exists(self.nonExistingDirPathStr)==False


    def testGetDirList(self):
        """
        Tests the getDirList() method.

        1. getDirList of existing directory
        2. getDirList of non-existing directory

        TODO: test re filtering

        """
        existingDirPath=ufsi.Path(self.existingDirPathStr)
        nonExistingDirPath=ufsi.Path(self.nonExistingDirPathStr)

        # 1
        d=existingDirPath.getDir()
        self.assertEquals(d.getDirList(),self.existingDirDirList,
                          'Returned dir list was not correct')

        # 2
        d=nonExistingDirPath.getDir()
        self.assertRaises(ufsi.PathNotFoundError,d.getDirList)


    def testGetStat(self):
        """
        Tests the getStat() method.

        1. getStat on existing directory
        2. getStat on non-existing directory

        """
        existingDirPath=ufsi.Path(self.existingDirPathStr)
        nonExistingDirPath=ufsi.Path(self.nonExistingDirPathStr)
        
        # 1
        d=existingDirPath.getDir()
        s1=d.getStat()
        s2=os.stat(self.existingDirPathStr)
        self.assertEquals(s1['size'],s2[stat.ST_SIZE],'Size not correct')
        self.assertEquals(s1['accessTime'],s2[stat.ST_ATIME],
                          'Access time not correct')
        self.assertEquals(s1['modificationTime'],s2[stat.ST_MTIME],
                          'Modification time not correct')
        self.assertEquals(s1['creationTime'],s2[stat.ST_CTIME],
                          'Creation time not correct')
        self.assertEquals(s1['userId'],s2[stat.ST_UID],
                          'UserID not correct')
        self.assertEquals(s1['groupId'],s2[stat.ST_GID],
                          'GroupID not correct')
        self.assertEquals(s1['permissions'],s2[stat.ST_MODE],
                          'Mode not correct')
        self.assertEquals(s1['inodeNumber'],s2[stat.ST_INO],
                          'Inode number not correct')
        self.assertEquals(s1['inodeDevice'],s2[stat.ST_DEV],
                          'Inode device not correct')
        self.assertEquals(s1['inodeLinks'],s2[stat.ST_NLINK],
                          'Inode links count not correct')

        # 2
        d=nonExistingDirPath.getDir() 
        self.assertRaises(ufsi.PathNotFoundError,d.getStat)


