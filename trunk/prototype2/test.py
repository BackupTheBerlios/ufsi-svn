import sys
import unittest

import ufsi
import test.ufsi.TestNativeUnixPath
import test.ufsi.TestNativeWindowsPath


if __name__=="__main__":
	suites=[]
	suites.append(unittest.makeSuite(test.ufsi.TestNativeUnixPath.TestNativeUnixPath))
	suites.append(unittest.makeSuite(test.ufsi.TestNativeWindowsPath.TestNativeWindowsPath))
	#suites.append(unittest.makeSuite(test.ufsi.TestNativePath.TestNativePath))
	unittest.TextTestRunner(verbosity=10).run(unittest.TestSuite(suites))
