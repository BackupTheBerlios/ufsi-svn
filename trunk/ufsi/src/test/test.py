"""
"""

import unittest
import os

from TestNativeFile import TestNativeFile
from TestNativeDir import TestNativeDir
from TestNativeWindowsPath import TestNativeWindowsPath
from TestNativeUnixPath import TestNativeUnixPath

from TestFtpFile import TestFtpFile

from TestTarPath import TestTarPath
from TestTarDir import TestTarDir

suites=[]
# Native implementations

suites.append(unittest.makeSuite(TestNativeFile))
suites.append(unittest.makeSuite(TestNativeDir))
if os.name=='nt':
    suites.append(unittest.makeSuite(TestNativeWindowsPath))
else:
    suites.append(unittest.makeSuite(TestNativeUnixPath))

# Http implementations

# Ftp implementations
suites.append(unittest.makeSuite(TestFtpFile))

# Tar implementations
suites.append(unittest.makeSuite(TestTarPath))
suites.append(unittest.makeSuite(TestTarDir))

# run them all
unittest.TextTestRunner(verbosity=10).run(unittest.TestSuite(suites))

