"""
Tests the TarFile implementation.

"""


import ufsi

import unittest



class TestTarFile(unittest.TestCase):
    """
    Tests the TarFile implementation
    
    """


    def setUp(self):
        """
        Creates the test data:

        * existing file, content
          '12345678901234567890\nSecondLine\nThirdLine'
        * non existing file

        """
        self.tarFilePath=ufsi.Path('data/tarfile.tar')
        
        # file paths
        self.existingFilePathStr='existing'
        self.existingFilePath=ufsi.TarPath(self.tarFilePath,
                                           self.existingFilePathStr)
        self.existingFileContents='12345678901234567890\nSecondLine\nThirdLine'
        self.nonExistingFilePathStr='nonExisting'
        self.nonExistingFilePath=ufsi.TarPath(self.tarFilePath,
                                              self.nonExistingFilePathStr)
        self.writeFilePathStr='write'
        self.writeFilePath=ufsi.TarPath(self.tarFilePath,
                                        self.writeFilePathStr)
        self.writeFileContents='test content\nsecond line\n'


    def testOpen(self):
        """
        Tests the open() method.

        1. open existing file for read
        2. open non-existing file for read
        3. open existing file for write
        4. open non-existing file for write

        """
        existingFilePath=ufsi.Path(self.existingFilePathStr)
        nonExistingFilePath=ufsi.Path(self.nonExistingFilePathStr)

        # 1
        f=existingFilePath.getFile()
        f.open('r')
        f.close()

        # 2
        f=nonExistingFilePath.getFile()
        self.assertRaises(ufsi.PathNotFoundError,f.open,'r')

        # 3
        f=existingFilePath.getFile()
        self.assertRaises(ufsi.UnsupportedOperationError,f.open,'w')
        
        # 4
        f=nonExistingFilePath.getFile()
        self.assertRaises(ufsi.UnsupportedOperationError,f.open,'w')


    def testRead(self):
        """
        Tests the read() method.

        1. read the first 10 bytes, then the next 10 bytes, then the rest
        2. read the entire file

        """
        existingFilePath=ufsi.Path(self.existingFilePathStr)

        # 1
        f=existingFilePath.getFile()
        f.open('r')
        self.assertEqual(f.read(10),self.existingFileContents[:10],
                         'Contents read are not correct')
        self.assertEqual(f.read(10),self.existingFileContents[10:20],
                         'Contents read are not correct')
        self.assertEqual(f.read(),self.existingFileContents[20:],
                         'Contents read are not correct')
        f.close()

        # 2
        f=existingFilePath.getFile()
        f.open('r')
        self.assertEqual(f.read(),self.existingFileContents,
                         'Contents read are not correct')
        f.close()

    def testReadLine(self):
        """
        Tests the readLine() method.

        1. Read each line to the end of the file.

        """
        existingFilePath=ufsi.Path(self.existingFilePathStr)

        # 1
        f=existingFilePath.getFile()
        f.open('r')
        lines=self.existingFileContents.splitlines(True)
        for l in lines:
            self.assertEqual(f.readLine(),l,'Contents read are not correct')
        self.assertEqual(f.readLine(),'','Too much content in the file')
        f.close()

    def testReadLines(self):
        """
        Tests the readLines() method

        1. Read all lines.

        """
        existingFilePath=ufsi.Path(self.existingFilePathStr)

        # 1
        f=existingFilePath.getFile()
        f.open('r')
        lines=self.existingFileContents.splitlines(True)
        self.assertEqual(f.readLines(),lines,'Contents read are not correct')
        f.close()
        
        
    def testWrite(self):
        """
        Tests the write() method.

        1. Write to a file.
        
        """
        writeFilePath=ufsi.Path(self.writeFilePathStr)

        # 1
        f=writeFilePath.getFile()
        self.assertRaises(ufsi.UnsupportedOperationError,f.open,'w')
        self.assertRaises(ufsi.UnsupportedOperationError,f.write,'data')

    def testWriteLines(self):
        """
        Tests the writeLines method.

        1. Write a list of lines to a file.

        """
        writeFilePath=ufsi.Path(self.writeFilePathStr)

        # 1
        f=writeFilePath.getFile()
        self.assertRaises(ufsi.UnsupportedOperationError,f.open,'w')
        self.assertRaises(ufsi.UnsupportedOperationError,f.write,['data\n'])

        
    def testGetStat(self):
        """
        Tests the getStat() method.

        1. Get the stat of an existing file.
        2. Get the stat of a non-existing file.

        """
        existingFilePath=ufsi.Path(self.existingFilePathStr)
        nonExistingFilePath=ufsi.Path(self.nonExistingFilePathStr)

        # 1
        f=existingFilePath.getFile()
        s1=f.getStat()
        # TODO: validate returned data

        # 2
        f=nonExistingFilePath.getFile()
        self.assertRaises(ufsi.PathNotFoundError,f.getStat)
