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
        # location of the testing server
        host='localhost'
        server='ftp://'+host+'/'
        self.testDataDir='ufsiTd/'

        # dirs
        self.existingDir='existingDir'
        self.existingDirPath=ufsi.FtpPath(server+self.testDataDir+
                                          self.existingDir)
        self.existingDirDirList=['file1','file2']
        
        self.nonExistingDir='nonExistingDir'
        self.nonExistingDirPath=ufsi.FtpPath(server+self.testDataDir+
                                             self.nonExistingDir)


    def testGetDirList(self):
        """
        Tests the getDirList() method.

        1. getDirList of existing directory
        2. getDirList of non-existing directory

        TODO: test re filtering

        """
        # 1
        d=self.existingDirPath.getDir()
        dirList=d.getDirList()
        dirList.sort()
        self.existingDirDirList.sort()
        self.assertEquals(dirList,self.existingDirDirList,
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


