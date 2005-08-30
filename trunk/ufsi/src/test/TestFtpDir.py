"""
Tests the FtpDir implementation.

"""


import ufsi

import unittest



class TestFtpDir(unittest.TestCase):
    """
    Tests the FtpDir implementation
    
    """


    def setUp(self):
        """
        Creates the test data:

        * existing dir, containing files: test1,test2
        * non existing dir

        TODO: update docstring

        """
        
        # paths
        self.existingDirPathStr='existingDir/'
        self.existingDirPath=ufsi.TarPath(self.tarFilePath,
                                          self.existingDirPathStr)
        self.existingDirDirList=['test1','test2']
        self.nonExistingDirPathStr='nonexistingDir/'
        self.nonExistingDirPath=ufsi.TarPath(self.tarFilePath,
                                          self.nonExistingDirPathStr)


    def testGetDirList(self):
        """
        Tests the getDirList() method.

        1. getDirList of existing directory
        2. getDirList of non-existing directory

        TODO: test re filtering

        """
        # 1
        d=self.existingDirPath.getDir()
        self.assertEquals(d.getDirList(),self.existingDirDirList,
                          'Returned dir list was not correct')

        # 2
        d=self.nonExistingDirPath.getDir()
        self.assertRaises(ufsi.PathNotFoundError,d.getDirList)


    def testGetStat(self):
        """
        Tests the getStat() method.

        1. getStat on existing directory
        2. getStat on non-existing directory

        TODO: actually test that the content received is valid tar info
        """
        # 1
        d=self.existingDirPath.getDir()
        s1=d.getStat()

        # 2
        d=self.nonExistingDirPath.getDir() 
        self.assertRaises(ufsi.PathNotFoundError,d.getStat)


