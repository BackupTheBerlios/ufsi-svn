"""
"""

import unittest
import ftplib

import ufsi


class TestFtpFile(unittest.TestCase):
    """
    
    """

    def setUp(self):
        """
        """
        # location of the testing server
        host='localhost'
        server='ftp://'+host+'/'
        self.testDataDir='ufsiTd/'

        # authentication details
        readUser='ufsitestread'
        readPassword='ufsitestread'
        writeUser='ufsitestwrite'
        writePassword='ufsitestwrite'
        # to save from creating another account, simply assign
        # readUserAuth to None for anonymous login
        self.readUserAuth=ufsi.UserPasswordAuthentication(
                readUser,readPassword)
        self.writeUserAuth=ufsi.UserPasswordAuthentication(
                writeUser,writePassword)
        self.anonUserAuth=None

        # files
        self.existingFile='existing'
        self.existingFilePath=ufsi.FtpPath(
            server+self.testDataDir+self.existingFile)
        self.existingFileContents=\
                '12345678901234567890\nSecondLine\nThirdLine\n'

        self.nonExistingFile='nonExisting'
        self.nonExistingFilePath=ufsi.FtpPath(
                server+self.testDataDir+self.nonExistingFile)

        # dirs
        self.existingDir='existingDir'
        self.existingDirPath=ufsi.FtpPath(server+self.testDataDir+
                                          self.existingDir)
        self.nonExistingDir='nonExistingDir'
        self.nonExistingDirPath=ufsi.FtpPath(server+self.testDataDir+
                                             self.nonExistingDir)
        # write file
        self.writeFile='write'
        self.writeFilePath=ufsi.Path(
                server+self.testDataDir+self.writeFile)
        self.writeFileContents='a couple\nof\nlines'
        
        # TODO: test symlinks (when implemented)

        self.server=server
        self.host=host


    def testOpen(self):
        """
        Tests the open() method.

        1. open existing file for read
        2. open non-existing file for read
        3. open existing file for read as anon
        4. open non-existing file for read as anon
        5. open existing file for write
        6. open non-existing file for write
        7. open existing file for write with read account

        """
        existingFilePath=self.existingFilePath
        nonExistingFilePath=self.nonExistingFilePath
        writeFilePath=self.writeFilePath
        
        # 1
        existingFilePath.setAuthentication(self.readUserAuth)
        f=existingFilePath.getFile()
        f.open('r')
        f.close()

        # 2
        nonExistingFilePath.setAuthentication(self.readUserAuth)
        f=nonExistingFilePath.getFile()
        self.assertRaises(ufsi.PathNotFoundError,f.open,'r')

        # 3
        existingFilePath.setAuthentication(self.anonUserAuth)
        f=existingFilePath.getFile()
        f.open('r')
        f.close()

        # 4
        nonExistingFilePath.setAuthentication(self.anonUserAuth)
        f=nonExistingFilePath.getFile()
        self.assertRaises(ufsi.PathNotFoundError,f.open,'r')

        # 5
        writeFilePath.setAuthentication(self.writeUserAuth)
        f=writeFilePath.getFile()
        f.open('w')
        f.close()
        # test that the file was truncated - assuming the read method works
        f.open('r')
        content=f.read()
        f.close()
        self.assertEqual(content,'','File was not truncated')
        
        # 6
        # TODO: we can't do this without messing up the above test for
        # nonExistingFile path on a subsequent run. Or this file needs
        # to be deleted each run through
##         nonExistingFilePath.setAuthentication(self.writeUserAuth)
##         f=nonExistingFilePath.getFile()
##         f.open('w')
##         f.close()
##         # test that the file was truncated - assuming the read method works
##         f.open('r')
##         content=f.read()
##         f.close()
##         self.assertEqual(content,'','File was not truncated')

        # 7
        existingFilePath.setAuthentication(self.readUserAuth)
        f=existingFilePath.getFile()
        # TODO: this should be an access denied error, but FTP isn't
        # specific enough with its error codes
        self.assertRaises(ufsi.PathNotFoundError,f.open,'w')
        # Should not have write access using a read account



    def testRead(self):
        """
        Tests the read() method.

        1. read the first 10 bytes, then the next 10 bytes, then the rest
        2. read the entire file

        """
        existingFilePath=self.existingFilePath

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
        existingFilePath=self.existingFilePath

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
        existingFilePath=self.existingFilePath

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
        # 1
        self.writeFilePath.setAuthentication(self.writeUserAuth)
        f=self.writeFilePath.getFile()
        f.open('w')
        f.write(self.writeFileContents)
        f.close()
        # now verify it - assuming the read method works
        f.open('r')
        content=f.read()
        f.close()
        self.assertEqual(content,self.writeFileContents,
                         'Contents were not written correctly')

    def testWriteLines(self):
        """
        Tests the writeLines method.

        1. Write a list of lines to a file.

        """
        lines=self.writeFileContents.splitlines(True)

        # 1
        self.writeFilePath.setAuthentication(self.writeUserAuth)
        f=self.writeFilePath.getFile()
        f.open('w')
        f.writeLines(lines)
        f.close()
        # now verify it - assuming the read method works
        f.open('r')
        content=f.read()
        f.close()
        self.assertEqual(content,self.writeFileContents,
                         'Contents were not written correctly')


    def testGetStat(self):
        """
        Tests the getStat() method.

        1. Get the stat of an existing file.
        2. Get the stat of a non-existing file.

        """
        # 1
        f=self.existingFilePath.getFile()
        s1=f.getStat()
        # TODO: test some stuff here.

        # 2
        f=self.nonExistingFilePath.getFile()
        self.assertRaises(ufsi.PathNotFoundError,f.getStat)
