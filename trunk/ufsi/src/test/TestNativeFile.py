"""
Tests the NativeFile implementation.

"""


import ufsi

import os
import stat
import unittest



class TestNativeFile(unittest.TestCase):
    """
    Tests the NativeFile implementation
    
    """


    def setUp(self):
        """
        Creates the test data:

        * existing file, content
          '12345678901234567890\nSecondLine\nThirdLine'
        * non existing file
        * write file, empty content

        """
        
        self.windows=False
        if os.name=='nt':
            self.windows=True

        # file paths
        self.existingFilePathStr='data/existing'
        self.existingFileContents='12345678901234567890\nSecondLine\nThirdLine'
        self.nonExistingFilePathStr='data/nonexisting'
        self.writeFilePathStr='data/write'
        self.writeFileContents='test content\nsecond line\n'

        # existing file
        f=file(self.existingFilePathStr,'w')
        f.write(self.existingFileContents)
        f.close()
        assert os.path.isfile(self.existingFilePathStr)

        # non existing file
        if os.path.isfile(self.nonExistingFilePathStr):
            os.remove(self.nonExistingFilePathStr)
        assert os.path.exists(self.nonExistingFilePathStr)==False

        # file for writing
        f=file(self.writeFilePathStr,'w')
        f.close()
        assert os.stat(self.writeFilePathStr)[stat.ST_SIZE]==0


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
        f.open('w')
        f.close()
        self.assertEqual(os.stat(self.existingFilePathStr)[stat.ST_SIZE],0,
                         'File was not truncated')
        
        # 4
        f=nonExistingFilePath.getFile()
        f.open('w')
        f.close()
        self.assert_(os.path.exists(self.nonExistingFilePathStr),
                    'File was not created')
        self.assertEqual(os.stat(self.nonExistingFilePathStr)[stat.ST_SIZE],0,
                         'File was not truncated')


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
        f.open('w')
        f.write(self.writeFileContents)
        f.close()
        f=file(self.writeFilePathStr,'r')
        self.assertEqual(f.read(),self.writeFileContents,
                         'Contents were not written correctly')
        f.close()

    def testWriteLines(self):
        """
        Tests the writeLines method.

        1. Write a list of lines to a file.

        """
        writeFilePath=ufsi.Path(self.writeFilePathStr)
        lines=self.writeFileContents.splitlines(True)

        # 1
        f=writeFilePath.getFile()
        f.open('w')
        f.writeLines(lines)
        f.close()
        f=file(self.writeFilePathStr,'r')
        self.assertEqual(f.readlines(),lines,
                         'Contents were not written correctly')
        f.close()

        
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
        s2=os.stat(self.existingFilePathStr)
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
        self.assertEquals(s1['mode'],s2[stat.ST_MODE],
                          'Mode not correct')
        self.assertEquals(s1['inodeNumber'],s2[stat.ST_INO],
                          'Inode number not correct')
        self.assertEquals(s1['inodeDevice'],s2[stat.ST_DEV],
                          'Inode device not correct')
        self.assertEquals(s1['inodeLinks'],s2[stat.ST_NLINK],
                          'Inode links count not correct')

        # 2
        f=nonExistingFilePath.getFile()
        self.assertRaises(ufsi.PathNotFoundError,f.getStat)
