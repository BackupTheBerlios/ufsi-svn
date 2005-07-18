import os
import os.path
import ufsi
import ufsi.LocalPath
import unittest

"""
Paths to test:

Windows:
	Unc:
		\\
		\\server
		\\server\
		\\server.com
		\\server.com\
		\\server\file
		\\server\file.
		\\server\file.ext
		\\server\dir\
		\\server\dir\file.ext
		//server/dir/file # windows doesn't find either of these
		\/server/dir\file #  ditto...
	
	Drive Letter:
		C:
		C:file
		C:dir\file
		C:\
		C:\file
		C:\file.
		C:\file.ext
		C:\dir\
		C:\dir\file.ext

	Regular path:
		\file
		file
		\dir\
		dir\
		\dir\file
		dir\file
		~\file
		~\dir\
		~user\dir\
		~user\file
	
Unix & windows:
	Regular path:
		/file
		/file.ext
		/dir/
		/dir/file.ext
"""


class TestLocalPath(unittest.TestCase):
	def setUp(self):
		self.winDrive=ufsi.LocalPath.LocalPathBuilder().build(r'C:\test')
		self.winUnc=ufsi.LocalPath.LocalPathBuilder().build(r'\\hostname\test')
		self.osAbs=ufsi.LocalPath.LocalPathBuilder().build(r'/test/file')
		self.osRel=ufsi.LocalPath.LocalPathBuilder().build(r'test/file')
	
	def testCorrectPathType(self):
		if os.name=='nt':
			self.assertTrue(isinstance(self.p,ufsi.LocalPath.LocalWindowsPath))
			self.assertEqual(str(self.p),"\\test\\this\\out")
		else:
			self.assertTrue(isinstance(self.p,ufsi.LocalPath.LocalUnixPath))
